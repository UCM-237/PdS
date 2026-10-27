ref = [100 300 500 700 900];  % verdad
det = [102 298 450 705 898 960];
tol = 10;
libres = ref; vp = 0;
for d = det
  [dmin, i] = min(abs(libres - d));
  if ~isempty(i) && dmin <= tol
    libres(i) = [];  % el más cercano, una vez
    vp = vp + 1;
  end
end
fp = numel(det) - vp;
fn = numel(libres);
Se = vp/(vp + fn); VPP = vp/(vp + fp);
F1 = 2*Se*VPP/(Se + VPP);
disp([vp fp fn Se VPP F1])
