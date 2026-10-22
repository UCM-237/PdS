%Muestreo de la señal
data=[];
hm=10000; %Numero de señales
N=1000;     %Longitud de la señal
%for i=1:hm
%x=3+2*randn(1,N);
%data(end+1,:)=x;
%end
%Como la señal es muy sencilla puedo generarlo todo 
%de forma matricial.
data=3+2*randn(hm,N);

aux=zeros(N,N);
%Matriz de autocorrelación, para señales genéricas
for i=1:N
    for j=i:N
        aux(i,j)=mean(data(:,i).*data(:,j));
        aux(j,i)=aux(i,j);
    end
end

%Dibujo de la autocorrelación que está almacenada en la matriz
n=1:N
for i=1:10:N %No dibujo todas las curvas, son muchas, 1 de cada 10 ...
   plot(n-i,aux(i,:))
   hold on;
end

%Si la señal es ergódica, podemos calcular la autocorrelación
%con una secuencia de la señal (por ejemplo, la primera secuencia)
%Sin embargo, es bueno que la secuencia sea suficientemente larga
%Por eso genero más datos para la primera secuencia
%Podría hacer N más grande en la parte superior del código,
%pero entonces el bucle del calculo de aux se hace muy lento. 
N=N*10;
data=3+2*randn(1,N);

[auto,lags]=xcorr(data(1,:),N/10,'unbiased');
plot(lags,auto,'o');
      
