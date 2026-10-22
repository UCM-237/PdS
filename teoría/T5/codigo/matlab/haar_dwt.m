n = 0:1023;
x = sin(2*pi*n/512) + (n > 300);
J = 4; c = cell(1, J+1); a = x;
for j = 1:J                      % análisis
  c{j} = (a(1:2:end)-a(2:2:end))/sqrt(2);
  a = (a(1:2:end)+a(2:2:end))/sqrt(2);
end
c{J+1} = a;
disp(cellfun(@numel, c))        % 512 ... 64
E = cellfun(@(v) sum(v.^2), c);
disp([E, sum(x.^2)])             % Parseval
for j = J:-1:1                   % síntesis
  y = zeros(1, 2*numel(a));
  y(1:2:end) = (a + c{j})/sqrt(2);
  y(2:2:end) = (a - c{j})/sqrt(2);
  a = y;
end
disp(max(abs(a - x)))            % ~1e-15
