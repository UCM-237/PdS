function x=MuestreoRechazo(N,m,c)

x=[];
M=4.5; %Valor de M

hm=0;
while hm<N
  y=rand(N-hm,1);
  xp=m/2+c*10*randn(N-hm,1); %Muestras q(x)
  l=find(y*M.*q(xp,m,c)-p(xp,m,c)<0);
  x=[x;xp(l)];
  hm=length(x);   
end



function val=q(x,m,c)
%Densidad prob. q(x)
val=normpdf(x,m/2,c*10);

function val=p(x,m,c)
%Densidad prob.  p(x)

val=lognpdf(x,m,c);


