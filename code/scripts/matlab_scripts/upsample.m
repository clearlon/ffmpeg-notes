function upsample(video_path, video_name, save_bic_folder, up_scale, data_type)
%UPSAMPLE matlab code to generate bicubic-upsampled for low-resolution images
%   
imgs_path = fullfile(video_path, video_name);
filepaths = dir(fullfile(imgs_path,'*.*'));
disp(fullfile(imgs_path, '*.*'));
idx = 0;
for i = 1 : length(filepaths)
    [~, img_name, ext] = fileparts(filepaths(i).name);
    if isempty(img_name)
        disp('Ignore . folder.');
    elseif strcmp(img_name, '.')
        disp('Ignore .. folder.');
    else
        idx = idx + 1;
        str_result = sprintf('%d\t%s.\n', idx, img_name);
        fprintf(str_result);

        % read image
        im_lr = imread(fullfile(imgs_path, [img_name, ext]));
        im_lr = im2double(im_lr);
        
         %Bicubic
        if exist('save_bic_folder', 'var')
            im_bicubic = imresize(im_lr, up_scale, 'bicubic');
            if strcmp(data_type, 'uint8')
                imwrite(im2uint8(im_bicubic), fullfile(save_bic_folder, video_name, [img_name, '.png']));
            elseif strcmp(data_type, 'uint16')
                imwrite(im2uint16(im_bicubic), fullfile(save_bic_folder, video_name, [img_name, '.png']));
            else
                error('input data type is not uint8 or uint16');
            end
        end
    end
end
end
