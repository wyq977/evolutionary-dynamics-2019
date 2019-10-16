import numpy as np
import pylab as pl


def neutral_moran(N, seed=0):
    """
    Return the population counts for the Moran process with neutral drift.
    """
    population = [0 for _ in range(int(N/2))] + [1 for _ in range(int(N/2))]
    counts = [population.count(0)/N]   
    np.random.seed(seed)
    times = 0
    while (times <= 98):
        times += 1
        reproduce_index = np.random.randint(N)
        eliminate_index = np.random.randint(N)
        population[eliminate_index] = population[reproduce_index]
        counts.append(population.count(0)/N)        
    return np.array(counts)


def plot_neutral_moran(N):
    v_1 = (2*0.5*(1-0.5))/(N**2)   
    anal_std=[np.sqrt(v_1)]
    approx_std = [np.sqrt(v_1)]
    times = 0
    while (times <= 98):
        times += 1
        anal_std.append(np.sqrt((v_1*(1-((1-2/(N**2))**times)))/(2/(N**2))))
        approx_std.append(np.sqrt(times*v_1))
    
    
    
    total_traj=[]
    pl.figure()
    for i in range(1000):
        traj = neutral_moran(N,i)
        pl.plot(traj, color = "gray")
        total_traj.append(traj)
    
    
    total_traj = np.array(total_traj)
    emp_mean = np.mean(total_traj, axis = 0)
    emp_std = np.std(total_traj, axis = 0)
    
    
    pl.plot(emp_mean, ls = '-.', color = "red", label='emp.mean')
    pl.plot(emp_std, ls = '-', color = "black", label = 'emp.stdv')
    pl.plot(anal_std, ls = '--', color = "blue", label = 'analyt.stdv')
    pl.plot(approx_std, ls = ':', color = "green", label = 'approx.stdv')
    
    pl.legend(loc = 'upper left', fontsize = 'x-small')
    pl.xlabel("Generation t")
    pl.ylabel("frequency")
    pl.title('N = {}'.format(N))
    pl.savefig("ex3_1d_n_{}.pdf".format(N))

plot_neutral_moran(10)
plot_neutral_moran(100)

















   