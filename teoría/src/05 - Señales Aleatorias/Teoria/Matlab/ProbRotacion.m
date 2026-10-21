x1=0:0.1:10;x2=0:0.1:10;[X1,X2]=meshgrid(x1,x2);
P=zeros(size(X1));
ang=0; %Orientacion
mu=[6,4];diag=[1 0;0 9];
rot=[cos(ang),sin(ang);
    -sin(ang),cos(ang)];
sigma=rot*diag*rot'
invsigma=inv(sigma);
coeff=1/2/pi/sqrt(det(sigma));
for i=1:length(x1)*length(x2)
    xvec=[X1(i),X2(i)]; xdif=xvec-[6,4];
    aux=xdif*invsigma*xdif';
    P(i)=coeff*exp(-aux/2);
end
mesh(X1,X2,P);xlabel('x');ylabel('y');