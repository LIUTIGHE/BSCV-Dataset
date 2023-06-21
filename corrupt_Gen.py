# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 13:23:55 2023

@author: LIU TIANYI
"""

import os
import binascii
import random
import re
import struct
import subprocess
from fractions import Fraction


# parameters
# GOP_size = 16
parser = argparse.ArgumentParser(description="CorruptionGenerator")
parser.add_argument("-P", "--prob", type=str, required=True)
parser.add_argument("-L", "--pos", type=str, required=True)
parser.add_argument("-S", "--len", type=str, required=True)
args = parser.parse_args()

corr_prob = int(args.prob)
corr_pos = float(args.pos)
corr_len = int(args.len)

def remove_ranges(data, ranges):
    ranges = sorted(ranges, reverse=True)
    for start, end in ranges:
        data_ = data[:start] + data[end:]
        # if length of data_ is odd, start from the next byte
        if len(data_) % 2 != 0:
            data_ = data[:start+1] + data[end+1:]
        data = data_    
    return data

for f in ['test', 'train']:
    for root, dirs, files in os.walk('./' + f + '/GT_h264/'):
        print('root:',root)
        print('dirs:',dirs)
        print('files:',files)
        print('\n')
        for filename in files:
            
            with open(root + filename, 'rb') as BS:
                hexBS = binascii.hexlify(BS.read())

            # Find all the location of content fragment
            startIndex = [a.start() for a in re.finditer(b'000001', hexBS)]
            header_index = [l.start() for l in re.finditer(b'00000167', hexBS)]
            I_index = [m.start() for m in re.finditer(b'00000165', hexBS)]
            P_index = [n.start() for n in re.finditer(b'00000141', hexBS)]
            B_index = [o.start() for o in re.finditer(b'00000101', hexBS)]
            frameIndexes = I_index + P_index + B_index
            startIndex.sort()
            frameIndexes.sort()
            
            # corruption occurs between each I-frame and next GOP header
            crpt_middle = []
            
            if len(I_index) > 2 and I_index [-2] > max(header_index):
                I_index = I_index[:-1]
            
            for i in I_index:
                # randomly select frames in this GOP
                print("In GOP starts with I-frame index: " + str(i))
                
                if i < max(I_index):
                    next_header_index = min(idx for idx in header_index if idx > i)
                    last_frame_in_GOP = max(idx for idx in frameIndexes if idx < next_header_index)
                    x_list = []
                    if len(frameIndexes[frameIndexes.index(i): frameIndexes.index(last_frame_in_GOP)+1]) < corr_prob:
                        corr_prob_ = len(frameIndexes[frameIndexes.index(i): frameIndexes.index(last_frame_in_GOP)+1])
                        x_list = random.sample(frameIndexes[frameIndexes.index(i): frameIndexes.index(last_frame_in_GOP)+1], corr_prob_) # randomly select n frame in this GOP
                    else:
                        x_list = random.sample(frameIndexes[frameIndexes.index(i): frameIndexes.index(last_frame_in_GOP)+1], corr_prob) # randomly select n frame in this GOP
                    
                    print("x_list: ", x_list)
                    # x = random.choice(frameIndexes[frameIndexes.index(i): frameIndexes.index(last_frame_in_GOP)+1])
                    for x in x_list:
                        y = min(idx for idx in startIndex if idx > x)
                        num = len(frameIndexes[frameIndexes.index(i): frameIndexes.index(last_frame_in_GOP)+1])
                        j = 0
                        while True:
                            if y-x > corr_len:
                                print("corruption occurs between " + str(x) + " and " + str(y))
                                # get corruption position (2048 Bytes)
                                es = int(y-x-7-corr_len)
                                print("possible error space (position): " + str(es) + "\n")
                                crpt_middle.append((int(x+7+es*corr_pos), int(x+7+es*corr_pos)+corr_len))
                                break
                            if j == num:
                                print("corruption occurs between " + str(x) + " and " + str(y))
                                # every frames in this GOP have too small fragment, we assume that the header is detected and fill the content by one byte
                                crpt_middle.append((int(x+9), int(y+1)))
                                break
                            else:
                                # look for other frames by sequence in the GOP with enought length
                                fi = frameIndexes[frameIndexes.index(i): frameIndexes.index(last_frame_in_GOP)+1]
                                x = fi[j]
                                y = min(idx for idx in startIndex if idx > x)
                                j = j + 1
            
                else:
                    x_list = []
                    # print(len(frameIndexes[frameIndexes.index(i):]))
                    if len(frameIndexes[frameIndexes.index(i):]) < corr_prob:
                        corr_prob_ = len(frameIndexes[frameIndexes.index(i):])
                        x_list = random.sample(frameIndexes[frameIndexes.index(i): ], corr_prob_) # randomly select n frame in this GOP
                    else:
                        x_list = random.sample(frameIndexes[frameIndexes.index(i): ], corr_prob) # randomly select n frame in this GOP

                    # x = random.choice(frameIndexes[frameIndexes.index(i):])
                    for x in x_list:
                        if x < max(frameIndexes): # not the last frame
                            y = min(idx for idx in startIndex if idx > x)
                        else:
                            y = len(hexBS)
                        
                        print("corruption occurs between " + str(x) + " and " + str(y))
                
                        # get corruption position (2048 Bytes)
                        es = int(y-x-7-corr_len)
                        print("possible error space (position): " + str(es) + "\n")
                        crpt_middle.append((int(x+7+es*corr_pos), int(x+7+es*corr_pos)+corr_len))
            
            crpt_middle.sort()
            
            #At the coruption location between the selected index and its next start code
            hexBS_new_middle = remove_ranges(hexBS, crpt_middle)
            print("corruption position: " + str(crpt_middle))
            # calculate the length difference between original and corrupted bitstream
            diff = len(hexBS) - len(hexBS_new_middle)
            print("length difference: " + str(diff))
            bi_hexBS_new_middle = binascii.unhexlify(hexBS_new_middle)

            # After corrupt each GOP, write the remained bitstream to file.
            if not os.path.exists(f + "_" + str(corr_prob) + str(int(corr_pos*10)) + str(corr_len)):
                os.makedirs(f + "_" + str(corr_prob) + str(int(corr_pos*10)) + str(corr_len))
                if not os.path.exists(f + "_" + str(corr_prob) + str(int(corr_pos*10)) + str(corr_len) + "/BSC_h264/"):
                    os.makedirs(f + "_" + str(corr_prob) + str(int(corr_pos*10)) + str(corr_len) + "/BSC_h264/")

            f_ = open(f + "_" + str(corr_prob) + str(int(corr_pos*10)) + str(corr_len) + "/BSC_h264/" + filename[:-5] + "_2" + filename[-5:], "wb")
            f_.write(bi_hexBS_new_middle)
            f_.close()
            print(f + "_" + str(corr_prob) + str(corr_pos*10) + str(corr_len) + "/BSC_h264/" + filename[:-5] + "_2" + filename[-5:])


# # Gen GT and BSC_JPEG
for a in ['_144096', '_124096', '_142048', '_244096']:

    for filename in os.listdir('train'+a+'/BSC_h264'):
        print(' ')
        print('files:',filename)
        if filename[-5:] == ".h264":
            if not os.path.exists("train"+a+"/BSC_JPEGImages/"):
                os.makedirs("train"+a+"/BSC_JPEGImages/")
            images_folder = 'train'+a+'/BSC_JPEGImages/' + filename[:-7] + '/'  
            if not os.path.exists(images_folder):
                os.makedirs(images_folder)
            cmd = 'ffmpeg -i train'+a+'/BSC_h264/' + filename + ' -start_number 0 -qscale:v 2 ' + images_folder + '%05d.jpg'
            print(cmd)
            subprocess.run(cmd, shell=True)

    for filename in os.listdir('test'+a+'/BSC_h264'):
        print(' ')
        print('files:',filename)
        if filename[-5:] == ".h264":
            if not os.path.exists("test"+a+"/BSC_JPEGImages/"):
                os.makedirs("test"+a+"/BSC_JPEGImages/")
            images_folder = 'test'+a+'/BSC_JPEGImages/' + filename[:-7] + '/'  
            if not os.path.exists(images_folder):
                os.makedirs(images_folder)
            cmd = 'ffmpeg -i test'+a+'/BSC_h264/' + filename + ' -start_number 0 -qscale:v 2 ' + images_folder + '%05d.jpg'
            print(cmd)
            subprocess.run(cmd, shell=True)
