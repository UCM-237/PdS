n = 0:31;
x1 = cos(pi/4 * n);            % π/4
x2 = cos(7*pi/4 * n);          % 2π - π/4
x3 = cos(9*pi/4 * n);          % π/4 + 2π
disp(max(abs(x1 - x2)))        % ≈ 0
disp(max(abs(x1 - x3)))        % ≈ 0
