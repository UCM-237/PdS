N=100
F=zeros(N,N);
for i=1:N
    for j=1:N
        if (i-N/2)^2+(j-N/2)^2<10^2
            F(i,j)=1;
        end
    end
end
x=linspace(-1,1,N);
[uu,vv]=meshgrid(x,x);
figure;mesh(uu,vv,F);
xlabel('u');ylabel('v');zlabel('|H(w)|');


N=100
F=ones(N,N);
for i=1:N
    for j=1:N
        if (i-N/2)^2+(j-N/2)^2<10^2
            F(i,j)=0;
        end
    end
end
x=linspace(-1,1,N);
[uu,vv]=meshgrid(x,x);
figure;mesh(uu,vv,F);
xlabel('u');ylabel('v');zlabel('|H(w)|');


N=100
F=zeros(N,N);
for i=1:N
    for j=1:N
        if ((i-N/2)^2+(j-N/2)^2>10^2)&&((i-N/2)^2+(j-N/2)^2<20^2)
            F(i,j)=1;
        end
    end
end
x=linspace(-1,1,N);
[uu,vv]=meshgrid(x,x);
figure;mesh(uu,vv,F);
xlabel('u');ylabel('v');zlabel('|H(w)|');


N=100
F=ones(N,N);
for i=1:N
    for j=1:N
        if ((i-N/2)^2+(j-N/2)^2>10^2)&&((i-N/2)^2+(j-N/2)^2<20^2)
            F(i,j)=0;
        end
    end
end
x=linspace(-1,1,N);
[uu,vv]=meshgrid(x,x);
figure;mesh(uu,vv,F);
xlabel('u');ylabel('v');zlabel('|H(w)|');

