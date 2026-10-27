n = 0:199;
s = double(n >= 100);         % escalón
x = s + 0.05*randn(1, 200);
i = [31 32 141];
x(i) = x(i) + [2 2 -2];         % impulsos
L = 7;                          % 2K+1
media = conv(x, ones(1, L)/L, 'same');
med = medfilt1(x, L);
for y = {media, med}
  e = abs(y{1} - s);
  disp(max(e(21:180)))          % error
end
