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

## Dataset

![Tesear](teaser_v6_00.png)

### Property
- Multiple video resolution (240P, 480P, 720P)
- Realistic video degradation caused by bitstream corruption.
- Various unpredictable error pattern in different degree.
- Large-scale with over 17K video clips and 2M frames, 50% frames have corruption.
- ...

### Accessibility
For data download, it is in the process of project commitee reviewing, to be updated...



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
