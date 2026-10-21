%% Muestreo Discreto
close all;
clear all;

wc = 2*pi / 10;
ws = 20*wc;
Ts = 2*pi / ws;

M = 200;
n = [1:M];
yd = cos(wc*n*Ts);

N = 5;
kN = (mod(n, N) == 0);
yds = yd .* kN;

figure();

subplot(211); hold on; grid();
stem(n(1:20), yd(1:20));
title('Señal Original');
xlabel('n');
ylabel('x(n)');
subplot(212); hold on; grid();
stem(n(1:20), yds(1:20));
title('Señal Muestreada');
xlabel('n');
ylabel('x_p(n)');

figure();
subplot(211); hold on; grid();

x = zeros(M, 1);
for i=1:M
  tt = (wc / pi) * (n-i);
  x = x + (N*wc/pi)*yds(i).*sinc(tt');
end

figure();
stem([90:110], x(90:110));
%% Diezmado
close all;
clear all;

wc = 2*pi / 10;
ws = 10*wc;
Ts = 2*pi / ws;

M = 200;
n = [1:M];
yd = cos(wc*n*Ts);

N = 2;
Nn = [1:N:M]';
Nk = length(Nn);
kN = (mod(n-1, N) == 0);
yds = yd .* kN;
ydb = yds(Nn);

figure();
subplot(211); hold on; grid();
stem(n, yds, 'x');
title('Señal Muestreada');
xlabel('n');
ylabel('x_p(n)');
xlim(gca, [0, 20]);
subplot(212); hold on; grid();
stem(Nn, ydb, 'o');
xlim(gca, [0, 20]);
title('Señal Diezmada');
xlabel('n');
ylabel('x_b(n)');

Yd = fft(yd);
Yd = Yd(1:(M-1)/2);
Yds = fft(yds);
Yds = Yds(1:(M-1)/2);
Ydb = fft(ydb);
Ydb = Yds(1:length(Nn)/2);

fd = 2*pi*[0:(M-1)/2-1] / (M*Ts);
fds = 2*pi*[0:length(Nn)/2-1] / (Nn(end)/(N*Ts));

figure();
subplot(311); hold on; grid();
stem(fd, abs(Yd)); 
xlim([0, pi]);
title('abs(Y(exp(jw))')
xlabel('w');
ylabel('abs(Y(exp(jw)))');
subplot(312); hold on; grid();
stem(fd, abs(Yds));
xlim([0, pi]);
title('abs(Y_p(exp(jw))')
xlabel('w');
ylabel('abs(Y_p(exp(jw)))');
subplot(313); hold on; grid();
stem(fds, abs(Ydb)); 
xlim([0, pi]);
title('abs(Y(exp(jw))')
xlabel('w');
ylabel('abs(Y(exp(jw)))');
