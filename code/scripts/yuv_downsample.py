import os
import numpy as np
import cv2
from yuv_io import YUVread_16bit, YUVread, YUVwrite


def downsample(y,u,v,scale=4):
    '''
    YUV downsample 
    :param y: y with a shape of [frame_num, height, width] or [height, width]
    :param u: u with a shape of [frame_num, height, width] or [height, width]
    :param v: v with a shape of [frame_num, height, width] or [height, width]
    :param scale: downsample scale rate, eg. scale = 4, downsample x4
    '''
    if len(y.shape) == 3:
        # for frame in range(y.shape[0]):
        y = np.array([cv2.resize(ch, (y.shape[2] // scale, y.shape[1] // scale), interpolation=cv2.INTER_CUBIC) for ch in y ])
        u = np.array([cv2.resize(ch, (u.shape[2] // scale, u.shape[1] // scale), interpolation=cv2.INTER_CUBIC) for ch in u ])
        v = np.array([cv2.resize(ch, (v.shape[2] // scale, v.shape[1] // scale), interpolation=cv2.INTER_CUBIC) for ch in v ])
    else:
        y = cv2.resize(y,(y.shape[1] // scale, y.shape[0] // scale), interpolation=cv2.INTER_CUBIC)
        u = cv2.resize(y,(u.shape[1] // scale, u.shape[0] // scale), interpolation=cv2.INTER_CUBIC)
        v = cv2.resize(y,(v.shape[1] // scale, v.shape[0] // scale), interpolation=cv2.INTER_CUBIC)

    return y, u, v

def main():
    bit_depth = 10
    size = (1920,1080)
    frame_num = 50
    input_path = 'datasets/yuv2yuv.yuv'
    save_path = 'datasets/down_x4'
    output_name = 'yuv_down_x4.yuv'
    #读取YUV
    if bit_depth == 10:
        y, u, v = YUVread_16bit(input_path, size=size, frame_num=frame_num, mode='420')
    else:
        y, u, v = YUVread(input_path, size=size, frame_num=frame_num, mode='420')
    
    print('读取完成')
    #对YUV下采样4倍
    y_down_x4, u_down_x4, v_down_x4 = downsample(y, u, v, scale = 4)
    print('已完成下采样')
    #写入下采样后的YUV
    os.makedirs(save_path, exist_ok = True)
    YUVwrite(y_down_x4, u_down_x4, v_down_x4, os.path.join(save_path, output_name))

if __name__ == '__main__':
    main()
