# ffmepg 命令

## 转换视频格式
```
ffmpeg -i 原视频路径和格式 -c:v copy 更改后的视频路径和格式 -y 
#例 a.mov采用HEVC编码
ffmpeg -i  a.mov  -c:v copy  a.mp4  -y  #转换后保持原有的编码格式（HEVC）
ffmpeg -i a.mov a1.mp4 -7               #使用默认编码格式（AVC）
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

## 将视频帧转为图像
```
ffmpeg -i {input_path} -qscale:v 1 -qmin 1 -qmax 1 -vsync 0  frame%06d.png
```

## 将图像帧合成视频  
将视频码率属性-b:v设为1263kb/s（具体设置按原视频码率设定）
```
ffmpeg  -framerate 29.97 -i  results/BasicVSR/frame%08d_BasicVSR.png -b:v 1263k results/BasicVSR_video/6_sdr_VSR.mp4
```

## 截取电影的前50帧，并将分辨率降为1920x1080
```
ffmpeg -i  INPUT  -vf  scale=270:480, setsar=1:1  OUTPUT  -hide_banner
ffmpeg  -i  hdr.mkv  -vframes  50 -vf scale=1920:1080,setsar=1:1  hdr_1920x1080.mp4 -hide_banner
```

## 提取视频
ffmpeg -i input.mp4 -vcodec copy -an output.mp4

## 视频剪切
下面的命令，可以从时间为00:00:15开始，截取5秒钟的视频。
```
ffmpeg -ss 00:00:15 -t 00:00:05 -i input.mp4 -vcodec copy -acodec copy output.mp4
```
`-ss`表示开始切割的时间，`-t`表示要切多少。上面就是从15秒开始，切5秒钟出来。
