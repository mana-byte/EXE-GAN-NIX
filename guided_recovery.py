# -*- coding: UTF-8 -*-
# coding=utf-8
import sys

# sys.path.append('./')
# print(sys.path)
# guided facial image recovery
import argparse
import math
import random
import os
from torch import nn, autograd
from torch.utils import data
from torchvision import utils
from tqdm import tqdm
from op.utils import mkdirs, delete_dirs, set_random_seed

import cv2

from img_load_util import *
from test import get_model

try:
    import wandb

except ImportError:
    wandb = None

from op import conv2d_gradfix


def data_sampler(dataset, shuffle, distributed):
    if distributed:
        return data.distributed.DistributedSampler(dataset, shuffle=shuffle)

    if shuffle:
        return data.RandomSampler(dataset)

    else:
        return data.SequentialSampler(dataset)


def requires_grad(model, flag=True):
    for p in model.parameters():
        p.requires_grad = flag


def accumulate(model1, model2, decay=0.999):
    par1 = dict(model1.named_parameters())
    par2 = dict(model2.named_parameters())

    for k in par1.keys():
        par1[k].data.mul_(decay).add_(par2[k].data, alpha=1 - decay)


def sample_data(loader):
    while True:
        for batch in loader:
            yield batch


def d_logistic_loss(real_pred, fake_pred):
    real_loss = F.softplus(-real_pred)
    fake_loss = F.softplus(fake_pred)

    return real_loss.mean() + fake_loss.mean()


def d_r1_loss(real_pred, real_img):
    with conv2d_gradfix.no_weight_gradients():
        (grad_real,) = autograd.grad(
            outputs=real_pred.sum(), inputs=real_img, create_graph=True
        )
    grad_penalty = grad_real.pow(2).reshape(grad_real.shape[0], -1).sum(1).mean()

    return grad_penalty


def g_nonsaturating_loss(fake_pred):
    loss = F.softplus(-fake_pred).mean()

    return loss


def g_path_regularize(fake_img, latents, mean_path_length, decay=0.01):
    noise = torch.randn_like(fake_img) / math.sqrt(
        fake_img.shape[2] * fake_img.shape[3]
    )
    (grad,) = autograd.grad(
        outputs=(fake_img * noise).sum(), inputs=latents, create_graph=True
    )
    path_lengths = torch.sqrt(grad.pow(2).sum(2).mean(1))

    path_mean = mean_path_length + decay * (path_lengths.mean() - mean_path_length)

    path_penalty = (path_lengths - path_mean).pow(2).mean()

    return path_penalty, path_mean.detach(), path_lengths


def make_noise(batch, latent_dim, n_noise, device):
    if n_noise == 1:
        return torch.randn(batch, latent_dim, device=device)

    noises = torch.randn(n_noise, batch, latent_dim, device=device).unbind(0)

    return noises


def mixing_noise(batch, latent_dim, prob, device):
    if prob > 0 and random.random() < prob:
        return make_noise(batch, latent_dim, 2, device)

    else:
        return [make_noise(batch, latent_dim, 1, device)]


def set_grad_none(model, targets):
    for n, p in model.named_parameters():
        if n in targets:
            p.grad = None


def get_random_index(tar_size, part_size):
    range_ = int(tar_size / part_size)

    index_y = random.randint(0, range_ - 1)
    index_x = random.randint(0, range_ - 1)

    return index_y, index_x


def crop_image_by_part(image, ind_y, ind_x, part_size):
    y_start = ind_y * part_size
    x_satrt = ind_x * part_size
    return image[:, :, y_start : y_start + part_size, x_satrt : x_satrt + part_size]


def get_mix_latent(infer_img, psp_embedding, lambda_=None):
    noise = mixing_noise(args.batch, args.latent, args.mixing, device)
    w_style = psp_embedding.get_style_mapping(noise)
    infer_embedding = psp_embedding.get_w_plus(infer_img)
    if lambda_ == None:
        lambda_ = random.random()
    infer_embedding = infer_embedding + lambda_ * (w_style - infer_embedding)

    return infer_embedding


