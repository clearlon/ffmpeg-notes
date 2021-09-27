function y_downsample(y, size, frame_num, scale, save_path, yuv_name)
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