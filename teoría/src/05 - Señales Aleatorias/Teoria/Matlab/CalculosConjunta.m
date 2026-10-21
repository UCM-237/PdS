%Muestreo
N=100000;
x=2+2*rand(N,1);
y=x+randn(N,1);
samples=[x,y];
%Caracterizacion
%Histograma
hist3(samples,[30,50])
xlabel('x');ylabel('y')
%Estadisticos
m=mean(samples) %Media
%Valor cuadratico medio
m2=mean(samples.*samples)
%Matriz de covarianza
sigma2=cov(samples,1) 
%Correlacion cruzada
correlacion=mean(x.*y)
%Coeficiente de correlacion
rho=corr(samples) 
