if 0
Ts=0.01;Fs=1/Ts;
t=0:Ts:20;
F0=40;F1=30;
x=chirp(t,F0,5,F1)


for a=0:3
    index=1+a*500:(a+1)*500;
    window=ones(length(index),1);
    %window=hamming(length(index)); 
    xp=x(index).*window';
    Xp=fft(xp)
    w=[0:499]/500/Ts;
    subplot(4,1,a+1);
    plot(w,abs(Xp));
    set(gca,'FontSize',16);
    if a==3
        xlabel('F (Hz)','FontSize',16);
    end
    ylabel('X(e^{jw})','FontSize',16);
    title(sprintf('Tramo [%3.2f,%3.2f]',t(index([1,end]))));
end

print -depsc Spect1


for a=0:3
    index=1+a*500:(a+1)*500;
    window=ones(length(index),1);
    window=hamming(length(index)); 
    xp=x(index).*window';
    Xp=fft(xp)
    w=[0:499]/500/Ts;
    subplot(4,1,a+1);
    plot(w,abs(Xp));
    set(gca,'FontSize',16);
    if a==3
        xlabel('F (Hz)','FontSize',16);
    end
    ylabel('X(e^{jw})','FontSize',16);
    title(sprintf('Tramo [%3.2f,%3.2f]',t(index([1,end]))));
end


print -depsc Spect2
end

Ts=0.01;Fs=1/Ts;
t=0:Ts:20;
F0=40;F1=30;
x=chirp(t,F0,5,F1);
L=500;index=1:L;
for b=1:2
figure;
for a=0:3
    %window=ones(L);
    window=hamming(L)
    xp=x(index).*window';
    Xp=fft(xp);
    f=[0:499]/500/Ts;
    
    subplot(4,1,a+1);plot(f,abs(Xp));
    set(gca,'FontSize',16);
    if a==3
        xlabel('F (Hz)','FontSize',16);
    end
    ylabel('X(e^{jw})','FontSize',16);
    title(sprintf('Tramo [%3.2f,%3.2f]',t(index([1,end]))));
    index=index+L/2;
    if any(index>length(t))
        break;
    end
end
end

print -depsc Spect3


spectrogram(x,128,120,[],Fs);


view(90,-90)
view(58,54)
set(gca,'FontSize',16);