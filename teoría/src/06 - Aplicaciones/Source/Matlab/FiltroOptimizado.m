N=40;
Hd=zeros(N); %Filtro no pasa frecuencias
[u,v]=freqspace(N); %Frecuencias normalizadas
[uu,vv]=meshgrid(u,v);
Duv=uu.^2+vv.^2; %Matriz radial
Hd(Duv>.3 &Duv<.5)=1; %FIR paso banda [0.3 y 0.5]
h=fsamp2(Hd); %Nucleo de convolucion
%Respuesta en frecuencia
[H,uu2,vv2]=freqz2(h); %Frecuencias normalizadas
subplot(2,1,1);mesh(uu2,vv2,abs(H));
subplot(2,1,2);mesh(uu,vv,Hd);

