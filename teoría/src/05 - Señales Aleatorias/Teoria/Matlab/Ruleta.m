p=[0.1,0.3,0.2,0.4];
cump=cumsum(p);
N=1000;

for i=1:N
    v(i)=rand(1);
    x(i)=sum(v(i)>cump)+1;
end
