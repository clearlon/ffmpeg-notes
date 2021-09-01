import numpy as np
import cv2
import os
import scipy.ndimage as ndimage
from data.yuv_io import YUVread_16bit


def yuv2rgb_2020(Dy, Du, Dv, yuv_bit_depth=10, quantification=16):
    """
    input:Y,U,V
    output:Drgb（uint16)
    """
    #YUV去量化  针对10bit  若是16bit,则/256
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
    Er = Ergb[0,:].reshape(1920,1080)
    Eg = Ergb[1,:].reshape(1920,1080)
    Eb = Ergb[2,:].reshape(1920,1080)
    #RGB量化   量化为16bit
    Dr = np.round((219*Er+16)*2**(quantification - 8)).clip(0,65535)
    Dg = np.round((219*Eg+16)*2**(quantification - 8)).clip(0,65535)
    Db = np.round((219*Eb+16)*2**(quantification - 8)).clip(0,65535)
    a = [Dr,Dg,Db]
    Drgb = np.array([Dr,Dg,Db]).astype(np.uint16)
    Drgb = Drgb.transpose(1,2,0)  #(3,1920,1080)->(1920,1080,3)
    # Drgb = Drgb.astype(np.uint16)
    return Drgb

def yuv2rgb_709_matrix(Dy,Du,Dv):
    """
    input:Y,U,V
    output:uint8 Drgb
    """
    h, w = Dy.shape
    #YUV去量化  针对8bit
    print(np.max(Dy))
    Ey = ((Dy-16)/219).flatten()
    print(np.max(Ey))
    print(np.min(Ey))
    Eu = ((Du-128)/224).flatten()
    Ev = ((Dv-128)/224).flatten()
    Eyuv = np.array([Ey,Eu,Ev])
    # YUV2RGB matrix
    yuv2rgb_709_matrix = np.matrix([[1., 0, 1.5747],
                                    [1., -0.1873, -0.4682],
                                    [1., 1.8556, 0]])
    Ergb = np.dot(yuv2rgb_709_matrix, Eyuv)
    Er = Ergb[0,:].reshape(h,w)
    Eg = Ergb[1,:].reshape(h,w)
    Eb = Ergb[2,:].reshape(h,w)
    #RGB量化   8bit
    Dr = np.round((219*Er+16)).clip(0,255)
    Dg = np.round((219*Eg+16)).clip(0.255)
    Db = np.round((219*Eb+16)).clip(0.255)
    Drgb = np.array([Dr,Dg,Db]).astype(np.uint8)
    Drgb = Drgb.transpose(1,2,0)  #(3,1920,1080)->(1920,1080,3)
    # Drgb = Drgb.astype(np.uint16)
    return Drgb

#有误，待完善
def yuv2rgb_709(Dy,Du,Dv):
    """
    input:Y,U,V
    output:uint8 Drgb
    """
    Dr = Dy + 1.402 * (Dy - 128)
    print(np.max(Dr))
    Dg = Dy - 0.34413 * (Du - 128) - 0.71414*(Dv - 128)
    Db = Dy + 1.772*(Du - 128)
    Dr = Dr.clip(0.255)
    Dg = Dg.clip(0.255)
    Db = Db.clip(0.255)
    Drgb = np.array([Dr,Dg,Db]).astype(np.uint8)
    Drgb = Drgb.transpose(1,2,0)  #(3,1920,1080)->(1920,1080,3)
    # Drgb = Drgb.astype(np.uint16)
    return Drgb

def main():
    yuv_path = 'datasets/HR.yuv'
    save_path = 'datasets/rgb'
    #读取前50帧YUV
    frames = 50
    #读取10bit的YUV
    Dy_frames, Du_frames, Dv_frames = YUVread_16bit(yuv_path, (1920,1080), frame_num=frames, start_frame=0, mode='420')
    #读取8bit的YUV
    # Dy_frames, Du_frames, Dv_frames = YUVread(yuv_path, (1080,1920), frame_num=frames, start_frame=0, mode='420')
    for i in range(frames):
        #U,V分量resize成Y的shape，以便进行矩阵运算
        # Du = cv2.resize(Du_frames[i,:,:],(Du_frames.shape[2]*2,Du_frames.shape[1]*2),interpolation=cv2.INTER_NEAREST)
        # Dv = cv2.resize(Dv_frames[i,:,:],(Dv_frames.shape[2]*2,Dv_frames.shape[1]*2),interpolation=cv2.INTER_NEAREST)
        Du = ndimage.zoom(Du_frames[i,:,:], 2, order=0)
        Dv = ndimage.zoom(Dv_frames[i,:,:], 2, order=0)
        #YUV->RGB
        Drgb = yuv2rgb_2020(Dy_frames[i,:,:], Du, Dv, yuv_bit_depth=10, quantification=8)
        #Drgb = yuv2rgb_709_matrix(Dy_frames[i,:,:], Du, Dv)
        cv2.imwrite(os.path.join(save_path, f'frame{i:03d}.png'), cv2.cvtColor(Drgb, cv2.COLOR_RGB2BGR))
        print(f'已转换第{i}帧')

if __name__ == '__main__':
    main()
