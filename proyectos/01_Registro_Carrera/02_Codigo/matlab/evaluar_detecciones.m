function [tp, fp, fn] = evaluar_detecciones(det, reales, tol)
% Empareja cada instante real con el detectado más cercano a menos de tol segundos (20 por defecto).
if nargin < 3, tol = 20; end
det = sort(det(:))'; tp = 0;
for r = reales(:)'
    if isempty(det), break; end
    [dmin, j] = min(abs(det - r));
    if dmin <= tol, det(j) = []; tp = tp + 1; end
end
fp = numel(det); fn = numel(reales) - tp;
end
