# Do Inpainting Yourself: Generative Facial Inpainting Guided by Exemplars (EXE-GAN) 
# Neurocomputing 2025
Official PyTorch implementation of EXE-GAN, publised on [Neurocomputing](https://www.sciencedirect.com/science/article/pii/S0925231224017673?via%3Dihub).

[[Homepage]](https://longlongaaago.github.io/EXE-GAN/)
[[paper]](https://arxiv.org/abs/2202.06358)
[[demo_youtube]](https://www.youtube.com/watch?v=nNEc94hgjtk)
[[demo_bilibili]](https://www.bilibili.com/video/BV14V4y1s7rz/?share_source=copy_web&vd_source=6fb8e0068d30286602ee8ea389f82ce4)
[![Page Views Count](https://badges.toozhao.com/badges/01JDD9C9YS7EVK0PN0QB8CJH4Z/green.svg)](https://badges.toozhao.com/stats/01JDD9C9YS7EVK0PN0QB8CJH4Z "Get your own page views count badge on badges.toozhao.com")



<div style="text-align: justify"> We present EXE-GAN, a novel exemplar-guided facial inpainting framework using generative adversarial networks. Our
approach can not only preserve the quality of the input facial image but also complete the image with exemplar-like facial attributes.</div>

![Performance](./imgs/teaser.png)


**NOTE**: This repo only uses a slightly modified version of the guided recovery. If you want all the other feature please checkout the original repo

## Notice
Our paper has been published in a Neurocomputing Journal!!!  (28 Nov. 2024). 
This paper has been going through a three-year review process!!

Our paper was first released on Sun, 13 Feb 2022. 
We are thankful for the community's recognition and attention to our project.
We also recognized that there have been some great papers published after ours,
and we encourage you to check out their projects as well:
- [Paint by Example](https://arxiv.org/abs/2211.13227), [codes](https://github.com/Fantasy-Studio/Paint-by-Example) (released at Wed, 23 Nov 2022, CVPR 2023)
- [Reference-Guided Face Inpainting](https://arxiv.org/abs/2303.07014), [codes](https://github.com/wuyangluo/reffaceinpainting) (released at Mon, 13 Mar 2023, TCSVT 2023)
- [PATMAT](https://arxiv.org/abs/2304.06107), [codes](https://github.com/humansensinglab/PATMAT) (released at Wed, 12 Apr 2023, ICCV 2023)

## Requirements 
Must have nix installed.
```
cd EXE-GAN project

nix develop # Install it the nix way

# OR

pip install -r requirements.txt # Install it the python way. If you use this you will need to install the CUDA drivers by yourself

```
- Note that other versions of PyTorch (e.g., higher than 1.7) also work well, but you have to install the corresponding CUDA version. 

##### What we have released
- [x] Training and testing codes
- [x] Pre-trained models


## Exemplar-guided facial image recovery: This is used together with [VR HEADSET FILTER](https://github.com/mana-byte/VR-Headset-filter)
#### Notice 
- For editing images from the web, photos should be aligned by face landmarks and cropped to 256x256 by [align_face](https://github.com/ZPdesu/Barbershop/blob/main/align_face.py).

(use our FFHQ_60k pre-trained model [EXE_GAN_model.pt](https://drive.google.com/file/d/1y7ThKBXL7QK7CPtvT3KICeNOu1T2xlCA/view?usp=drive_link) or trained *pt file by yourself.)

```bash
python guided_recovery.py --psp_checkpoint_path ./pre-train/psp_ffhq_encode.pt
--ckpt  ./checkpoint/EXE_GAN_model.pt  --masked_dir ./imgs/exe_guided_recovery/mask --gt_dir ./imgs/exe_guided_recovery/target --exemplar_dir ./imgs/exe_guided_recovery/exemplar --sample_times 1 --video_output ./output.mp4
 --eval_dir ./recover_out  
```

- masked_dir: mask input folder
- gt_dir: the input gt_dir, used for  editing 
- exemplar_dir: exemplar_dir, the exemplar dir, for guiding the editing
- eval_dir: output dir
- video_output: video output dir

### Use this with [VR HEADSET FILTER](https://github.com/mana-byte/VR-Headset-filter)

1. Install the two projects
2. Use in the VR HEADSET FILTER

```bash
python main.py --action frames --source_video ./video/test.mp4 # With the video you want
```
3. Gather all the frames from **video_frames/mask** and **video_frames/target** and move them into **imgs/exe_guided_recovery/mask** and **imgs/exe_guided_recovery/target**
4. Take a selfie/photo of the person's face that is present in the video and use [align_face](https://github.com/ZPdesu/Barbershop/blob/main/align_face.py) to align your face correctly
5. Place the aligned face into **imgs/exe_guided_recovery/examplar** and name it **1_exe.png**

6. Finally use in the EXE-GAN:

```bash
python guided_recovery.py --psp_checkpoint_path ./pre-train/psp_ffhq_encode.pt
--ckpt  ./checkpoint/EXE_GAN_model.pt  --masked_dir ./imgs/exe_guided_recovery/mask --gt_dir ./imgs/exe_guided_recovery/target --exemplar_dir ./imgs/exe_guided_recovery/exemplar --sample_times 1 --video_output ./output.mp4
 --eval_dir ./recover_out  
```


## Editing masks by yourself 
![gen_mask](./imgs/Mask_gen.gif)

We also uploaded the mask editing tool. 
You can try this tool to generate your masks for editing.
> python mask_gui.py


## Bibtex
- If you find our code useful, please cite our paper:
  ```
  @article{LU2025128996,
    title = {Do inpainting yourself: Generative facial inpainting guided by exemplars},
    journal = {Neurocomputing},
    volume = {617},
    pages = {128996},
    year = {2025},
    issn = {0925-2312},
    doi = {https://doi.org/10.1016/j.neucom.2024.128996},
    url = {https://www.sciencedirect.com/science/article/pii/S0925231224017673},
    author = {Wanglong Lu and Hanli Zhao and Xianta Jiang and Xiaogang Jin and Yong-Liang Yang and Kaijie Shi},
    keywords = {Generative adversarial networks, Image generation, Image inpainting, Facial image inpainting},
    }
  
  @ARTICLE{FACEMUG,
    author={Lu, Wanglong and Wang, Jikai and Jin, Xiaogang and Jiang, Xianta and Zhao, Hanli},
    journal={IEEE Transactions on Visualization and Computer Graphics}, 
    title={FACEMUG: A Multimodal Generative and Fusion Framework for Local Facial Editing}, 
    year={2024},
    volume={},
    number={},
    pages={1-15},
    keywords={Facial features;Semantics;Codes;Generators;Image synthesis;Faces;Image color analysis;Generative adversarial networks;image-toimage translation;multimodal fusion;image editing;facial editing},
    doi={10.1109/TVCG.2024.3434386}}
  ```

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=LonglongaaaGo/EXE-GAN&type=Date)](https://star-history.com/#LonglongaaaGo/EXE-GAN&Date)

## Acknowledgements

Model details and custom CUDA kernel codes are from official repositories: https://github.com/NVlabs/stylegan2

Codes for Learned Perceptual Image Patch Similarity, LPIPS came from https://github.com/richzhang/PerceptualSimilarity

To match FID scores more closely to tensorflow official implementations, I have used FID Inception V3 implementations in https://github.com/mseitzer/pytorch-fid
