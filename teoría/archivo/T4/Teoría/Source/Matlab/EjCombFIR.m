L=5;
%hn=1/2*[1 1];
hn=1/3*[1 1 1];
N=length(hn);
hnL([0:N-1]*L+1)=hn;

[hw,w]=freqz(hn,1,0:0.01:2*pi);
[hwL,wL]=freqz(hnL,1,0:0.01:2*pi);

