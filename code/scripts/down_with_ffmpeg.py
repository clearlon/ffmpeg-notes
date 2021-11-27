import os
import glob


input_path = '/Users/unbelievable/iCloudDrive/Desktop/龙/研究生学习/HDR视频/oHDR_video'
video_list = sorted(glob.glob(os.path.join(input_path, '*')))
output_dir = '/Users/unbelievable/iCloudDrive/Desktop/龙/研究生学习/HDR视频/oLR_video'

num_videos = len(video_list)
for i in range(num_videos):
    # os.system(f'ffmpeg -i {video_list[i]} -qscale:v 1 -qmin 1 -qmax 1 -vsync 0  {output_path}/frame%06d.png')
    a = os.path.split(video_list[i])[1]
    output_path = os.path.join(output_dir, a)
    #调用ffmpeg，把4K视频（2160x3840）下采样4倍成540x970
    os.system(f'ffmpeg -i  {video_list[i]} -c:v libx265 -vf  scale=540:960,setsar=1:1  {output_path}')
    print(f'已完成{i}个视频')
    
    
    
