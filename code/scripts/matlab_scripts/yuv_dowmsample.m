clear
clc
%run yuvdownsample_x4
save_path='G:\datasets\HLG\Yframes\Y_lr';
if ~exist(save_path,'dir')
    mkdir(save_path)
end

maindir='G:\datasets\HLG\Yframes\Y_gt';

height = 1080;
weight = 1920;
frame_num = 18;
scale = 4;
mode = '420';
yuvfile=dir(fullfile(maindir,'*.yuv'));
for i =1:length(yuvfile)
    yuv_name = yuvfile(i).name;  
    yuvseq = fullfile(maindir, yuv_name);
    if ~exist(fullfile(save_path, yuv_name), 'file')
%         [y, ~, ~] = YUVread_16bit(yuvseq, [weight, height], frame_num, '420');
        y = Yread_16bit(yuvseq, [weight, height], frame_num);
        YDownsample(y, [weight, height],frame_num, scale, save_path, yuv_name)
        clear y
    end
end

function YUVDownsample(y ,u ,v, size, frame_num, scale, save_path, yuv_name)
%YUVDownsample for yuv down sample
% only for yuv 420
weight = size(1);
height = size(2);
YY=zeros(weight/scale,height/scale,frame_num);   
UU=zeros(weight/2/scale,height/2/scale,frame_num);
VV=zeros(weight/2/scale,height/2/scale,frame_num);

for frame=1:frame_num
    YY(:,:,frame) = round(imresize(y(:, :, frame), 1/scale, 'bicubic'));
    UU(:,:,frame) = round(imresize(u(:, :, frame), 1/scale, 'bicubic'));
    VV(:,:,frame) = round(imresize(v(: ,: ,frame), 1/scale, 'bicubic'));
end
clear y u v

fprintf('%s is processing...\n', yuv_name);
yuv_path = fullfile(save_path, yuv_name);
outfid=fopen(yuv_path,'wb');
for frame=1:frame_num
    fprintf('downsampling frame=%d\n',frame)
    fwrite(outfid,YY(:,:,frame), 'uint16');
    fwrite(outfid,UU(:,:,frame), 'uint16');
    fwrite(outfid,VV(:,:,frame), 'uint16');
end
fclose(outfid);
clear YY UU VV
end

function YDownsample(y, size, frame_num, scale, save_path, yuv_name)
%YUVDownsample for yuv down sample
% only for yuv 420
weight = size(1);
height = size(2);
YY=zeros(weight/scale,height/scale,frame_num);   
for frame=1:frame_num
    YY(:,:,frame) = round(imresize(y(:, :, frame), 1/scale, 'bicubic'));
end
fprintf('%s is processing...', yuv_name);
yuv_path = fullfile(save_path, yuv_name);
outfid=fopen(yuv_path,'wb');
for frame=1:frame_num
    fprintf('downsampling frame=%d\n',frame)
    fwrite(outfid,YY(:,:,frame), 'uint16');
end
fclose(outfid);
end

function y = Yread_16bit(yuv_path, size, frame_num)
weight = size(1);
height = size(2);
 y=zeros(weight,height,frame_num);
yuv_file = fopen(yuv_path, 'r');
for frame = 1:frame_num
    y_tmp = fread(yuv_file, weight * height * 2, 'uchar');
    y(:,:,frame) = reshape(y_tmp(1:2:end) + bitshift(y_tmp(2:2:end), 8), weight, height);
end
end

function [y, u, v] = YUVread_16bit(yuv_path, size, frame_num, mode)
%downsample for yuv 
%   only for 4:2:0 and 4:4:4
weight = size(1);
height = size(2);
if strcmp(mode, '420')
    y=zeros(weight,height,frame_num);
    u=zeros(weight/2,height/2,frame_num);
    v=zeros(weight/2,height/2,frame_num);
    yuv_file = fopen(yuv_path, 'r');
    for frame = 1:frame_num
        y_tmp = fread(yuv_file, weight * height * 2, 'uchar');
        y(:,:,frame) = reshape(y_tmp(1:2:end) + bitshift(y_tmp(2:2:end), 8), weight, height);
        clear y_tmp
        u_tmp = fread(yuv_file, weight * height * 2 / 4, 'uchar');
        u(:,:,frame) = reshape(u_tmp(1:2:end) + bitshift(u_tmp(2:2:end), 8), weight / 2, height / 2);
        clear u_tmp
        v_tmp = fread(yuv_file, weight * height * 2 / 4 , 'uchar');
        v(:,:,frame) = reshape(v_tmp(1:2:end) + bitshift(v_tmp(2:2:end), 8), weight / 2, height / 2);
        clear v_tmp
    end
else
    y=zeros(row,col,frame_num);
    u=zeros(row,col,frame_num);
    v=zeros(row,col,frame_num);
    yuv_file = fopen(yuv_path, 'r');
    for frame = 1:frame_num
        y_tmp = fread(yuv_file, weight * height * 2, 'uchar');
        y(:,:,frame) = reshape(y_tmp(1:2:end) + bitshift(y_tmp(2:2:end), 8), weight, height);
        u_tmp = fread(yuv_file, weight * height * 2, 'uchar');
        u(:,:,frame) = reshape(u_tmp(1:2:end) + bitshift(u_tmp(2:2:end), 8), weight, height);
        v_tmp = fread(yuv_file, weight * height * 2 , 'uchar');
        v(:,:,frame) = reshape(v_tmp(1:2:end) + bitshift(v_tmp(2:2:end), 8), weight, height);
    end
end
end
