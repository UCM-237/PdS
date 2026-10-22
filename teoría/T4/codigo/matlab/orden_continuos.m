wp = 2*pi*1e3; ws = 2*pi*5e3;
ap = 1; as = 40;
N1 = buttord(wp, ws, ap, as, 's')   % 4
N2 = cheb1ord(wp, ws, ap, as, 's')  % 3
N3 = cheb2ord(wp, ws, ap, as, 's')  % 3
N4 = ellipord(wp, ws, ap, as, 's')  % 3
% Rizado de la banda de paso (ap) antes
% que la atenuación (as):
[b, a] = cheby1(3, ap, wp, 's');
[b, a] = cheby2(3, as, ws, 's');
[b, a] = ellip(3, ap, as, wp, 's');
