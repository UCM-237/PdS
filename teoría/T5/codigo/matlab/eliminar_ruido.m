N = 1024; n = 0:N-1;
x = 1.5*(n > 100) - 2.2*(n > 240) ...
    + 1.6*(n > 410) + 1.2*(n > 512);
y = x + 0.4*randn(1, N);
J = 5; c = cell(1, J+1); a = y;
for j = 1:J
  c{j} = (a(1:2:end)-a(2:2:end))/sqrt(2);
  a = (a(1:2:end)+a(2:2:end))/sqrt(2);
end
s = median(abs(c{1}))/0.6745;     % sigma
u = s*sqrt(2*log(N));             % umbral
for j = J:-1:1                    % duro
  d = c{j}.*(abs(c{j}) > u);
  z = zeros(1, 2*numel(a));
  z(1:2:end) = (a + d)/sqrt(2);
  z(2:2:end) = (a - d)/sqrt(2);
  a = z;
end
rms = @(e) sqrt(mean(e.^2));
disp([s u])                      % 0.40 1.49
disp([rms(y-x) rms(a-x)])        % 0.40 0.12
