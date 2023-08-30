# BSCV-Dataset
<!-- 
<p align="left">
    <a href=''>
      <img src='https://img.shields.io/badge/Paper-arXiv-green?style=plastic&logo=arXiv&logoColor=green' alt='Paper arXiv'>
    </a>
    <a href=''>
      <img src='https://img.shields.io/badge/Paper-PDF-red?style=plastic&logo=adobeacrobatreader&logoColor=red' alt='Paper PDF'>
    </a>
</p> -->

<!-- This repo contains code for our paper:

[Bitstream-corrupted Video Recovery: A Novel Benchmark Dataset and Method]()

[Tianyi Liu](), [Kejun Wu](), [Yi Wang](), [Wenyang Liu](), [Kim-Hui Yap](), [Lap-Pui Chau]() -->

(This page is under construction)


## Update
### 8.29

1. We shared our proposed video recovery method and evaluation results in the [method](https://github.com/LIUTIGHE/BSCV-Dataset/edit/main/README.md#824) part.

2. We provide preliminary comparison between our method and non-end-to-end video inpainting methods, the recovered video is illustrated to demonstrate our method's advantage.

### 8.24

1. New YouTube-VOS&DAVIS branches will soon be released with tougher parameter adjustments and corruption ratios.

2. New subset with higher resolutions in 1080P and 4K is included.

3. H.265 protocol is supported, uploading of mentioned subset and branches is in progress due to size and network speed.


## Dataset

![Tesear](teaser_v9.png)

For each video in YouTubeVOS&DAVIS subset, under various parameter setting, we provide differently corrupted videos (from left to right: ``(P, L, S) = (1/16, 0.4, 2048), (1/16, 0.4, 4096), (1/16, 0.2, 4096), (2/16, 0.4, 4096)``, and **additional** ``(1/16, 0.4, 8192), (1/16, 0.8, 4096), (4/16, 0.4, 4096)`` branches , respectively. The explanation of the parameter will be explained below/in paper.).
<!-- 
<table>
  <tr>
    <td><img src="GIF/1e0c2e54f2_142048.gif" alt="GIF 1" width="180"/></td>
    <td><img src="GIF/1e0c2e54f2_144096.gif" alt="GIF 2" width="180"/></td>
    <td><img src="GIF/1e0c2e54f2_124096.gif" alt="GIF 3" width="180"/></td>
    <td><img src="GIF/1e0c2e54f2_244096.gif" alt="GIF 4" width="180"/></td>
  </tr>
</table>
<table>
  <tr>
    <td><img src="GIF/1e0c2e54f2_142048_rec.gif" alt="GIF 1" width="180"/></td>
    <td><img src="GIF/1e0c2e54f2_144096_rec.gif" alt="GIF 2" width="180"/></td>
    <td><img src="GIF/1e0c2e54f2_124096_rec.gif" alt="GIF 3" width="180"/></td>
    <td><img src="GIF/1e0c2e54f2_244096_rec.gif" alt="GIF 4" width="180"/></td>
  </tr>
</table>
-->
<table>
  <tr>
    <td><img src="GIF/bmx-bumps_142048.gif" alt="GIF 1" width="180"/></td>
    <td><img src="GIF/bmx-bumps_144096.gif" alt="GIF 2" width="180"/></td>
    <td><img src="GIF/bmx-bumps_124096.gif" alt="GIF 3" width="180"/></td>
    <td><img src="GIF/bmx-bumps_244096.gif" alt="GIF 4" width="180"/></td>
  </tr>
</table>
<table>
  <tr>
    <td><img src="GIF/bmx-bumps_142048_rec.gif" alt="GIF 1" width="180"/></td>
    <td><img src="GIF/bmx-bumps_144096_rec.gif" alt="GIF 2" width="180"/></td>
    <td><img src="GIF/bmx-bumps_124096_rec.gif" alt="GIF 3" width="180"/></td>
    <td><img src="GIF/bmx-bumps_244096_rec.gif" alt="GIF 4" width="180"/></td>
  </tr>
</table>
<table>
  <tr>
    <td><img src="GIF/camel_142048.gif" alt="GIF 1" width="180"/></td>
    <td><img src="GIF/camel_144096.gif" alt="GIF 2" width="180"/></td>
    <td><img src="GIF/camel_124096.gif" alt="GIF 3" width="180"/></td>
    <td><img src="GIF/camel_244096.gif" alt="GIF 4" width="180"/></td>
  </tr>
</table>
<table>
  <tr>
    <td><img src="GIF/camel_142048_rec.gif" alt="GIF 1" width="180"/></td>
    <td><img src="GIF/camel_144096_rec.gif" alt="GIF 2" width="180"/></td>
    <td><img src="GIF/camel_124096_rec.gif" alt="GIF 3" width="180"/></td>
    <td><img src="GIF/camel_244096_rec.gif" alt="GIF 4" width="180"/></td>
  </tr>
</table>
<table>
  <tr>
    <td><img src="GIF/mascot_142048.gif" alt="GIF 1" width="180"/></td>
    <td><img src="GIF/mascot_144096.gif" alt="GIF 2" width="180"/></td>
    <td><img src="GIF/mascot_124096.gif" alt="GIF 3" width="180"/></td>
    <td><img src="GIF/mascot_244096.gif" alt="GIF 4" width="180"/></td>
  </tr>
</table>
<table>
  <tr>
    <td><img src="GIF/mascot_142048_rec.gif" alt="GIF 1" width="180"/></td>
    <td><img src="GIF/mascot_144096_rec.gif" alt="GIF 2" width="180"/></td>
    <td><img src="GIF/mascot_124096_rec.gif" alt="GIF 3" width="180"/></td>
    <td><img src="GIF/mascot_244096_rec.gif" alt="GIF 4" width="180"/></td>
  </tr>
</table>
<table>
  <tr>
    <td><img src="GIF/tennis_142048.gif" alt="GIF 1" width="180"/></td>
    <td><img src="GIF/tennis_144096.gif" alt="GIF 2" width="180"/></td>
    <td><img src="GIF/tennis_124096.gif" alt="GIF 3" width="180"/></td>
    <td><img src="GIF/tennis_244096.gif" alt="GIF 4" width="180"/></td>
  </tr>
</table>
<table>
  <tr>
    <td><img src="GIF/tennis_142048_rec.gif" alt="GIF 1" width="180"/></td>
    <td><img src="GIF/tennis_144096_rec.gif" alt="GIF 2" width="180"/></td>
    <td><img src="GIF/tennis_124096_rec.gif" alt="GIF 3" width="180"/></td>
    <td><img src="GIF/tennis_244096_rec.gif" alt="GIF 4" width="180"/></td>
  </tr>
</table>

### Property
- Flexible video resolution setting (480P, 720P, 1080P, 4K)
- Realistic video degradation caused by bitstream corruption.
- Various unpredictable error pattern in different degree.
- With about 30K video clips and 3.5M frames, 50% frames have corruption.
- ...

### Download
For dataset downloading, please check this [link](https://entuedu-my.sharepoint.com/:f:/g/personal/liut0038_e_ntu_edu_sg/Egn7Xygv7UJBilL9z3nFo_4Bm5LdeoXCv-uiDo3qANsmTw?e=fMU9gZ) (Extension for higher resolution, more parameter combination, and uploading are in progress).

### Extraction
We have seperated the dataset into training and testing set and for each branch in YouTube-VOS&DAVIS.
YouTube-UGC 1080P subset and Videezy4K 4K subset (for testing).
After downloading the ``.tar.gz`` files, please firstly restore the original ``.tar.gz`` files, unzipping the archives and formatting the folders by
```
$ bash format.sh
```

After the data preparation, ffmpeg encoded orignial (GT) video bitstream is provided in the ``_144096`` branch with folder name ``GT_h264`` and its decoded frame sequence with corruption is provided in the folder named ``GT_JPEGImages``.
We also provide the h264 bitstreams of each video and their decoded frame sequence as commonlu used video dataset.
Additionally, the mask sequence which is used for corruption region indication is provided in the ``masks`` folder in each branch, the files are structured as following:
```
BSCV-Dataset
|-scripts                         # Codes for dataset construction
|-YouTube-VOS&DAVIS
| |-train_144096                    # Branch_144096
|  |-GT_h264
|    |-##########.h264            # H.264 video bitstream with original id in YouTube-VOS dataset
|    |-...                        # 3,471 bitstream files in total
|  |-GT_JPEGImages
|    |-##########                 # Corresponding video ID
|      |-00000.jpg                # Decoded frame sequence with different length
|      |-...
|    |-...                        # 3,471 frame sequence folder in total
|  |-BSC_h264                     # Corresponding corrupted bitstream
|    |-##########_2.h264          
|    |-...                        
|  |-BSC_JPEGImages               # Corresponding decoded corrupted frame sequence
|    |-##########
|      |-00000.jpg              
|      |-...
|    |-...
|  |-masks                        # Corresponding mask sequence
|    |-##########
|      |-00000.png
|      |-...
|    |-...         
|  |-Diff                         # The binary difference map for mask geneartion by morphological operations
|    |-##########
|      |-00000.png
|      |-...
|    |-...
| |-train_142048                    # The following branch has the same structure, without GT data only
|  |-BSC_h264
|  |-BSC_JPEGImages
|  |-masks       
|  |-Diff      
| |...
|-YouTube-UGC-1080P
| |-FHD
| |-FHD_124096
|  |-GT_h264       
|  |-GT_JPEGImages
|  |-BSC_h264
|  |-BSC_JPEGImages
|  |-masks       
|  |-Diff
| |...
|-Videezy4K-4K
| |-QHD
|  |-GT_h264       
|  |-GT_JPEGImages
|  |-BSC_h264
|  |-BSC_JPEGImages
|  |-masks       
|  |-Diff
```

### Extension
We adopt FFmpeg as our video codec, please refer to the official guide line for your ffmpeg installation.

We proposed a parameter model for generating bitstream corruption and therefore causing arbitrarily corrupted videos, even additional branches. 
![Param_Model](extend_fig.png)

You can use the provided program with your parameter combination to generate arbitrary branches based on the GOP size 16 as our setting, by the following commands, e.g.
```
python corrpt_Gen.py --prob 1 --pos 0.4 --size 4096 
```
Please use integer for ``prob`` and ``size``, and float for ``pos`` due to the limitation of our current experimental setting. 
If you want to adjust the GOP size, please refer to FFmpeg's instruction to recoding the frame sequence in folder ``GT_JPEGImages`` of branch ``_144096``.

PS: It seems the working principle is different between Linux and Windows version of FFmpeg since we have some practical lost-frame error in decoding on Linux but the same bitstream is fine on Windows. So we recommend using FFmpeg on windows to deal with the lost frame issue if you are generating new branches. 

## Method

We propose a recovery framework based on end to end video inpainting method while leveraging the partial contents in the corrupted region, and we achieved better recovery quality compared with existing SOTA video inpainting methods.
![Method](Fig/Overview_v6.png)

![Eval](Fig/quantitative.png)

![Vis](Fig/qualitative.png)

For additional comparison with non-end-to-end methods, our preliminary evaluation result is
| Method | PSNR $\uparrow$ | SSIM $\uparrow$ | LPIPS $\downarrow$ | VFID $\downarrow$ | Runtime |
| ------ | ------ | ------ | ------ | ------ | ------ |
| FGT[2] | **31.5407** | 0.8967 | 0.0486 | 0.3368 | ~1.97 |
| ECFVI[1] | 20.8676 | 0.7692 | 0.0705 | 0.3019 | ~2.24 |
| **BSCVR-S (Ours)** | 28.8288 | ***0.9138*** | ***0.0399*** | **0.1704** | **0.172** |
| **BSCVR-P (Ours)** | ***29.0186*** | **0.9166** | **0.0391** | ***0.1730*** | ***0.178*** |

Recovery results in the form of video is illustrated below, from left to right, top to down is Corrupted Video, Mask Input, Ground Truth, FGT, ECFVI, and Our method in sequence.

<!--
<p align="center">
  <img src="GIF/mascot_input.gif" alt="Image 1" width="160" height="90"/>
  <img src="GIF/mascot_mask.gif" alt="Image 2" width="160" height="90"/>
  <img src="GIF/mascotpretrain_FGT.gif" alt="Image 3" width="160" height="90"/>
  <img src="GIF/mascotpretrain_ECFVI.gif" alt="Image 4" width="160" height="90"/>
  <img src="GIF/mascotbsctrain_BSCVI_S.gif" alt="Image 5" width="160" height="90"/>
  <img src="GIF/mascot_gt.gif" alt="Image 6" width="160" height="90"/>
</p>

<p align="center">
  <img src="GIF/walking_input.gif" alt="Image 1" width="160" height="90"/>
  <img src="GIF/walking_mask.gif" alt="Image 2" width="160" height="90"/>
  <img src="GIF/walkingpretrain_FGT.gif" alt="Image 3" width="160" height="90"/>
  <img src="GIF/walkingpretrain_ECFVI.gif" alt="Image 4" width="160" height="90"/>
  <img src="GIF/walkingbsctrain_BSCVI_S.gif" alt="Image 5" width="160" height="90"/>
  <img src="GIF/walking_gt.gif" alt="Image 6" width="160" height="90"/>
</p>

<p align="center">
  <img src="GIF/tennis_input.gif" alt="Image 1" width="160" height="90"/>
  <img src="GIF/tennis_mask.gif" alt="Image 2" width="160" height="90"/>
  <img src="GIF/tennispretrain_FGT.gif" alt="Image 3" width="160" height="90"/>
  <img src="GIF/tennispretrain_ECFVI.gif" alt="Image 4" width="160" height="90"/>
  <img src="GIF/tennisbsctrain_BSCVI_S.gif" alt="Image 5" width="160" height="90"/>
  <img src="GIF/tennis_gt.gif" alt="Image 6" width="160" height="90"/>
</p>
-->

<p align="center">
  <img src="GIF/mascot_input.gif" alt="Image 1" width="272" height="153"/>
  <img src="GIF/mascot_mask.gif" alt="Image 2" width="272" height="153"/>
  <img src="GIF/mascot_gt.gif" alt="Image 6" width="272" height="153"/>
  <img src="GIF/mascotpretrain_FGT.gif" alt="Image 3" width="272" height="153"/>
  <img src="GIF/mascotpretrain_ECFVI.gif" alt="Image 4" width="272" height="153"/>
  <img src="GIF/mascotbsctrain_BSCVI_S.gif" alt="Image 5" width="272" height="153"/>
</p>

<p align="center">
  <img src="GIF/walking_input.gif" alt="Image 1" width="272" height="153"/>
  <img src="GIF/walking_mask.gif" alt="Image 2" width="272" height="153"/>
  <img src="GIF/walking_gt.gif" alt="Image 6" width="272" height="153"/>
  <img src="GIF/walkingpretrain_FGT.gif" alt="Image 3" width="272" height="153"/>
  <img src="GIF/walkingpretrain_ECFVI.gif" alt="Image 4" width="272" height="153"/>
  <img src="GIF/walkingbsctrain_BSCVI_S.gif" alt="Image 5" width="272" height="153"/>
</p>

<p align="center">
  <img src="GIF/tennis_input.gif" alt="Image 1" width="272" height="153"/>
  <img src="GIF/tennis_mask.gif" alt="Image 2" width="272" height="153"/>
  <img src="GIF/tennis_gt.gif" alt="Image 6" width="272" height="153"/>
  <img src="GIF/tennispretrain_FGT.gif" alt="Image 3" width="272" height="153"/>
  <img src="GIF/tennispretrain_ECFVI.gif" alt="Image 4" width="272" height="153"/>
  <img src="GIF/tennisbsctrain_BSCVI_S.gif" alt="Image 5" width="272" height="153"/>
</p>


The code for our method, experimental setup, and evaluation scripts will be released soon after packaging and checking.

<!-- 
## Experimental Setup

### Environmental Setting for Evaluation
For evaluation, we provide all environment configurations in ``requirements.txt``.

```bash
$ conda create -n BSCVI python=3.7
$ pip install -r requirements.txt
```



## Citation
If you find our paper and/or code helpful, please consider citing:
```
@inproceedings{,
    title = {},
    author = {},
    booktitle = {},
    year = {}
}
```

## Acknowledgement
-->
