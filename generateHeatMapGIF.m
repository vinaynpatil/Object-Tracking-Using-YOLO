function generateGIF()
%Getting the full directory name

folder_name = "Heatmaps_One_Man_Bigger_With_Cars_Movement_moving";

directory_name = fullfile(folder_name, '*.png');
%Getting all files in the directory
directory_files = dir(directory_name);
count = length(directory_files);
background = imread('background.png');
%size(background)
filename = strcat('one_man_moving.gif');

for k = 1:count
    image_name = strcat(folder_name,'/Heatmap (',num2str(k),').png')
    image = imread(image_name);
    %image = imresize(image,[358 640]);
    %size(image)
    image = background + image;
    
    [A,map] = rgb2ind(image,256);
    if k == 1
        imwrite(A,map,filename,'gif','LoopCount',Inf,'DelayTime',0.1);
    else
        imwrite(A,map,filename,'gif','WriteMode','append','DelayTime',0.1);
    end
end