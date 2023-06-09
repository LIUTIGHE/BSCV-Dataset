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

## Dataset

![Tesear](teaser_v6_00.png)

For each video, under various parameter setting, we provide differently corrupted videos (from left to right: ``(P, L, S) = (1/16, 0.4, 2048), (1/16, 0.4, 4096), (1/16, 0.2, 4096), and (2/16, 0.4, 4096)``, respectively. The explanation of the parameter will be explained below/in paper.).
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
    <td><img src="GIF/bmx-bumps_142048.gif" alt="GIF 1" width="180"/></td>
    <td><img src="GIF/bmx-bumps_144096.gif" alt="GIF 2" width="180"/></td>
    <td><img src="GIF/bmx-bumps_124096.gif" alt="GIF 3" width="180"/></td>
    <td><img src="GIF/bmx-bumps_244096.gif" alt="GIF 4" width="180"/></td>
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
    <td><img src="GIF/mascot_142048.gif" alt="GIF 1" width="180"/></td>
    <td><img src="GIF/mascot_144096.gif" alt="GIF 2" width="180"/></td>
    <td><img src="GIF/mascot_124096.gif" alt="GIF 3" width="180"/></td>
    <td><img src="GIF/mascot_244096.gif" alt="GIF 4" width="180"/></td>
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

### Property
- Flexible video resolution setting (240P, 480P, 720P)
- Realistic video degradation caused by bitstream corruption.
- Various unpredictable error pattern in different degree.
- With over 17K video clips and 2M frames, 50% frames have corruption.
- ...

### Download
For dataset downloading, please check this [link](https://entuedu-my.sharepoint.com/:f:/g/personal/liut0038_e_ntu_edu_sg/Egn7Xygv7UJBilL9z3nFo_4Bm5LdeoXCv-uiDo3qANsmTw?e=fMU9gZ) (About 1T).

### Extraction
We have seperated the dataset into training and testing set and for each branch. 
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
|-train_144096                    # Branch_144096
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
|-train_142048                    # The following branch has the same structure, without GT data only
|  |-BSC_h264
|  |-BSC_JPEGImages
|  |-masks       
|  |-Diff
|-train_124096
|  |-BSC_h264
|  |-BSC_JPEGImages
|  |-masks       
|  |-Diff
|-train_244096
|  |-BSC_h264
|  |-BSC_JPEGImages
|  |-masks       
|  |-Diff         
```

### Extension
We proposed a parameter model for generating bitstream corruption and therefore causing arbitrarily corrupted videos, even additional branches. 
![Param_Model](extend_fig.png)
You can use the provided program with your parameter combination to generate arbitrary branches based on the GOP size 16 as our setting, by the following commands, e.g.
```
python corrpt_Gen.py --prob 1 --pos 0.4 --size 4096 
```
Please use integer for ``prob`` and ``size``, and float for ``pos`` due to the limitation of our current experimental setting. 
If you want to adjust the GOP size, please refer to FFmpeg's instruction to recoding the frame sequence in folder ``GT_JPEGImages`` of branch ``_144096``.

## Experimental Setup
### FFmpeg Installation
We adopt FFmpeg as our video codec, please refer to the official guide line for your ffmpeg installation.

PS: It seems the working principle is different between Linux and Windows version of Linux since we have some lost-frame error in decoding on Linux but the same bitstream is fine on Windows. So we recommend using Windows FFmpeg to repair the frame loss issue if you are generating new branches. 

### Environmental Setting for Evaluation
For evaluation, we provide all environment configurations in ``requirements.txt``.

```bash
$ conda create -n BSCVI python=3.7
$ pip install -r requirements.txt
```

<!-- 
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
