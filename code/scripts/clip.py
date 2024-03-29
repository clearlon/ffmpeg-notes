import os 
import cv2


input_path = 'E:\视频\Our.Friend.2021.2160p.AMZN.WEB-DL.x265.10bit.HDR10Plus.DTS-HD.MA.5.1-SWTYBLZ\Our.Friend.2021.2160p.AMZN.WEB-DL.x265.10bit.HDR10Plus.DTS-HD.MA.5.1-SWTYBLZ.mkv'
output_dir = 'E:\HDR视频\HDR_filmclip'

def get_video_duration(filename):
    cap = cv2.VideoCapture(filename)
    if cap.isOpened():
        rate = cap.get(5)  #获取视频帧率
        frame_num =cap.get(7)   #获取视频总帧数
        duration = frame_num/rate
        return duration
    return -1

duration = get_video_duration(input_path)
print(duration)

start_time = 120    # 开始时间（单位：s）
lasts_time = 10     # 截取多长时间
for i in range(int(duration)):
    filename = 'hdr10_' + str(i) + '.mp4'
    output_path = os.path.join(output_dir, filename)
    print(f'开始截取第{i}段视频:ss {start_time} t {lasts_time}')
    os.system(f'ffmpeg -i {input_path} -ss {str(start_time)} -t {str(lasts_time)} -vcodec copy -an {output_path} -y')
    start_time = start_time + lasts_time

print('完成')

