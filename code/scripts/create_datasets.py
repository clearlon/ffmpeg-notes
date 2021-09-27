import os
import shutil
import numpy as np
import cv2
import glob
import argparse
from yuv_io import YUVread_16bit,Ywrite
from yuv2rgb import create_imgs_from_yuv
import matlab
import matlab.engine


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--origin_video_path', type=str, default='G:\datasets\HLG\origin', help='input origin video file')
    parser.add_argument('--video_clip', type=str, default='G:\datasets\HLG\\video_clip', help='output normalize video(60fps 5s)file')
    parser.add_argument('--frame_num', type=int, default='18')
    parser.add_argument('--video_frame_num', type=int, default='21')
    parser.add_argument('--video_size', type=int, default=(1080,1920), help='input video size(h,w)')
    parser.add_argument('--yuv_path', type=str, default='G:\datasets\HLG\yuv18', help='save yuv30fps path')
    parser.add_argument('--Y_gt_path', type=str, default='G:\datasets\HLG\Yframes\Y_gt', help='save ground-true of Y-frames path')
    parser.add_argument('--Y_lr_path', type=str, default='G:\datasets\HLG\Yframes\Y_lr', help='save low-resolution of Y-frames path')
    parser.add_argument('--imgs_gt_path', type=str, default='G:\datasets\HLG\\rgb18\\train_gt', help='save ground-true image path')
    parser.add_argument('--imgs_lr_path', type=str, default='G:\datasets\HLG\\rgb18\\train_lr', help='save low-resolution image path')
    parser.add_argument('--scale', type=int, default='4')
    parser.add_argument('--data_type', type=str, default='uint16')
    args = parser.parse_args()
    
    video_foders = glob.glob(os.path.join(args.origin_video_path, '*'))
    for folder in video_foders:
        # video_name = os.path.basename(folder) #with suffix
        video_name = os.path.splitext(os.path.basename(folder))[0] 
        cap = cv2.VideoCapture(folder)
        #extract frame number of origin video
        if cap.isOpened():
            weight = int(cap.get(3))
            height = int(cap.get(4))
            if (height, weight) != args.video_size:
                print(f'video size is {args.video_size}')
                raise ValueError(f'video {video_name} size is not 1080x1920')

            frames = cap.get(7)
            if frames < args.frame_num:
                print(f'{video_name}总帧数小于{args.frame_num}!!!')
                raise ValueError(f'frame_num必须大于{args.frame_num}')
        
        # 进入系统命令，用FFmpeg将HDR视频转为yuv，并保存在{video_clip}里
        os.makedirs(args.video_clip, exist_ok=True)
        os.makedirs(args.yuv_path, exist_ok=True)
        yuv_name = os.path.join(args.yuv_path, f'{video_name}.yuv')
        # video -> yuv60fps
        if not os.path.exists(os.path.join(args.video_clip,f'{video_name}.mp4')):
            os.system(f'ffmpeg -i {folder} -vcodec copy -an -vframes {args.video_frame_num} {args.video_clip}\{video_name}.mp4 -y')

        #create yuv 21 frame number
        if not os.path.exists(yuv_name):
            os.system(f'ffmpeg -i {args.video_clip}\{video_name}.mp4 {yuv_name} -y')

        #create Y_gt 18 frame number
        if not os.path.exists(os.path.join(args.Y_gt_path, f'{video_name}.yuv')):
            all_y, all_u, all_v = YUVread_16bit(yuv_name, args.video_size, args.frame_num, mode='420')
            Ywrite(all_y, os.path.join(args.Y_gt_path, f'{video_name}.yuv'))
        else:
            imgs_save_path = os.path.join(args.imgs_gt_path, video_name)
            if not os.path.exists(imgs_save_path):
                all_y, all_u, all_v = YUVread_16bit(yuv_name, args.video_size, args.frame_num, mode='420')
                create_imgs_from_yuv(all_y, all_u, all_v, imgs_save_path)
                
        #create rgb_gt
        imgs_save_path = os.path.join(args.imgs_gt_path, video_name)
        if not os.path.exists(imgs_save_path):
            create_imgs_from_yuv(all_y, all_u, all_v, imgs_save_path)

        #create y_lr
        #调用MATLAB程序下采样
        # os.makedirs(args.Y_lr_path, exist_ok=True)
        # tmp = matlab.double(all_y.tolist())
        # engine.y_downsample(tmp, args.video_size, args.frame_num, matlab.double([args.scale]), args.Y_lr_path, video_name, nargout=0)

        #create rgb_lr
        #调用MATLAB程序下采样
        if not os.path.exists(os.path.join(args.imgs_lr_path, video_name)):
            engine = matlab.engine.start_matlab()
            os.makedirs(os.path.join(args.imgs_lr_path, video_name), exist_ok=True)
            engine.rgb_downsample(args.imgs_gt_path, video_name, args.imgs_lr_path, matlab.double([args.scale]), args.data_type, nargout=0)


if __name__ == '__main__':
    main()
