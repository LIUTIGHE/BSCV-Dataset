import os
import json
import random

import cv2
from PIL import Image
import numpy as np

import torch
import torchvision.transforms as transforms

from core.utils import (TrainZipReader, TestZipReader,
                        create_random_shape_with_random_motion, Stack,
                        ToTorchFormatTensor, GroupRandomHorizontalFlip) 

import concurrent.futures

# Mean Hash
def aHash(img):
    img = img.resize((8, 8), Image.ANTIALIAS)
    img = img.convert('L')
    pixels = np.array(img.getdata())
    avg = pixels.mean()
    diff = pixels > avg
    hash_value = ''
    for d in diff:
        hash_value += '1' if d else '0'
    return hash_value

# Hamming Distance
def hammingDistance(hash1, hash2):
    return sum(ch1 != ch2 for ch1, ch2 in zip(hash1, hash2))

class TrainDataset(torch.utils.data.Dataset):
    def __init__(self, args: dict, debug=False):
        self.args = args
        self.num_local_frames = args['num_local_frames']
        self.num_ref_frames = args['num_ref_frames']
        self.size = self.w, self.h = (args['w'], args['h'])

        json_path = os.path.join(args['data_root'], args['name'], 'train.json')
        with open(json_path, 'r') as f:
            self.video_dict = json.load(f)
        self.video_names = list(self.video_dict.keys())
        if debug:
            self.video_names = self.video_names[:100]

        self._to_tensors = transforms.Compose([
            Stack(),
            ToTorchFormatTensor(),
        ])

    def __len__(self):
        return len(self.video_names)

    def __getitem__(self, index):
        item = self.load_item(index)
        return item
    

    def _sample_index(self, length, sample_length, video_name, num_ref_frame=3):
        complete_idx_set = list(range(length))
        pivot = random.randint(0, length - sample_length)
        local_idx = complete_idx_set[pivot:pivot + sample_length]
        remain_idx = list(set(complete_idx_set) - set(local_idx))

        def process_image(idx):
            video_path = os.path.join(self.args['data_root'],
                                    self.args['name'], 'JPEGImages',
                                    f'{video_name}.zip')
            img = TrainZipReader.imread(video_path, idx).convert('RGB')
            if img is None:
                return None, None
            mask_path = os.path.join(self.args['data_root'], 
                                    self.args['name'], 'train_mask', 
                                    video_name, str(idx).zfill(5) + '.png')
            if not os.path.exists(mask_path):
                return None, None
            mask = Image.open(mask_path).resize(self.size, Image.NEAREST).convert('L')
            mask = np.asarray(mask)
            if not mask.sum() == 0:
                return None, None
            img = img.resize(self.size)
            return img, idx

        def calculate_distance(ref_img, target_img, idx):
            # hash1 = aHash(Image.fromarray(ref_img))
            hash2 = aHash(Image.fromarray(target_img))
            hash1 = aHash(ref_img)
            # hash2 = aHash(target_img)
            distance = hammingDistance(hash1, hash2)
            return distance, idx

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_image, idx) for idx in remain_idx]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
            ref_imgs = [res[0] for res in results if res[0] is not None]
            remain_idx = [res[1] for res in results if res[1] is not None]

        mididx = local_idx[(len(local_idx)+1)//2]
        video_path = os.path.join(self.args['data_root'], self.args['name'], 'JPEGImages', f'{video_name}.zip')
        target_img = TrainZipReader.imread(video_path, mididx).convert('RGB')
        target_img = target_img.resize(self.size)
        target_img = np.asarray(target_img)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(calculate_distance, ref_img, target_img, idx) 
                    for ref_img, idx in zip(ref_imgs, remain_idx)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
            distance_list = [res[0] for res in results]
            remain_idx = [res[1] for res in results]

        ref_index = []
        for i in range(num_ref_frame):
            min_idx = distance_list.index(min(distance_list))
            ref_index.append(remain_idx[min_idx])
            distance_list[min_idx] = 1000000

        # ref_index = sorted(random.sample(remain_idx, num_ref_frame)) # random sample
        
        # for idx in remain_idx: # Similarity-based sampling step 1: select uncorrupted frames
        #     video_path = os.path.join(self.args['data_root'],
        #                               self.args['name'], 'JPEGImages',
        #                               f'{video_name}.zip')
        #     img = TrainZipReader.imread(video_path, idx).convert('RGB')
        #     if img is None:
        #         continue

        #     mask_path = os.path.join(self.args['data_root'], 
        #                              self.args['name'], 'train_mask', 
        #                              video_name, str(idx).zfill(5) + '.png')
        #     if not os.path.exists(mask_path):
        #         continue
            
        #     mask = Image.open(mask_path).resize(self.size,
        #                                         Image.NEAREST).convert('L')
        #     mask = np.asarray(mask)
            
        #     if not mask.sum() == 0:
        #         # remove this idx from remain_idx
        #         remain_idx.remove(idx)
        #         continue
        
        # # 取local_idx的中间帧作为相似度目标帧
        # mididx = local_idx[(len(local_idx)+1)//2]
        # video_path = os.path.join(self.args['data_root'],
        #                               self.args['name'], 'JPEGImages',
        #                               f'{video_name}.zip')
        
        # target_img = TrainZipReader.imread(video_path, mididx).convert('RGB')
        # target_img = target_img.resize(self.size)
        
        # ref_imgs = []
        # for idx in remain_idx:
        #     img = TrainZipReader.imread(video_path, idx).convert('RGB')
        #     img = img.resize(self.size)
        #     ref_imgs.append(img)
        # # ref_imgs 对应 remain_idx 的顺序排列
        
        # # Similarity-based sampling step 2: select frames with high similarity
        # distance_list = []
        # for i in range(len(ref_imgs)):
        #     ref_img = ref_imgs[i]
        #     ref_img = np.asarray(ref_img)
        #     target_img = np.asarray(target_img)

        #     # 计算相似度，基于均值哈希算法
        #     hash1 = aHash(Image.fromarray(ref_img))
        #     hash2 = aHash(Image.fromarray(target_img))

        #     distance = hammingDistance(hash1, hash2)
        #     distance_list.append(distance)
        # # distance_list 对应 remain_idx 的顺序排列

        # ref_index = []
        # # 取distance_list中最小的元素的索引，对应remain_idx中的元素即为ref_index
        # for i in range(num_ref_frame):
        #     min_idx = distance_list.index(min(distance_list))
        #     ref_index.append(remain_idx[min_idx])
        #     distance_list[min_idx] = 1000000

        return local_idx + ref_index

    def load_item(self, index):
        video_name = self.video_names[index]
        # create masks
        # all_masks = create_random_shape_with_random_motion(
        #     self.video_dict[video_name], imageHeight=self.h, imageWidth=self.w) 
        
        # create sample index
        selected_index = self._sample_index(self.video_dict[video_name],
                                            self.num_local_frames,
                                            video_name,
                                            self.num_ref_frames)

        # read video frames
        frames = []
        masks = []
        corrupts = []
        for idx in selected_index:
            video_path = os.path.join(self.args['data_root'],
                                      self.args['name'], 'JPEGImages',
                                      f'{video_name}.zip')
            corr_video_path = os.path.join(self.args['data_root'],
                                           self.args['name'], 'BSCJPEGImages',
                                             f'{video_name}.zip')
            img = TrainZipReader.imread(video_path, idx).convert('RGB')
            corr_img = TrainZipReader.imread(corr_video_path, idx).convert('RGB')
            # if the imread result is None, then skip this frame
            if img is None:
                continue
            if corr_img is None:
                continue
            img = img.resize(self.size)
            corr_img = corr_img.resize(self.size)
            # masks.append(all_masks[idx])
            
            mask_path = os.path.join(self.args['data_root'], 
                                     self.args['name'], 'train_mask', 
                                     video_name, str(idx).zfill(5) + '.png')
            if not os.path.exists(mask_path):
                continue
            
            mask = Image.open(mask_path).resize(self.size,
                                                Image.NEAREST).convert('L')

            # origin: 0 indicates missing. now: 1 indicates missing
            mask = np.asarray(mask)
            m = np.array(mask > 0).astype(np.uint8)
            m = cv2.dilate(m,
                        cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3)),
                            iterations=4)
            mask = Image.fromarray(m*255)
            frames.append(img)
            masks.append(mask)
            corrupts.append(corr_img)

        # normalizate, to tensors
        frames = GroupRandomHorizontalFlip()(frames)
        corrupts = GroupRandomHorizontalFlip()(corrupts)
        frame_tensors = self._to_tensors(frames) * 2.0 - 1.0
        corrupt_tensors = self._to_tensors(corrupts) * 2.0 - 1.0
        mask_tensors = self._to_tensors(masks)
        return frame_tensors, mask_tensors, corrupt_tensors, video_name


