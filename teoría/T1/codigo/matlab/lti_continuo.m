RC = 1e-3;                     % 1 kΩ, 1 µF
H = tf(1, [RC 1]);             % 1/(RC s + 1)
disp(pole(H))                  % -1000
[s, t] = step(H);              % escalón
[mag, fase, W] = bode(H);
