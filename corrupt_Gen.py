# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 13:23:55 2023

@author: HF-Tech
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
corr_prob = 1 # F: each frame has 1/16 probability to be corrupted, equally 1 frame per GOP
corr_pos = 0.4 # P: the position of corruption occurance in the frame, equally happens in 40% of the specific frame length
corr_len = 512*4 # L: 2048 Bytes (16 Kbits) packet loss length

def remove_ranges(data, ranges):
    ranges = sorted(ranges, reverse=True)
    for start, end in ranges:
        data_ = data[:start] + data[end:]
        # if length of data_ is odd, start from the next byte
        if len(data_) % 2 != 0:
            data_ = data[:start+1] + data[end+1:]
        data = data_    
    return data
'''
for f in ['test', 'train']:
    for root, dirs, files in os.walk('/media/tianyi/BSC-VideoCompletion/' + f + '/h264/'):
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
            
            # corruption occurs between each I-frame and next GOP header (i.e., one loss happens in each GOP's content)
            # crpt_front = []
            crpt_middle = []
            # crpt_back = []
            
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
                
                    # # get corruption position (2048 Bytes)
                    # es = int(y-x-7-1024*4)
                    # print("possible error space (position): " + str(es) + "\n")
                    # crpt_middle.append((int(x+7+es*0.4), int(x+7+es*0.4)+1024*4))
                    
                    # if y-x > 1024*4:
                    # # crpt_front.append((int(x+7+es*0.1), int(x+7+es*0.1)+1024*4))
                    #     crpt_middle.append((int(x+7+es*0.4), int(x+7+es*0.4)+1024*4))
                    # # crpt_back.append((int(x+7+es*0.7), int(x+7+es*0.7)+1024*4))
                    # else:
                    #     crpt_middle.append((int(x+7), int(y+1)))
                    #     # too small fragment, completely drop
            
            # crpt_front.sort()
            crpt_middle.sort()
            # crpt_back.sort()
            
            #At the coruption location between the selected index and its next start code
            # hexBS_new_front =remove_ranges(hexBS, crpt_front) # Lossless, 16 times larger bitstream
            hexBS_new_middle = remove_ranges(hexBS, crpt_middle)
            print("corruption position: " + str(crpt_middle))
            # calculate the length difference between original and corrupted bitstream
            diff = len(hexBS) - len(hexBS_new_middle)
            print("length difference: " + str(diff))
            # hexBS_new_back =remove_ranges(hexBS, crpt_back)
            # bi_hexBS_new_front = binascii.unhexlify(hexBS_new_front)
            bi_hexBS_new_middle = binascii.unhexlify(hexBS_new_middle)
            # bi_hexBS_new_back = binascii.unhexlify(hexBS_new_back)
            

            
            
            # After corrupt each GOP, write the remained bitstream to file.
            # f = open("E:\\DAVIS\\DAVIS-TrainVal_c\\" + filename[:-5] + "1" + filename[-5:], "wb")
            # f.write(bi_hexBS_new_front)
            # f.close()
            # print('\n' + filename + ': done')
            if not os.path.exists("/media/tianyi/BSC-VideoCompletion/" + f + "_" + str(corr_prob) + str(int(corr_pos*10)) + str(corr_len)):
                os.makedirs("/media/tianyi/BSC-VideoCompletion/" + f + "_" + str(corr_prob) + str(int(corr_pos*10)) + str(corr_len))
                if not os.path.exists("/media/tianyi/BSC-VideoCompletion/" + f + "_" + str(corr_prob) + str(int(corr_pos*10)) + str(corr_len) + "/BSC_h264/"):
                    os.makedirs("/media/tianyi/BSC-VideoCompletion/" + f + "_" + str(corr_prob) + str(int(corr_pos*10)) + str(corr_len) + "/BSC_h264/")

            f_ = open("/media/tianyi/BSC-VideoCompletion/" + f + "_" + str(corr_prob) + str(int(corr_pos*10)) + str(corr_len) + "/BSC_h264/" + filename[:-5] + "_2" + filename[-5:], "wb")
            f_.write(bi_hexBS_new_middle)
            f_.close()
            print("/media/tianyi/BSC-VideoCompletion/" + f + "_" + str(corr_prob) + str(corr_pos*10) + str(corr_len) + "/BSC_h264/" + filename[:-5] + "_2" + filename[-5:])
            
            # f_ = open("/media/tianyi/BSC-VideoCompletion/" + f + "_" + str(corr_prob) + str()44096/BSC_h264/" + filename[:-5] + "_2" + filename[-5:], "wb")
            # f_.write(bi_hexBS_new_middle)
            # f_.close()
            print(filename + ': done' + '\n\n')
            
            # f = open("E:\\DAVIS\\DAVIS-TrainVal_c\\" + filename[:-5] + "3" + filename[-5:], "wb")
            # f.write(bi_hexBS_new_back)
            # f.close()
            # print('\n' + filename + ': done')


for root, dirs, files in os.walk('/media/tianyi/BSC-VideoCompletion/+ f +/h264/'):
    print('root:',root)
    print('dirs:',dirs)
    print('files:',files)
    print('\n')
    for filename in files:
        print(filename)
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
        
        # corruption occurs between each I-frame and next GOP header (i.e., one loss happens in each GOP's content)
        # crpt_front = []
        crpt_middle = []
        # crpt_back = []
        
        if len(I_index) > 2 and I_index [-2] > max(header_index):
            I_index = I_index[:-1]
        print(I_index)
        for i in I_index:
            # randomly select a frame in this GOP
            print("In GOP starts with I-frame index: " + str(i))

            if i < max(I_index):
                print(header_index)
                next_header_index = min(idx for idx in header_index if idx > i)
                last_frame_in_GOP = max(idx for idx in frameIndexes if idx < next_header_index)
                x = random.choice(frameIndexes[frameIndexes.index(i): frameIndexes.index(last_frame_in_GOP)+1])
                y = min(idx for idx in startIndex if idx > x)
                num = len(frameIndexes[frameIndexes.index(i): frameIndexes.index(last_frame_in_GOP)+1])
                j = 0
                while True:
                    if y-x > 1024*4:
                        print("corruption occurs between " + str(x) + " and " + str(y))
                        # get corruption position (2048 Bytes)
                        es = int(y-x-7-1024*4)
                        print("possible error space (position): " + str(es) + "\n")
                        crpt_middle.append((int(x+7+es*0.4), int(x+7+es*0.4)+1024*4))
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
                x = random.choice(frameIndexes[frameIndexes.index(i):])
                if x < max(frameIndexes): # not the last frame
                    y = min(idx for idx in startIndex if idx > x)
                else:
                    y = len(hexBS)
                
                print("corruption occurs between " + str(x) + " and " + str(y))
        
                # get corruption position (2048 Bytes)
                es = int(y-x-7-1024*4)
                print("possible error space (position): " + str(es) + "\n")
                crpt_middle.append((int(x+7+es*0.4), int(x+7+es*0.4)+1024*4))
            
            # # get corruption position (2048 Bytes)
            # es = int(y-x-7-1024*4)
            # print("possible error space (position): " + str(es) + "\n")
            # crpt_middle.append((int(x+7+es*0.4), int(x+7+es*0.4)+1024*4))
            
            # if y-x > 1024*4:
            # # crpt_front.append((int(x+7+es*0.1), int(x+7+es*0.1)+1024*4))
            #     crpt_middle.append((int(x+7+es*0.4), int(x+7+es*0.4)+1024*4))
            # # crpt_back.append((int(x+7+es*0.7), int(x+7+es*0.7)+1024*4))
            # else:
            #     crpt_middle.append((int(x+7), int(y+1)))
            #     # too small fragment, completely drop
        
        # crpt_front.sort()
        crpt_middle.sort()
        # crpt_back.sort()
        
        #At the coruption location between the selected index and its next start code
        # hexBS_new_front =remove_ranges(hexBS, crpt_front) # Lossless, 16 times larger bitstream
        hexBS_new_middle =remove_ranges(hexBS, crpt_middle)
        # hexBS_new_back =remove_ranges(hexBS, crpt_back)
        # bi_hexBS_new_front = binascii.unhexlify(hexBS_new_front)
        bi_hexBS_new_middle = binascii.unhexlify(hexBS_new_middle)
        # bi_hexBS_new_back = binascii.unhexlify(hexBS_new_back)
        
        
        # After corrupt each GOP, write the remained bitstream to file.
        # f = open("E:\\DAVIS\\DAVIS-TrainVal_c\\" + filename[:-5] + "1" + filename[-5:], "wb")
        # f.write(bi_hexBS_new_front)
        # f.close()
        # print('\n' + filename + ': done')
        
        f = open("/media/tianyi/BSC-VideoCompletion/train/BSC_h264/" + filename[:-5] + "_2" + filename[-5:], "wb")
        f.write(bi_hexBS_new_middle)
        f.close()
        print('\n' + filename + ': done')
        
        # f = open("E:\\DAVIS\\DAVIS-TrainVal_c\\" + filename[:-5] + "3" + filename[-5:], "wb")
        # f.write(bi_hexBS_new_back)
        # f.close()
        # print('\n' + filename + ': done')


for root, dirs, files in os.walk('/media/tianyi/BSC-VideoCompletion/test/h264/'):
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
        
        # corruption occurs between each I-frame and next GOP header (i.e., one loss happens in each GOP's content)
        # crpt_front = []
        crpt_middle = []
        # crpt_back = []
        
        if len(I_index) > 2 and I_index [-2] > max(header_index):
            I_index = I_index[:-1]
        for i in I_index:
            # randomly select a frame in this GOP
            print("In GOP starts with I-frame index: " + str(i))

            if i < max(I_index):
                next_header_index = min(idx for idx in header_index if idx > i)
                last_frame_in_GOP = max(idx for idx in frameIndexes if idx < next_header_index)
                x = random.choice(frameIndexes[frameIndexes.index(i): frameIndexes.index(last_frame_in_GOP)+1])
                y = min(idx for idx in startIndex if idx > x)
                num = len(frameIndexes[frameIndexes.index(i): frameIndexes.index(last_frame_in_GOP)+1])
                j = 0
                while True:
                    if y-x > 1024*4:
                        print("corruption occurs between " + str(x) + " and " + str(y))
                        # get corruption position (2048 Bytes)
                        es = int(y-x-7-1024*4)
                        print("possible error space (position): " + str(es) + "\n")
                        crpt_middle.append((int(x+7+es*0.4), int(x+7+es*0.4)+1024*4))
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
                x = random.choice(frameIndexes[frameIndexes.index(i):])
                if x < max(frameIndexes): # not the last frame
                    y = min(idx for idx in startIndex if idx > x)
                else:
                    y = len(hexBS)
                
                print("corruption occurs between " + str(x) + " and " + str(y))
        
                # get corruption position (2048 Bytes)
                es = int(y-x-7-1024*4)
                print("possible error space (position): " + str(es) + "\n")
                crpt_middle.append((int(x+7+es*0.4), int(x+7+es*0.4)+1024*4))
            
            # # get corruption position (2048 Bytes)
            # es = int(y-x-7-1024*4)
            # print("possible error space (position): " + str(es) + "\n")
            # crpt_middle.append((int(x+7+es*0.4), int(x+7+es*0.4)+1024*4))
            
            # if y-x > 1024*4:
            # # crpt_front.append((int(x+7+es*0.1), int(x+7+es*0.1)+1024*4))
            #     crpt_middle.append((int(x+7+es*0.4), int(x+7+es*0.4)+1024*4))
            # # crpt_back.append((int(x+7+es*0.7), int(x+7+es*0.7)+1024*4))
            # else:
            #     crpt_middle.append((int(x+7), int(y+1)))
            #     # too small fragment, completely drop
        
        # crpt_front.sort()
        crpt_middle.sort()
        # crpt_back.sort()
        
        #At the coruption location between the selected index and its next start code
        # hexBS_new_front =remove_ranges(hexBS, crpt_front) # Lossless, 16 times larger bitstream
        hexBS_new_middle =remove_ranges(hexBS, crpt_middle)
        # hexBS_new_back =remove_ranges(hexBS, crpt_back)

        # bi_hexBS_new_front = binascii.unhexlify(hexBS_new_front)
        bi_hexBS_new_middle = binascii.unhexlify(hexBS_new_middle)
        # bi_hexBS_new_back = binascii.unhexlify(hexBS_new_back)
        
        
        # After corrupt each GOP, write the remained bitstream to file.
        # f = open("E:\\DAVIS\\DAVIS-TrainVal_c\\" + filename[:-5] + "1" + filename[-5:], "wb")
        # f.write(bi_hexBS_new_front)
        # f.close()
        # print('\n' + filename + ': done')
        
        f = open("/media/tianyi/BSC-VideoCompletion/test/BSC_h264/" + filename[:-5] + "_2" + filename[-5:], "wb")
        f.write(bi_hexBS_new_middle)
        f.close()
        print('\n' + filename + ': done')
        
        # f = open("E:\\DAVIS\\DAVIS-TrainVal_c\\" + filename[:-5] + "3" + filename[-5:], "wb")
        # f.write(bi_hexBS_new_back)
        # f.close()
        # print('\n' + filename + ': done')


# Gen valid GT and BSC_JPEG
for filename in os.listdir('/media/tianyi/BSC-VideoCompletion/valid/h264'):
    print('files:',filename)
    if filename[-5:] == ".h264":
        images_folder = '/media/tianyi/BSC-VideoCompletion/valid/JPEGImages/' + filename[:-5] + '/'  
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)
        cmd = 'ffmpeg -i /media/tianyi/BSC-VideoCompletion/valid/h264/' + filename + ' -start_number 0 -qscale:v 2 ' + images_folder + '%05d.jpg'
        subprocess.run(cmd, shell=True)

for filename in os.listdir('/media/tianyi/BSC-VideoCompletion/valid/BSC_h264'):
    print('files:',filename)
    if filename[-5:] == ".h264":
        images_folder = '/media/tianyi/BSC-VideoCompletion/valid/BSC_JPEGImages/' + filename[:-7] + '/'  
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)
        cmd = 'ffmpeg -i /media/tianyi/BSC-VideoCompletion/valid/BSC_h264/' + filename + ' -start_number 0 -qscale:v 2 ' + images_folder + '%05d.jpg'
        subprocess.run(cmd, shell=True)
'''
for a in ['_124096', '_142048', '_244096']:

    # # Gen train GT and BSC_JPEG
    # for filename in os.listdir('/media/tianyi/BSC-VideoCompletion/train'+a+'/h264'):
    #     print('files:',filename)
    #     if filename[-5:] == ".h264":
    #         images_folder = '/media/tianyi/BSC-VideoCompletion/train/JPEGImages/' + filename[:-5] + '/' 
    #         if not os.path.exists(images_folder):
    #             os.makedirs(images_folder)
    #         cmd = 'ffmpeg -i /media/tianyi/BSC-VideoCompletion/train/h264/' + filename + ' -start_number 0 -qscale:v 2 ' + images_folder + '%05d.jpg'
    #         subprocess.run(cmd, shell=True)

    for filename in os.listdir('/media/tianyi/BSC-VideoCompletion/train'+a+'/BSC_h264'):
        print(' ')
        print('files:',filename)
        if filename[-5:] == ".h264":
            if not os.path.exists("/media/tianyi/BSC-VideoCompletion/train"+a+"/BSC_JPEGImages/"):
                os.makedirs("/media/tianyi/BSC-VideoCompletion/train"+a+"/BSC_JPEGImages/")
            images_folder = '/media/tianyi/BSC-VideoCompletion/train'+a+'/BSC_JPEGImages/' + filename[:-7] + '/'  
            if not os.path.exists(images_folder):
                os.makedirs(images_folder)
            cmd = 'ffmpeg -i /media/tianyi/BSC-VideoCompletion/train'+a+'/BSC_h264/' + filename + ' -start_number 0 -qscale:v 2 ' + images_folder + '%05d.jpg'
            print(cmd)
            subprocess.run(cmd, shell=True)


    # # Gen test GT and BSC_JPEG
    # for filename in os.listdir('/media/tianyi/BSC-VideoCompletion/test/h264'):
    #     print('files:',filename)
    #     if filename[-5:] == ".h264":
    #         images_folder = '/media/tianyi/BSC-VideoCompletion/test/JPEGImages/' + filename[:-5] + '/' 
    #         if not os.path.exists(images_folder):
    #             os.makedirs(images_folder)
    #         cmd = 'ffmpeg -i /media/tianyi/BSC-VideoCompletion/test/h264/' + filename + ' -start_number 0 -qscale:v 2 ' + images_folder + '%05d.jpg'
    #         subprocess.run(cmd, shell=True)

    for filename in os.listdir('/media/tianyi/BSC-VideoCompletion/test'+a+'/BSC_h264'):
        print(' ')
        print('files:',filename)
        if filename[-5:] == ".h264":
            if not os.path.exists("/media/tianyi/BSC-VideoCompletion/test"+a+"/BSC_JPEGImages/"):
                os.makedirs("/media/tianyi/BSC-VideoCompletion/test"+a+"/BSC_JPEGImages/")
            images_folder = '/media/tianyi/BSC-VideoCompletion/test'+a+'/BSC_JPEGImages/' + filename[:-7] + '/'  
            if not os.path.exists(images_folder):
                os.makedirs(images_folder)
            cmd = 'ffmpeg -i /media/tianyi/BSC-VideoCompletion/test'+a+'/BSC_h264/' + filename + ' -start_number 0 -qscale:v 2 ' + images_folder + '%05d.jpg'
            print(cmd)
            subprocess.run(cmd, shell=True)
