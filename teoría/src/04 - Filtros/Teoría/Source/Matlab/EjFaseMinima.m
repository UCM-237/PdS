close all;
den=1/4*poly([0.5,0.1+0.3j,0.1-0.3j])
num1=poly([0.3j,-0.3j,4])
num2=4*poly([0.3j,-0.3j,1/4])
num3=0.3^2/4*poly([1/0.3j,-1/0.3j,4])

[hw1,w1]=freqz(num1,den)
[hw2,w2]=freqz(num2,den)
[hw3,w3]=freqz(num3,den)

subplot(2,1,1);hold on;
plot(w1/pi,abs(hw1),'r'),
plot(w2/pi,abs(hw2),'g'),
plot(w3/pi,abs(hw3),'b'),
legend('H_1(exp(jw))',...
        'H_{MIN}(exp(jw))',...
        'H_{MAX}(exp(jw))');
ylabel('|H(exp(jw)|')
subplot(2,1,2);hold on;
plot(w1/pi,unwrap(angle(hw1)),'r'),
plot(w2/pi,unwrap(angle(hw2)),'b'),
plot(w3/pi,unwrap(angle(hw3)),'g'),

ylabel('arg(H(exp(jw))')
xlabel('w/pi')
