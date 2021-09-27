import os
import cv2
import glob
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--origin_video_path', type=str, default='E:\HDR_video\datasets\HLG_video\origin\\3840x2160', help='input origin video file')
    parser.add_argument('--video_60fps_5s_path', type=str, default='datasets\HLG_video\\video_60fps_5s', help='output normalize video(60fps 5s)file')
    parser.add_argument('--frame_num', type=int, default='40')
    args = parser.parse_args()
    
    video_foders = glob.glob(os.path.join(args.origin_video_path, '*'))
    for folder in video_foders:
        video_name = os.path.basename(folder) #with suffix
        cap = cv2.VideoCapture(folder)
        #获取原视频的尺寸
        if cap.isOpened():
            frames = cap.get(7)
            if frames < args.frame_num:
                print(f'{video_name}总帧数小于{args.frame_num}!!!')
                raise ValueError(f'frame_num必须大于{args.frame_num}')
        
        # 进入系统命令，用FFmpeg将HDR视频转为yuv，并保存在{video_60fps_5s_path}里
        os.makedirs(args.video_60fps_5s_path, exist_ok=True)
        tmp = os.path.join(args.video_60fps_5s_path,f'{video_name}')
        #判断该视频是否已经转换过了
        if os.path.exists(os.path.join(args.video_60fps_5s_path,f'{video_name}')):
            continue
        else:
            #video -> yuv60fps
            os.system(f'ffmpeg -i {folder} -vcodec copy -an -vframes {args.frame_num} {args.video_60fps_5s_path}\{video_name} -y')
        

if __name__ == '__main__':
    main()
