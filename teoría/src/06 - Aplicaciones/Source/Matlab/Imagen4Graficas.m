im=uint8(rand(100,100)*255);
figure;imshow(im);print -depsc Colormap1
figure;imshow(im,colormap('hsv'));print -depsc Colormap2
figure;imshow(im,colormap('autumn'));print -depsc Colormap3