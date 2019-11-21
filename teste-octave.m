clear all 
close all
clc
I = imread('proximo-letreiro.jpg');
figure, imshow(I)
temp_I = histeq(I);
temp_I = imadjust(temp_I);
figure, imshow(temp_I);
temp_I=uint8((temp_I)*255);
figure, imshow(temp_I);
radius_range = 1:22;
intensity_area = zeros(size(radius_range));
for counter = radius_range
    remain = imopen(temp_I, strel('disk', counter,0));
    intensity_area(counter + 1) = sum(remain(:));  
end
figure
plot(intensity_area, 'm - *')
grid on
title('Sum of pixel values in opened image versus radius')
xlabel('radius of opening (pixels)')
ylabel('pixel value sum of opened objects (intensity)')
intensity_area_prime = diff(intensity_area);
figure, plot(intensity_area_prime, 'm - *')
grid on
title('Granulometry (Size Distribution) of Snowflakes')
%ax = gca;
XTick = [0 2 4 6 8 10 12 14 16 18 20 22];
xlabel('radius of snowflakes (pixels)')
ylabel('Sum of pixel values in snowflakes as a function of radius')
open5 = imopen(temp_I,strel('disk',5,0));
open6 = imopen(temp_I,strel('disk',6,0));
rad5 = imsubtract(open5,open6);
figure, imshow(rad5,[])