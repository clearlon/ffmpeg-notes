function rgb_downsample(video_path, video_name, save_lr_folder, scale, data_type)
imgs_path = fullfile(video_path, video_name);
filepaths = dir(fullfile(imgs_path,'*.*'));
disp(fullfile(imgs_path, '*.*'));
for i = 1 : length(filepaths)
    [~, img_name, ext] = fileparts(filepaths(i).name);
    if isempty(img_name)
        disp('Ignore . folder.');
    elseif strcmp(img_name, '.')
        disp('Ignore .. folder.');
    else
        % read image
        img = imread(fullfile(imgs_path, [img_name, ext]));
        % [a, b, c] = size(img);
        img = im2double(img);
        % LR
        im_lr = imresize(img, 1/scale, 'bicubic');
        if exist('save_lr_folder', 'var')
            if strcmp(data_type, 'uint8')
                imwrite(im2uint8(im_lr), fullfile(save_lr_folder, video_name, [img_name, '.png']));
            elseif strcmp(data_type, 'uint16')
                imwrite(im2uint16(im_lr), fullfile(save_lr_folder, video_name, [img_name, '.png']));
            else
                error('input data type is not uint8 or uint16');
            end
        end
    end
end
end
