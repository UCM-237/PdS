function e = evaluar(det, ref, fs, tol)
% Sensibilidad (Se) y valor predictivo positivo (VPP) emparejando uno a uno con tolerancia tol (s).
if nargin < 4, tol = 0.15; end
tol = round(tol * fs);
usado = false(size(det)); vp = 0;
for k = 1:numel(ref)
    dd = abs(det - ref(k)); dd(usado) = Inf;
    [m, j] = min(dd);
    if ~isempty(m) && m <= tol, usado(j) = true; vp = vp + 1; end
end
e.VP = vp; e.FN = numel(ref) - vp; e.FP = numel(det) - vp;
e.Se = vp / max(vp + e.FN, 1); e.VPP = vp / max(vp + e.FP, 1);
end
