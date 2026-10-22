wc=0.5*pi;Ls=[5,10,20,30];
k=1;c=rand(4,3);
for L=Ls
n=-L:L;
h=sin(wc*(n))./n/pi;h(L+1)=wc/pi;
[hw,w]=freqz(h,1);
subplot(2,1,1),hold on,grid on;
plot(w/pi,abs(hw),'Color',c(k,:));
ylabel('|H(exp(jw))|');
subplot(2,1,2),hold on,grid on,
ang=unwrap(angle(hw));
plot(w/pi,ang,'Color',c(k,:));
ylabel('arg H(exp(jw))');
xlabel('w/\pi'),
msg{k}=sprintf('N=%d',2*L)
k=k+1;
end
subplot(2,1,1);
legend(msg{:});
