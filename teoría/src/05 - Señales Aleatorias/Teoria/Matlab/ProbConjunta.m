x1=0:0.1:10;x2=0:0.1:10;
[X1,X2]=meshgrid(x1,x2);
P=exp(-(X2-X1).^2/2)/sqrt(2*pi)/2
P(X1<2)=0;P(X1>4)=0;
mesh(X1,X2,P);
xlabel('x');ylabel('y');


