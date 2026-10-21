% Tarea 3
clear; close all;
set(groot, 'DefaultFigureWindowStyle', 'docked');
x = DatosTarea3();

save('datos.mat');

figure(1);
  histogram(x(:,1), 30);

figure(2);
  histogram(x(:,2));

figure(3);
  histogram(x(:,3));