class TestDataset(torch.utils.data.Dataset):
    def __init__(self, args):
        self.args = args
        self.size = self.w, self.h = args.size

        with open(os.path.join(args.data_root, args.dataset, 'test.json'),
                  'r') as f:
            self.video_dict = json.load(f)
        self.video_names = list(self.video_dict.keys())

        self._to_tensors = transforms.Compose([
            Stack(),
            ToTorchFormatTensor(),
        ])

    def __len__(self):
        return len(self.video_names)

    def __getitem__(self, index):
        item = self.load_item(index)
        return item

    def load_item(self, index):
        video_name = self.video_names[index]
        ref_index = list(range(self.video_dict[video_name]))

        # read video frames
        frames = []
        masks = []
        for idx in ref_index:
            video_path = os.path.join(self.args.data_root, self.args.dataset,
                                      'JPEGImages_test', f'{video_name}.zip')
            img = TestZipReader.imread(video_path, idx).convert('RGB')
            img = img.resize(self.size)
            frames.append(img)
            mask_path = os.path.join(self.args.data_root, self.args.dataset,
                                     'test_masks', video_name,
                                     str(idx).zfill(5) + '.png')
            mask = Image.open(mask_path).resize(self.size,
                                                Image.NEAREST).convert('L')
            # origin: 0 indicates missing. now: 1 indicates missing
            mask = np.asarray(mask)
            m = np.array(mask > 0).astype(np.uint8)
            m = cv2.dilate(m,
                           cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3)),
                           iterations=4)
            mask = Image.fromarray(m * 255)
            masks.append(mask)

        # to tensors
        frames_PIL = [np.array(f).astype(np.uint8) for f in frames]
        frame_tensors = self._to_tensors(frames) * 2.0 - 1.0
        mask_tensors = self._to_tensors(masks)
        return frame_tensors, mask_tensors, video_name, frames_PIL
