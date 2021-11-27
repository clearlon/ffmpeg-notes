clear
clc
input_folder = 'G:\datasets\HLG\rgb18\val_gt\hdr';
save_lr_folder = 'G:\datasets\HLG\rgb18\tesss';

% mkdir(save_lr_folder)

%setting output data type, 'uint8' or 'uint16'
data_type = 'uint16'; 
up_scale = 4;

filepaths = dir(fullfile(input_folder,'*.*'));
for i = 1 : length(filepaths)
    [~, img_name, ext] = fileparts(filepaths(i).name);
    if isempty(img_name) || strcmp(img_name, '.')
        disp('Ignore . folder and .. folder.');
        continue
    end
    %根据子文件是否有后缀来判断需要批处理还是处理单独场景
    if isempty(ext)  %批处理
        video_name =  filepaths(i).name;
        video_path = filepaths(i).folder;
         if exist(fullfile(save_lr_folder, video_name), 'dir')
            disp(fullfile(save_lr_folder, video_name))
            continue
        end
        mkdir(fullfile(save_lr_folder, video_name));
        imgs_down_x4(video_path, video_name, save_lr_folder, up_scale, data_type)
    else  %单场景处理
        [video_path, video_name, ~] = fileparts(input_folder);
         if exist(fullfile(save_lr_folder, video_name), 'dir')
            disp(fullfile(save_lr_folder, video_name))
            continue
        end
        mkdir(fullfile(save_lr_folder, video_name));
        imgs_down_x4(video_path, video_name, save_lr_folder, up_scale, data_type)
        break
    end
end


function imgs_down_x4(video_path, video_name, save_lr_folder, up_scale, data_type)
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
        img = imread(fullfile(imgs_path, [img_name, ext]));
        % [a, b, c] = size(img);
        img = im2double(img);
        % LR
        im_lr = imresize(img, 1/up_scale, 'bicubic');
        %im_lr = im2uint16(im_lr);
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



