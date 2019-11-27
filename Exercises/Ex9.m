function Ex9

close all % close all previous graphics
clear all % clear the values of all variables

L = 10;
x = linspace(0,L,200);
t = linspace(0,1e3,200);

m = 0;
sol = pdepe(m,@heatpde,@heatic,@heatbc,x,t);

colormap hot
imagesc(x,t,sol)
colorbar
xlabel('x','interpreter','latex')
ylabel('Time t','interpreter','latex')
title('$0 \le x \le L$ and $0 \le t \le 10^3$','interpreter','latex')
fig = gcf;
fig.PaperPositionMode = 'auto';
print('ex9_2d','-dpng')
end

function [c,f,s] = heatpde(x,t,u,dudx)
m = 0.3;
mu = 0.5;
l = 1;
D = mu * m * l^2 / 2;

c = 1/D;
f = dudx;
s = 0;
end

function u0 = heatic(x)
u0 = 0;
end

function [pl,ql,pr,qr] = heatbc(xl,ul,xr,ur,t)
pl = ul;
ql = 0;
pr = ur - 1;
qr = 0;
end


