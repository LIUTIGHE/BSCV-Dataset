# -*- coding: utf-8 -*-
import cv2
from PIL import Image
import numpy as np
import importlib
import os
import argparse
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib import animation
import torch

from core.utils import to_tensors


parser = argparse.ArgumentParser(description="BSCVR")
parser.add_argument("-v", "--video", type=str, required=True)
parser.add_argument("-c", "--ckpt", type=str, required=True)
parser.add_argument("-m", "--mask", type=str, required=True)
parser.add_argument("--model", type=str, default='bscvi_hq')
parser.add_argument("--type", type=str, required=True)
parser.add_argument("--step", type=int, default=10)
parser.add_argument("--num_ref", type=int, default=-1)
parser.add_argument("--neighbor_stride", type=int, default=5)
parser.add_argument("--framestride", type=int, default=30)
parser.add_argument("--width", type=int)
parser.add_argument("--height", type=int)

args = parser.parse_args()

ref_length = args.step  # ref_step
num_ref = args.num_ref
neighbor_stride = args.neighbor_stride


# sample reference frames from the whole video
def get_ref_index(f, neighbor_ids, length):
    ref_index = []
    if num_ref == -1:
        for i in range(0, length, ref_length):
            if i not in neighbor_ids:
                ref_index.append(i)
    else:
        start_idx = max(0, f - ref_length * (num_ref // 2))
        end_idx = min(length, f + ref_length * (num_ref // 2))
        for i in range(start_idx, end_idx + 1, ref_length):
            if i not in neighbor_ids:
                if len(ref_index) > num_ref:
                    break
                ref_index.append(i)
    return ref_index


# read frame-wise masks
def read_mask(mpath, size):
    masks = []
    mnames = os.listdir(mpath)
    mnames.sort()
    for mp in mnames:
        m = Image.open(os.path.join(mpath, mp))
        m = m.resize(size, Image.NEAREST)
        m = np.array(m.convert('L'))
        m = np.array(m > 0).astype(np.uint8)
        m = cv2.dilate(m,
                       cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3)),
                       iterations=4)
        masks.append(Image.fromarray(m * 255))
    return masks


#  read frames from video
def read_frame_from_videos(args):
    vname = args.video
    frames = []
    if args.use_mp4:
        vidcap = cv2.VideoCapture(vname)
        success, image = vidcap.read()
        count = 0
        while success:
            image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            frames.append(image)
            success, image = vidcap.read()
            count += 1
    else:
        lst = os.listdir(vname)
        lst.sort()
        fr_lst = [vname + '/' + name for name in lst]
        for fr in fr_lst:
            image = cv2.imread(fr)
            image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            frames.append(image)
    return frames


# resize frames
def resize_frames(frames, size=None):
    if size is not None:
        frames = [f.resize(size) for f in frames]
    else:
        size = frames[0].size
    return frames, size


def main_worker(): 
    # set up models
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    size = (args.width, args.height)

    net = importlib.import_module('model.' + args.model)
    if args.type == 'BSCVR_S':
        model = net.InpaintGenerator_S().to(device)
    elif args.type == 'BSCVR_P':
        model = net.InpaintGenerator_P().to(device)
    data = torch.load(args.ckpt, map_location=device)
    model.load_state_dict(data)
    print(f'Loading model from: {args.ckpt}')
    model.eval()

    # prepare datset
    args.use_mp4 = True if args.video.endswith('.mp4') else False
    print(
        f'Loading videos and masks from: {args.video} | INPUT MP4 format: {args.use_mp4}'
    )
    rframes = read_frame_from_videos(args)
    rframes, size = resize_frames(rframes, size)
    h, w = size[1], size[0]
    video_length = len(rframes)
    rmasks = read_mask(args.mask, size)

    comp_frames = [None] * video_length
    
    framestride = args.framestride

    x_frames = [rframes[i:i + framestride] for i in range(0, len(rframes), framestride)]
    x_masks = [rmasks[i:i + framestride] for i in range(0, len(rmasks), framestride)]

    for itern in range(0, len(x_frames), 1):
        stride_length = len(x_frames[itern])
        print(stride_length)
        imgs = to_tensors()(x_frames[itern]).unsqueeze(0) * 2 - 1
        frames = [np.array(f).astype(np.uint8) for f in x_frames[itern]]


        binary_masks = [
            np.expand_dims((np.array(m) != 0).astype(np.uint8), 2) for m in x_masks[itern]
        ]
        masks = to_tensors()(x_masks[itern]).unsqueeze(0)
        imgs, masks = imgs.to(device), masks.to(device)

        # completing holes
        print(f'Start test...')
        for f in tqdm(range(0, stride_length, neighbor_stride)):
            neighbor_ids = [
                i for i in range(max(0, f - neighbor_stride),
                                 min(stride_length, f + neighbor_stride + 1))
            ]
            ref_ids = get_ref_index(f, neighbor_ids, stride_length)
            selected_imgs = imgs[:1, neighbor_ids + ref_ids, :, :, :]
            selected_masks = masks[:1, neighbor_ids + ref_ids, :, :, :]
            with torch.no_grad():
                masked_imgs = selected_imgs * (1 - selected_masks)
                corrupted_contents = selected_imgs * selected_masks
                mod_size_h = 60
                mod_size_w = 108
                h_pad = (mod_size_h - h % mod_size_h) % mod_size_h
                w_pad = (mod_size_w - w % mod_size_w) % mod_size_w

                masked_imgs = torch.cat(
                    [masked_imgs, torch.flip(masked_imgs, [3])],
                    3)[:, :, :, :h + h_pad, :]
                masked_imgs = torch.cat(
                    [masked_imgs, torch.flip(masked_imgs, [4])],
                    4)[:, :, :, :, :w + w_pad]
                corrupted_contents = torch.cat(
                    [corrupted_contents, torch.flip(corrupted_contents, [3])],
                    3)[:, :, :, :h + h_pad, :]
                corrupted_contents = torch.cat(
                    [corrupted_contents, torch.flip(corrupted_contents, [4])],
                    4)[:, :, :, :, :w + w_pad]
                pred_imgs, _= model(masked_imgs, corrupted_contents, len(neighbor_ids))
                pred_imgs = pred_imgs[:, :, :h, :w]
                pred_imgs = (pred_imgs + 1) / 2
                pred_imgs = pred_imgs.cpu().permute(0, 2, 3, 1).numpy() * 255
                for i in range(len(neighbor_ids)):
                    idx = neighbor_ids[i]
                    img = np.array(pred_imgs[i]).astype(
                        np.uint8) * binary_masks[idx] + frames[idx] * (
                            1 - binary_masks[idx])
                    if comp_frames[(itern * framestride) + idx] is None:
                        comp_frames[(itern * framestride) + idx] = img
                    else:
                        comp_frames[(itern * framestride) + idx] = comp_frames[(itern * framestride) + idx].astype(
                            np.float32) * 0.5 + img.astype(np.float32) * 0.5
    
    print('Saving videos arr...')
    save_dir_name = './result'
    save_base_name = args.video.split('/')[-1]
    save_ver_name = '_' + args.type
    save_base_name = save_base_name + save_ver_name
    # print(save_base_name)
    if not os.path.exists(save_dir_name):
        os.makedirs(save_dir_name)
    save_path = os.path.join(save_dir_name, save_base_name)
    # save the comp_frames as gif
    new_comp_frames = []
    for frame in comp_frames:
        if frame is not None:
            new_frame = frame.astype(np.uint8)
            new_comp_frames.append(new_frame)

    imgs = [Image.fromarray(comp_frame) for comp_frame in new_comp_frames]
    # image folder
    imwrite_path = os.path.join(save_path, 'frame_seq')
    if not os.path.exists(imwrite_path):
        os.makedirs(imwrite_path)
    for i, img in enumerate(imgs):
        img.save(os.path.join(imwrite_path, f'{i:05d}.jpg'))
    # 30 fps gif
    imgs[0].save(os.path.join(save_path, 'GIF_result.gif'), save_all=True, append_images=imgs[1:], duration=40, loop=0)

if __name__ == '__main__':
    main_worker()
