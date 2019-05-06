clear
clc
list = dir('*.png'); % reading all the images one by one .
for i = 1:length(list)
img{i} = imread(list(i).name);
end
numimg=(size(img));
avgmat=img{1};
sizeofimg=size(img{1});
avgtmp=zeros(sizeofimg(1),sizeofimg(2),sizeofimg(3),numimg(2));
j=1;

while j <=numimg(2)
    im=img{j};
    for d=1:sizeofimg(3)
        for r=1:sizeofimg(1)
            for c=1:sizeofimg(2)
                avgtmp(r,c,d,j)=im(r,c,d);
            end
        end
    end
    j=j+1;
end

for d=1:sizeofimg(3)
    for r=1:sizeofimg(1)
        for c=1:sizeofimg(2)
            avgmat(r,c,d)=mode(avgtmp(r,c,d,:));
        end
    end
end
imshow(avgmat);
imwrite(avgmat,'background.png');