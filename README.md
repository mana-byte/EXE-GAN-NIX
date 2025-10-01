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


**NOTE**: This repo only uses a slightly modified version of the guided recovery. If you want all the other features please checkout the original repo

| Result (Not Real) | Real Image | Mask |
|-------------------|------------|------|
| [![Watch the video](https://raw.githubusercontent.com/mana-byte/EXE-GAN-NIX/main/example_result/Talking_example/recover_out/1_0_inpaint.png)](https://raw.githubusercontent.com/mana-byte/EXE-GAN-NIX/main/output.mp4) | <img width="256" height="256" alt="Real Image" src="https://github.com/user-attachments/assets/0849bab1-3afc-4fa2-9c7c-fc6f1e1e0c46" /> | <img width="256" height="256" alt="Mask" src="https://github.com/user-attachments/assets/1d36ca78-3544-4b4e-80c7-ba792ae502da" /> |


## Installation 

**YOU MUST HAVE CUDA INSTALLED**
**NOTE:** This project dependencies do not depend on me ([mana-byte](https://github.com/mana-byte)). If requirements.txt doesn't work you should checkout the original repo for troubleshooting. Using Nix in this case ensures that the project works on any machine as long as [Nix](https://nixos.org/) is installed (if the machine can support CUDA).

```
cd EXE-GAN project

nix develop # Install it the nix way

# OR

pip install -r requirements.txt # Install it the python way. If you use this you will need to install the CUDA drivers by yourself

```
- Note that other versions of PyTorch (e.g., higher than 1.7) also work well, but you have to install the corresponding CUDA version. 


## Exemplar-guided facial image recovery
#### Notice 
- For editing images from the web, photos should be aligned by face landmarks and cropped to 256x256 by [align_face](https://github.com/ZPdesu/Barbershop/blob/main/align_face.py).

(use our FFHQ_60k pre-trained model [EXE_GAN_model.pt](https://drive.google.com/file/d/1y7ThKBXL7QK7CPtvT3KICeNOu1T2xlCA/view?usp=drive_link) or trained *pt file by yourself.)

```bash
python guided_recovery.py --psp_checkpoint_path ./pre-train/psp_ffhq_encode.pt --ckpt  ./checkpoint/EXE_GAN_model.pt  --masked_dir ./imgs/exe_guided_recovery/mask --gt_dir ./imgs/exe_guided_recovery/target --exemplar_dir ./imgs/exe_guided_recovery/exemplar --sample_times 1 --video_output ./output.mp4 --eval_dir ./recover_out  
```

- masked_dir: mask input folder
- gt_dir: the input gt_dir, used for  editing 
- exemplar_dir: exemplar_dir, the exemplar dir, for guiding the editing
- eval_dir: output dir
- video_output: video output dir

---

## Use Guided facial image recovery with [VR HEADSET FILTER](https://github.com/mana-byte/VR-Headset-filter)

1. Install the two projects
2. Use in the VR HEADSET FILTER

```bash
python main.py --action frames --source_video ./video/test.mp4 # With the video you want
```
3. Gather all the frames from **video_frames/mask** and **video_frames/target** and move them into **imgs/exe_guided_recovery/mask** and **imgs/exe_guided_recovery/target**
4. Take a selfie/photo of the person's face that is present in the video and use [align_face](https://github.com/ZPdesu/Barbershop/blob/main/align_face.py) to align your face correctly
5. Place the aligned face into **imgs/exe_guided_recovery/examplar** and name it **1_exe.png**

6. Finally use in the EXE-GAN (Don't forget to install this project weight [EXE_GAN_model.pt](https://drive.google.com/file/d/1y7ThKBXL7QK7CPtvT3KICeNOu1T2xlCA/view?usp=drive_link)): 

```bash
python guided_recovery.py --psp_checkpoint_path ./pre-train/psp_ffhq_encode.pt --ckpt  ./checkpoint/EXE_GAN_model.pt  --masked_dir ./imgs/exe_guided_recovery/mask --gt_dir ./imgs/exe_guided_recovery/target --exemplar_dir ./imgs/exe_guided_recovery/exemplar --sample_times 1 --video_output ./output.mp4 --eval_dir ./recover_out  
```

7. Watch the output video ./output.mp4
