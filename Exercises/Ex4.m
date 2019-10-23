function Ex4

close all % close all previous graphics
clear all % clear the values of all variables

% Mechanism (b)
clear p x0
p(1) = 1e-7;
p(2) = 1e-8;
x0 = [1 0 0];
tspan = [0 1e6];

[t, x] = ode45(@mech ,tspan ,x0 ,[] ,p);

for i = 1:3
    disp(['x_' num2str(i) ': ' num2str(x(end,i))]) ;
end


figure(1)

hold on

plot (t , x)
legend ({'X_0', 'X_1', 'X_2'})
xlabel ('Time')
fig = gcf;
fig.PaperPositionMode = 'auto';
print('numerical','-dpng')
end



function dxdt_b = mech(t, x, p)
N = 100;
k1 = p(1);
k2 = p(2);
dxdt_b = zeros(3,1);
dxdt_b(1) = -k1 * x(1); % X_1
dxdt_b(2) = k1 * x(1) - N * k2 * x(2); % X_2
dxdt_b(3) = N * k2 * x(2);  % X_3
end

