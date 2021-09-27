import numpy as np
import cv2
import os
import scipy.ndimage as ndimage
import glob
import argparse
from yuv_io import YUVread_16bit


def yuv2rgb_2020(Dy, Du, Dv, mode='420', yuv_bit_depth=10, quantification=16):
    """
    only for 420 or 444 yuv mode,default 420
    input:Y,U,V（default 10bit）
    output:Drgb（default uint16)
    """
    if mode == '420':
        #U,V分量resize成Y的shape，以便进行矩阵运算
        Du = ndimage.zoom(Du, 2, order=0) #使用最近邻插值法
        Dv = ndimage.zoom(Dv, 2, order=0)

    h, w = Dy.shape
    #YUV去量化
    Ey = ((Dy/2 ** (yuv_bit_depth - 8) - 16)/219).flatten()
    Eu = ((Du/2 ** (yuv_bit_depth - 8) - 128)/224).flatten()
    Ev = ((Dv/2 ** (yuv_bit_depth - 8) - 128)/224).flatten()
    Eyuv = np.array([Ey,Eu,Ev])
    # YUV2RGB matrix
    rgb2yuv_bt2020_matrix = np.matrix([[0.2627, 0.6780, 0.0593],
                            [-0.1396, -0.3604, 0.5000],
                            [0.5000, -0.4598, -0.0402]])
    yuv2rgb_2020_matrix = rgb2yuv_bt2020_matrix.I
    Ergb = np.dot(yuv2rgb_2020_matrix, Eyuv)
    Er = Ergb[0,:].reshape(h,w)
    Eg = Ergb[1,:].reshape(h,w)
    Eb = Ergb[2,:].reshape(h,w)
    #RGB量化   
    Dr = np.round((219*Er+16)*2**(quantification - 8)).clip(0,65535)
    Dg = np.round((219*Eg+16)*2**(quantification - 8)).clip(0,65535)
    Db = np.round((219*Eb+16)*2**(quantification - 8)).clip(0,65535)
    a = [Dr,Dg,Db]
    Drgb = np.array([Dr,Dg,Db]).astype(np.uint16)
    Drgb = Drgb.transpose(1,2,0)  #(3,1920,1080)->(1920,1080,3)
    return Drgb

def create_imgs_from_yuvpath(yuv_path, save_path, frames=18, size=(1080,1920), yuv_mode='420'):
    #读取10bit的YUV
    Dy_frames, Du_frames, Dv_frames = YUVread_16bit(yuv_path, size=size, frame_num=frames, start_frame=0, mode=yuv_mode)
    for i in range(frames):
        #YUV->RGB
        Drgb = yuv2rgb_2020(Dy_frames[i,:,:], Du_frames[i,:,:], Dv_frames[i,:,:], yuv_bit_depth=10, quantification=16)
        #保存图像
        os.makedirs(save_path, exist_ok = True)
        img_name = os.path.join(save_path, f'frame{i:03d}.png')
        cv2.imwrite(img_name, cv2.cvtColor(Drgb, cv2.COLOR_RGB2BGR))
        print(f'已转换第{i}帧')

def create_imgs_from_yuv(y,u,v,save_path):
    if len(np.shape(y)) == 3:
        frame_num = np.shape(y)[0]
        for i in range(frame_num):
            #YUV->RGB
            Drgb = yuv2rgb_2020(y[i,:,:], u[i,:,:], v[i,:,:], yuv_bit_depth=10, quantification=16)
            #保存图像
            os.makedirs(save_path, exist_ok = True)
            img_name = os.path.join(save_path, f'frame{i:03d}.png')
            cv2.imwrite(img_name, cv2.cvtColor(Drgb, cv2.COLOR_RGB2BGR))
    else:
        #YUV->RGB
        Drgb = yuv2rgb_2020(y, u, v, yuv_bit_depth=10, quantification=16)
        #保存图像
        os.makedirs(save_path, exist_ok = True)
        img_name = os.path.join(save_path, f'frame{i:03d}.png')
        cv2.imwrite(img_name, cv2.cvtColor(Drgb, cv2.COLOR_RGB2BGR))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--yuv_path', type=str, default='G:\datasets\HLG\yuv\gt_from_4k', help='input test image folder')
    parser.add_argument('--save_path', type=str, default='G:\datasets\HLG\\rgb18\\train_gt', help='save image path')
    parser.add_argument('--frames', type=int, default=18, help='frames number')
    parser.add_argument('--size', type=int, default=(1080,1920), help='input video size:(h,w)')
    args = parser.parse_args()
    
    if os.path.isdir(args.yuv_path):
        yuv_list = sorted(glob.glob(os.path.join(args.yuv_path, '*.*')))
        for i in range(len(yuv_list)):
            yuv_name = os.path.splitext(os.path.basename(yuv_list[i]))[0]
            save_path = os.path.join(args.save_path, yuv_name)
            os.makedirs(save_path, exist_ok=True)
            create_imgs_from_yuvpath(yuv_list[i], save_path, frames=args.frames, size=args.size, yuv_mode='420')
    else: 
        create_imgs_from_yuvpath(args.yuv_path, args.save_path, frames=args.frames, size=args.size, yuv_mode='420')

if __name__ == '__main__':
    main()
