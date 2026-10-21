n=0:1:10;
secuencias=[];
for l=1:50 %Bucle para varios procesos
x=0+sqrt(0.1)*randn(1);
for i=2:length(n)
    x(i)=x(:,i-1)+sqrt(0.25)*randn(1);    
end
secuencias=[secuencias;x];
end
plot(n,secuencias,'LineWidth',2)
xlabel('n');ylabel('x(n)')