def get_name_fromTime():
    import time

    time.sleep(1)
    time_now = int(round(time.time() * 1000))
    time_now = time.strftime("%Y%m%d%H%M%S", time.localtime(time_now / 1000))
    return time_now


if __name__ == "__main__":
    device = "cuda"

    parser = argparse.ArgumentParser(description="EXE-GAN guided facial image recovery")
    parser.add_argument(
        "--arch", type=str, default="exe_gan", help="models architectures ( exe_gan)"
    )
    parser.add_argument("--batch", type=int, default=1, help="batch sizes for each gpu")
    parser.add_argument(
        "--size", type=int, default=256, help="image sizes for the models"
    )
    parser.add_argument(
        "--psp_checkpoint_path",
        type=str,
        default="./pre-train/psp_ffhq_encode.pt",
        help="psp model pretrained model",
    )
    parser.add_argument(
        "--mixing", type=float, default=0.5, help="probability of latent code mixing"
    )
    parser.add_argument(
        "--ckpt",
        type=str,
        default="./checkpoint/EXE_GAN_model.pt",
        help="psp model pretrained model",
    )

    parser.add_argument(
        "--masked_dir",
        type=str,
        default="./imgs/exe_guided_recovery/mask",
        help=" the input  masked_dir ",
    )
    parser.add_argument(
        "--gt_dir",
        type=str,
        default="./imgs/exe_guided_recovery/target",
        help="the input gt_dir, used for  editing ",
    )
    parser.add_argument(
        "--exemplar_dir",
        type=str,
        default="./imgs/exe_guided_recovery/exemplar",
        help="exemplar_dir, the exemplar dir, for guiding the editing",
    )
    parser.add_argument(
        "--sample_times", type=int, default=10, help="image sizes for the models"
    )
    parser.add_argument(
        "--eval_dir",
        type=str,
        default="./recover_out",
        help="path to the output the generated images",
    )
    parser.add_argument(
        "--video_output",
        type=str,
        default="",
        help="path to the output video",
    )

    args = parser.parse_args()

    delete_dirs(args.eval_dir)
    mkdirs(args.eval_dir)

    set_random_seed(1)

    gt_post = ".png"
    mask_post = ".png"
    exe_post = ".png"
    # os.makedirs(out_root,exist_ok=True)
    gt_imgs = get_img_lists(args.gt_dir, gt_post)
    mask_imgs = get_img_lists(args.masked_dir, mask_post)
    exe_imgs = get_img_lists(args.exemplar_dir, exe_post)

    generator = get_model(args, model_path=args.ckpt, psp_path=args.psp_checkpoint_path)

    if args.video_output != "":
        output_video = cv2.VideoWriter(
            args.video_output,
            cv2.VideoWriter_fourcc(*"mp4v"),
            30,
            (args.size, args.size),
        )

    for i in tqdm(range(len(gt_imgs))):
        exe_img_ = load_img2tensor(exe_imgs[0], args.size).to(device)
        gt_img_ = load_img2tensor(gt_imgs[i], args.size).to(device)
        mask_ = load_mask2tensor(mask_imgs[i], args.size).to(device)

        ##get mask
        mask_01 = mask_
        name = str(os.path.basename(gt_imgs[i])).split("_")[0]
        for jj in range(args.sample_times):
            completed_img, _, infer_imgs, _ = generator.get_inherent_stoc(
                gt_img_, mask_01, infer_imgs=exe_img_
            )

            utils.save_image(
                completed_img.add(1).mul(0.5),
                f"{str(args.eval_dir)}/{name}_{jj}_inpaint.png",
                nrow=int(1),
            )
            if args.video_output != "":
                frame = (
                    completed_img.add(1)
                    .mul(0.5)
                    .squeeze(0)
                    .permute(1, 2, 0)
                    .cpu()
                    .detach()
                    .numpy()
                )
                frame = (frame * 255).astype("uint8")
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                output_video.write(frame)
    if args.video_output != "":
        output_video.release()
