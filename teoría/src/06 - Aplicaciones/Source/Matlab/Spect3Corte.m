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
    xlabel('F (Hz)');ylabel('X(e^{jw})');
    rango=t(index([1,end]));
    title(sprintf('Tramo [%3.2f,%3.2f]',rango));
    index=index+L/2;
    if any(index>length(t))
        break;
    end
end
end

