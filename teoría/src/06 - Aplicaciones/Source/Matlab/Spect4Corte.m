Ts=0.01;Fs=1/Ts;
t=0:Ts:20;
F0=40;F1=30;
x=chirp(t,F0,5,F1);
spectrogram(x,128,120,[],Fs);
%Reorientar los ejes
view(90,-90) 


