import numpy as np
import cv2
import glob
import os


def rgb2yuv_2020(Dbgr):
    '''
    input: 16bit的PNG
    output: 10bit的Dyuv
    '''
    h, w, _ = Dbgr.shape
    #RGB去量化  输入为16bit PNG, 若为8bit,则 /4
    Er = ((Dbgr[:,:,2]/256-16)/219).flatten()
    Eg = ((Dbgr[:,:,1]/256-16)/219).flatten()
    Eb = ((Dbgr[:,:,0]/256-16)/219).flatten()
    Ergb = np.array([Er,Eg,Eb])
    #RGB2YUV
    rgb2yuv_bt2020_matrix = np.matrix([[0.2627, 0.6780, 0.0593],
                                        [-0.1396, -0.3604, 0.5000],
                                        [0.5000, -0.4598, -0.0402]])
    Eyuv = np.dot(rgb2yuv_bt2020_matrix, Ergb)
    Ey = Eyuv[0,:].reshape(h, w)
    Ecb = Eyuv[1,:].reshape(h, w)
    Ecr = Eyuv[2,:].reshape(h, w)
    #YUV量化 10bit   若是16bit，则2**8
    Dy = np.round((219*Ey+16)*2**2).clip(0,1024)
    Dcb = np.round((224*Ecb+128)*2**2).clip(0,1024)
    Dcr = np.round((224*Ecr+128)*2**2).clip(0,1024)
    Dyuv = np.array([Dy,Dcb,Dcr])
    Dyuv = Dyuv.astype(np.uint16)
    Dyuv = Dyuv.transpose(1,2,0)  #(3,h,w)->(h,w,3)
    return Dyuv

def yuv2rgb_2020(Dyuv):
    '''
    input: Dyuv 10bit(np.uint16)
    output: Drgb 16bit(np.uint16)
    '''
    #YUV去量化  针对10bit  若是16bit,则/256
    Ey = ((Dyuv[:,:,0]/4-16)/219).flatten()
    Ecb = ((Dyuv[:,:,1]/4-128)/224).flatten()
    Ecr = ((Dyuv[:,:,2]/4-128)/224).flatten()
    Eyuv = np.array([Ey,Ecb,Ecr])
    #YUV2RGB
    rgb2yuv_bt2020_matrix = np.matrix([[0.2627, 0.6780, 0.0593],
                            [-0.1396, -0.3604, 0.5000],
                            [0.5000, -0.4598, -0.0402]])
    yuv2rgb_2020_matrix = rgb2yuv_bt2020_matrix.I
    Ergb = np.dot(yuv2rgb_2020_matrix, Eyuv)
    Er = Ergb[0,:].reshape(1920,1080)
    Eg = Ergb[1,:].reshape(1920,1080)
    Eb = Ergb[2,:].reshape(1920,1080)
    Ergb = np.array([Er,Eg,Eb])
    Ergb = Ergb.transpose(1,2,0)
    #RGB量化   #量化为16bit，若为8bit，则为 2**2
    Drgb = np.zeros((1920,1080,3))
    Drgb[:,:,0] = (219*Ergb[:,:,0]+16)*2**8
    Drgb[:,:,1] = (219*Ergb[:,:,1]+16)*2**8
    Drgb[:,:,2] = (219*Ergb[:,:,2]+16)*2**8
    Drgb = Drgb.astype(np.uint16)
    return Drgb
 
def main():
    image_path = 'code/test2.png'
    save_path = 'rgb2yuv2.yuv'
    #如果输入为图像序列路径，则批量处理，否则只处理一张
    if os.path.isdir(image_path):
        imgs_list = sorted(glob.glob(os.path.join(image_path, '*')))
        num_imgs = len(imgs_list)
        with open(save_path, 'wb') as file:
            for i in range(50):
                Dbgr = cv2.imread(imgs_list[i], cv2.IMREAD_UNCHANGED)
                #RGB->YUV
                Dyuv = rgb2yuv_2020(Dbgr)
                # Dyuv = np.ascontiguousarray(Dyuv)  #解决Dyuv数据存储地址不连续问题
                Dy = Dyuv[:,:,0]
                Du = Dyuv[:,:,1]
                Dv = Dyuv[:,:,2]
                #对uv分量采样，转换成YUV420格式
                Du = np.array([cv2.resize(Du, (Du.shape[1] // 2, Du.shape[0] // 2), interpolation=cv2.INTER_CUBIC)])
                Dv = np.array([cv2.resize(Dv, (Dv.shape[1] // 2, Dv.shape[0] // 2), interpolation=cv2.INTER_CUBIC)])
                # 写入YUV
                file.write(Dy.tobytes())
                file.write(Du.tobytes())
                file.write(Dv.tobytes())
                # YUV->RGB来显示结果
                # Drgb = yuv2rgb_2020(Dyuv)
                # Dbgr = cv2.cvtColor(Drgb, cv2.COLOR_RGB2BGR)
                # cv2.imwrite('code/t1.png', Dbgr)
                print(f'已转换第{i}帧')
        file.close()
    else:
        with open(save_path, 'wb') as file:
            Dbgr = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            #RGB->YUV
            Dyuv = rgb2yuv_2020(Dbgr)
            # Dyuv = np.ascontiguousarray(Dyuv)  #解决Dyuv数据存储地址不连续问题
            Dy = Dyuv[:,:,0]
            Du = Dyuv[:,:,1]
            Dv = Dyuv[:,:,2]
            #对uv分量采样，转换成YUV420格式
            Du = np.array([cv2.resize(Du, (Du.shape[1] // 2, Du.shape[0] // 2), interpolation=cv2.INTER_CUBIC)])
            Dv = np.array([cv2.resize(Dv, (Dv.shape[1] // 2, Dv.shape[0] // 2), interpolation=cv2.INTER_CUBIC)])
            #写入YUV
            file.write(Dy.tobytes())
            file.write(Du.tobytes())
            file.write(Dv.tobytes())
            file.close()

if __name__ == '__main__':
    main()

