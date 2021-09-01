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
 
def main():
    image_path = 'code/test2.png'
    save_path = 'rgb2yuv.yuv'
    #如果输入为图像序列路径，则批量处理，否则只处理一张
    if os.path.isdir(image_path):
        imgs_list = sorted(glob.glob(os.path.join(image_path, '*')))
        num_imgs = len(imgs_list)
        #以planner的方式逐帧把YUV保存到'rgb2yuv.yuv'文件下
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

