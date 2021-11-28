import os
import glob
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--origin_video_path', type=str, default='G:\datasets\myYoutube\original_video\hdr_video', help='input origin video file')
    parser.add_argument('--save_frames_path', type=str, default='G:\datasets\myYoutube\\training_set\\train_hdr', help='')
    parser.add_argument('--flag', type=str, default='folder')
    args = parser.parse_args()
    
    if args.flag == 'folder':
        video_foders = glob.glob(os.path.join(args.origin_video_path, '00*'))
        for folder in video_foders:
            video_name = os.path.basename(folder).split('.')[0] 
            
            # 进入系统命令，用FFmpeg将HDR视频转为yuv，并保存在{save_frames_path}里
            os.makedirs(os.path.join(args.save_frames_path, video_name), exist_ok=True)
            
            os.system(f'ffmpeg -i {folder} -r 10 -f image2 {args.save_frames_path}\\{video_name}\\frame%3d.png')
    else:
        folder = args.origin_video_path
        video_name = os.path.basename(folder).split('.')[0]
        os.makedirs(os.path.join(args.save_frames_path, video_name), exist_ok=True)
        os.system(f'ffmpeg -i {folder} -r 10 -f image2 {args.save_frames_path}\\{video_name}\\frame%3d.png')

if __name__ == '__main__':
    main()
