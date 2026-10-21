x = [1 2 1];                 % n = 0..2
h = [1 1 1 1];               % n = 0..3
y = conv(x, h);              % n = 0..5
disp(y)                      % 1 3 4 4 3 1
disp(length(y) == length(x) + length(h) - 1)
