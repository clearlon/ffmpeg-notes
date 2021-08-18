# ffmepg 命令

## 转换视频格式
```
ffmpeg -i 原视频路径和格式 -c:v copy 更改后的视频路径和格式 -y 
#例
ffmpeg -i  a.flv  -c:v copy  a.mp4  -y
```
`-c:v copy` : indicate that the stream is not to be re-encoded 

 `-y`: Overwrite output files without asking（直接覆盖原同名文件）
 
##For example
```
ffmpeg -i INPUT -map 0 -c:v libx264 -c:a copy OUTPUT
```
encodes all video streams with libx264 and copies all audio streams.

For each stream, the last matching c option is applied, so
```
ffmpeg -i INPUT -map 0 -c copy -c:v:1 libx264 -c:a:137 libvorbis OUTPUT
```
will copy all the streams except the second video, which will be encoded with libx264, and the 138th audio, which will be encoded with libvorbis.

## 将HDR视频转为SDR视频
```
ffmpeg -i 原视频路径和格式 -vf zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p -c:v libx265 -crf 18 -preset slower 更改后的视频路径和格式
ffmpeg -i /Users/unbelievable/iCloudDrive/Desktop/龙/研究生学习/HDR视频/6_hdr.MOV -vf zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p -c:v libx265 -crf 18 -preset slower /Users/unbelievable/iCloudDrive/Desktop/龙/研究生学习/HDR视频/6_sdr.mkv
```

ffmpeg -i /Users/unbelievable/Downloads/20210629-145829-730.MP4 -c:v libx264 -preset veryslow -crf 18 -c:a copy /Users/unbelievable/Downloads/20210629-145829-730.MP4


提取视频帧
ffmpeg -i {input_path} -qscale:v 1 -qmin 1 -qmax 1 -vsync 0  frame%06d.png

将图像帧合成视频  将视频码率属性-b:v设为1263kb/s（具体设置按原视频码率设定）
ffmpeg  -framerate 29.97 -i  results/BasicVSR/frame%08d_BasicVSR.png -b:v 1263k results/BasicVSR_video/6_sdr_VSR.mp4

截取电影的前50帧，并将分辨率降为1920x1080
ffmpeg -i  原视频  -vf  scale=270:480, setsar=1:1  输出视频  -hide_banner
ffmpeg  -i  E:\视频\Our.Friend.2021.2160p.AMZN.WEB-DL.x265.10bit.HDR10Plus.DTS-HD.MA.5.1-SWTYBLZ\Our.Friend.2021.2160p.AMZN.WEB-DL.x265.10bit.HDR10Plus.DTS-HD.MA.5.1-SWTYBLZ.mkv  -vframes  50 -vf scale=1920:1080,setsar=1:1  E:\HDR视频\hdr_1920x1080.mp4 -hide_banner
