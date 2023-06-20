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

[Bitstream-corrupted Video Recovery: Benchmark Dataset and Method]()

[Tianyi Liu](), [Kejun Wu](), [Yi Wang](), [Wenyang Liu](), [Kim-Hui Yap](), [Lap-Pui Chau]() -->

(This page is under construction)

## Dataset

![Tesear](teaser_v6_00.png)

### Property
- Flexible video resolution setting (240P, 480P, 720P)
- Realistic video degradation caused by bitstream corruption.
- Various unpredictable error pattern in different degree.
- With over 17K video clips and 2M frames, 50% frames have corruption.
- ...

### Download
For dataset downloading, please check this [link](https://entuedu-my.sharepoint.com/:f:/g/personal/liut0038_e_ntu_edu_sg/Egn7Xygv7UJBilL9z3nFo_4Bm5LdeoXCv-uiDo3qANsmTw?e=fMU9gZ) (Upload in progress).

### Data Extraction
We have seperated the dataset into training and testing set and for each branch. 
After downloading the .tar.gz files, please firstly restore the original .tar.gz file of the 144096 branch of the training set and do data extraction and basic formatting by the following script.
```
.sh
concat xxx
```

After the prepration, ffmpeg encoded orignial (GT) video bitstream is provided in the _144096 branch with folder name "GT_h264" and the decoded frame sequence is provided in the folder named "JPEGImages" 
We provide the encoded h264 bitstream of each video and its decoded frame sequence as common video dataset

### Arbitrary Extension
Our proposed parameter model for generating bitstream corruption and therefore generating corrupted videos can be used to generate additional

## Experimental Setup
We provide all environment configurations in ``requirements.txt``.

```bash
$ conda create -n BSCVI python=3.7
$ pip install -r requirements.txt
```

<!-- Similar CUDA version should also be acceptable with corresponding version control for ``torch`` and ``torchvision``.
We refer the authors to [Generation](generation/README.md) and [Experiment](baselines/README.md) for details on quetsion-answer
generation, balancing, data split, and baseline experiments. For these two functionalities, please checkout the corresponding
sub-directory for code and instructions. -->

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
