function s = ssim_medio(x, ref)
% SSIM medio (Wang et al., 2004) con ventana gaussiana σ = 1,5 (radio 5), L = 1.
x = min(max(x, 0), 1);
n = -5:5; h = exp(-n.^2 / (2 * 1.5^2)); h = h / sum(h);
f = @(a) filtrar_sep(a, h, h);
c1 = 0.01^2; c2 = 0.03^2;
mx = f(x); my = f(ref);
vx = f(x .* x) - mx.^2; vy = f(ref .* ref) - my.^2; cxy = f(x .* ref) - mx .* my;
m = ((2 * mx .* my + c1) .* (2 * cxy + c2)) ./ ((mx.^2 + my.^2 + c1) .* (vx + vy + c2));
s = mean(m(:));
end
