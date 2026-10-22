%% Superposición Espectro
clear all;
close all;

dt = 0.01;
N = 20;
t = [0:dt:100]';
n = [0:N]';
Ts = 2;
ws = 2*pi/Ts;
wc = 0.95 * ws/2;
xc = cos(wc*t);
xd = cos(wc*Ts*n);

xt = [wc, ws/2, ws];
xl = {'w_c', 'w_s/2', 'w_s'};

if(wc > ws/2)
  if(wc < ws)
    xt = xt([2, 1, 3]);
    xl = xl([2, 1, 3]);
  else
    xt = xt([2, 3, 1]);
    xl = xl([2, 3, 1]);
  end
end

M = length(t);
w = fftshift(fftfreq(M, (dt/(2*pi))));
Xc = fftshift(fft(xc) / M);
Xcabs = abs(Xc);

figure(); hold on;
plot(t, xc);
stem(n*Ts, xd);
xlim(gca, [0, N]);
grid();

figure(); hold on;
plot(w+ws, Xcabs, 'g');
plot(w, Xcabs, 'k');
plot((ws/2)*[-1, -1], [0, 0.5], 'r--');
plot((ws/2)*[1, 1], [0, 0.5], 'r--');
plot(wc*[-1, -1], [0, 0.5], 'b--');
plot(wc*[1, 1], [0, 0.5], 'b--');

xlim(gca, [-10, 10])
xticks(xt);
xticklabels(xl);
%% Funciones 
function w = fftfreq(N, d)
  if(mod(N, 2))
    w = [0:(N-1)/2, -(N-1)/2:-1]' / N;
  else
    w = [0:N/2-1, -N/2:-1]' / N;
  end
  if(d > 0)
    w = w / d;
  end
end