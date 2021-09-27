import os
import shutil
import numpy as np
import cv2
import glob
import argparse
from yuv_io import YUVread_16bit,YUVwrite
from yuv2rgb import create_imgs_from_yuv


def yuvfps_extract(path, size, frame_num=None, start_frame=0, mode='420'):
    # 时间两倍下采样
    all_y, all_u, all_v = YUVread_16bit(path,size,frame_num,start_frame,mode)
    yfps_down_x2 = all_y[::2,:,:]
    ufps_down_x2 = all_u[::2,:,:]
    vfps_down_x2 = all_v[::2,:,:]
    return yfps_down_x2, ufps_down_x2, vfps_down_x2

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--video_path', type=str, default='E:\HDR_video\datasets\HLG_video\\video_60fps_5s', help='input video file')
    parser.add_argument('--yuv60fps_save_path', type=str, default='E:\HDR_video\datasets\HLG_video\yuv60tmp', help='save yuv path tmp')
    parser.add_argument('--video_scale', type=int, default=(2160,3840), help='input video size(h,w)')
    parser.add_argument('--frame_num', type=int, default=300, help='input video size(h,w)')
    parser.add_argument('--yuv30fps_save_path', type=str, default='G:\datasets\HLG\\4K\yuv30', help='save yuv30fps path')
    # parser.add_argument('--rgb30fps_save_path', type=str, default='datasets/HLG/rgb30/gt', help='save rgb30fps path')
    args = parser.parse_args()
    
    video_foders = glob.glob(os.path.join(args.video_path, '*'))
    for folder in video_foders:
        video_name = os.path.splitext(os.path.basename(folder))[0]
        cap = cv2.VideoCapture(folder)
        #获取原视频的尺寸
        if cap.isOpened():
            frames = cap.get(7)
            if frames < args.frame_num:
                print(f'{video_name}总帧数小于300!!!')
                raise ValueError('frame_num必须大于300')
        
        # 进入系统命令，用FFmpeg将HDR视频转为yuv，并保存在{yuv60fps_save_path}里
        os.makedirs(args.yuv60fps_save_path, exist_ok=True)
        os.makedirs(args.yuv30fps_save_path, exist_ok=True)
        #判断该视频是否已经转换过了
        if os.path.exists(os.path.join(args.yuv30fps_save_path,f'{video_name}.yuv')):
            continue
        else:
            #video -> yuv60fps
            os.system(f'ffmpeg -i {folder} {args.yuv60fps_save_path}/{video_name}.yuv -y')
            #从yuv60 提取 yuv30
            y, u, v = yuvfps_extract(f'{args.yuv60fps_save_path}/{video_name}.yuv', args.video_scale, frame_num=args.frame_num)
            #写入yuv30fps
            YUVwrite(y, u, v, os.path.join(args.yuv30fps_save_path, f'{video_name}.yuv'))
            shutil.rmtree(args.yuv60fps_save_path)
            # os.system(f'rm -r {args.yuv60fps_save_path}/{video_name}.yuv')
            #由yuv30fps -> rgb30
            # create_imgs_from_yuv(y, u, v, os.path.join(args.rgb30fps_save_path, video_name))

if __name__ == '__main__':
    main()
