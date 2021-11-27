clear
clc
input_folder = 'G:\datasets\HLG\rgb18\val_lr\hdr2sdr';
save_bicubic_folder = 'G:\datasets\HLG\rgb18\val_bic\hdr2sdr';

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
    if isempty(ext)
        video_name =  filepaths(i).name;
        video_path = filepaths(i).folder;
        mkdir(fullfile(save_bicubic_folder, video_name));
        upsample(video_path, video_name, save_bicubic_folder, up_scale, data_type)
    else
        [video_path, video_name, ~] = fileparts(input_folder);
        mkdir(fullfile(save_bicubic_folder, video_name));
        upsample(video_path, video_name, save_bicubic_folder, up_scale, data_type)
        break
    end
end




