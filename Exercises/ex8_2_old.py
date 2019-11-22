import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as pl
pl.style.use('classic')

# define the function for neutral moran process
def moran(N, r, time, seed=0):
    population = np.array([0 for _ in range(int(N/2))] + [1 for _ in range(int(N/2))])
    counts = [np.sum(population)/N]   
    np.random.seed(seed)
    times = 1
    while (times < time):
        times += 1
        m = np.sum(population)
        prob_add = ((r*m)/(r*m+N-m))*((N-m)/N)  
        prob_minus = ((N-m)/(r*m+N-m))*(m/N)  
        if_add= np.random.choice(3, 1, p=[prob_minus,prob_add, 1-prob_add-prob_minus])
        if m == N or m == 0:
            eliminate_index = reproduce_index  = 0            
        elif if_add == 1:
            eliminate_index =  np.random.choice(np.where(population == 0)[0], 1)
            reproduce_index =  np.random.choice(np.where(population == 1)[0], 1)
            
        elif if_add == 0:
            eliminate_index =  np.random.choice(np.where(population == 1)[0], 1)
            reproduce_index =  np.random.choice(np.where(population == 0)[0], 1)
        else:
            eliminate_index = reproduce_index  = 0
            
        population[eliminate_index] = population[reproduce_index]
        counts.append(np.sum(population)/N)        
    return np.array(counts)

# define the function for evolution on the specific graph
def graph(N, r, time, seed=0):
    v = np.array([0 for _ in range(int(N/2))] + [1 for _ in range(int(N/2))])
    w = np.zeros((N,N))
    for i in range(N):
        if i == 0:
            w[i,1] = w[i,N-1]=0.5
        elif i == N-1:
            w[i,0] = w[i,N-2]=0.5
        else:            
            w[i, i-1]= w[i, i+1]= 0.5
    counts = [np.sum(v)/N]  
    times = 1
    np.random.seed(seed)                   
    while (times < time):
        times += 1
        m = np.sum(v)
        temp_1 = 0
        temp_2 = 0
        if m != N and m != 0:            
            for i in range(N):
                 for j in range(N):
                     temp_1 += w[i,j]*v[i]*(1-v[j])
                     temp_2 += w[i,j]*v[j]*(1-v[i])
            prob_add = (r*temp_1)/(r*m+N-m)
            prob_minus = temp_2/(r*m+N-m)
            if_add = np.random.choice(3, 1, p=[prob_minus,prob_add, 1-prob_add-prob_minus])
            filter_vector = np.matmul(w, v)
            add_index = np.where((v == 0) & (filter_vector != 0))[0]
            minus_index = np.where((v == 1) & (filter_vector != 1))[0]          
            if if_add == 1: # add
                v[np.random.choice(add_index)] = 1
            elif if_add == 0: # minus
                v[np.random.choice(minus_index)] = 0
            else:
                pass
        else:                   
            pass
            # eliminate_index = reproduce_index  = 0 
                
        counts.append(np.sum(v)/N)  

    return np.array(counts)


def plot_moran(N, r , time, num, fname='moran.png'):
    total_traj = []
    pl.figure()
    for i in range(num):
        traj = moran(N,r,time,i)
        pl.plot(traj, color='red', alpha=0.7)
        total_traj.append(traj)
    pl.xlabel("Generation t")
    pl.ylabel("frequency of type B")
    total_traj = np.array(total_traj)
    p_moran = sum(total_traj[:,(time-1)] == 1)/total_traj.shape[0]
    pl.title('fixation probabiliy with r = {} in Moran process = {}'.format(r, p_moran))
    pl.savefig(fname, dpi=200)
    

def plot_graph(N, r , time, num, fname='graph.png'):
    total_traj = []
    pl.figure()

    for i in range(num):
        traj = graph(N,r,time,i)
        pl.plot(traj, color='red', alpha=0.7)
        total_traj.append(traj)
        
    pl.xlabel("Generation t")
    pl.ylabel("frequency of type B")
    total_traj = np.array(total_traj)
    p_graph= sum(total_traj[:,time-1] == 1)/total_traj.shape[0]
    pl.title('fixation probabiliy with r = {} in evolution on graph = {}'.format(r, p_graph))
    pl.savefig(fname, dpi=200)
        
        

                
# plot the the trajectory of the process as well as the mean and std
if __name__ == "__main__":
    # N = 20, r = 1/1.1, t = 2000, num_simulation = 1000
    plot_graph(20, 1.1 , 200, 100)
    plot_moran(20, 1.1 , 200, 100)
