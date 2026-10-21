h=1/10^2*ones(10,10); %FIR paso baja
[H,u,v]=freqz2(h);AH=abs(H); 
figure;imshow(AH,[]);
[uu,vv]=meshgrid(u,v);
figure;mesh(uu,vv,AH/max(AH(:)));
xlabel('u');ylabel('v');zlabel('|H(w)|');


h=-ones(3,3);h(2,2)=8 %FIR laplaciana
[H,u,v]=freqz2(h);AH=abs(H); 
figure;imshow(AH,[]);
[uu,vv]=meshgrid(u,v);
figure;mesh(uu,vv,AH/max(AH(:)));
xlabel('u');ylabel('v');zlabel('|H(w)|');