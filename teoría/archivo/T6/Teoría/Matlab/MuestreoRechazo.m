function x=MuestreoRechazo(N)

x=[];
M=2; %Valor de M
hm=0;
while hm<N
  y=rand(N-hm,1);
  xp=rand(N-hm,1); %Muestras q(x)
  l=find(y*M.*q(xp)-p(xp)<0)
  x=[x;xp(l)];
  hm=length(x)   
end

function val=q(x)
%Densidad prob. q(x)
val=1;

function val=p(x)
%Densidad prob.  p(x)
val=2*x;


