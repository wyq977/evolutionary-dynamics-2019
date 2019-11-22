import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as pl
pl.style.use('classic')

def moran(N, r, time, seed=0):
    """Simulate a 2-state Moran process

    The state space only consists of `[0, 1]` with relative fitness `r`.

    Parameters
    ----------
    N : int
        The number of individuals.
    r : float
        Relative fitness of type 1 to type 0.
    time : int
        Steps/index for simulation.
    seed : int
        Random seed.

    Returns
    -------
    numpy.array
        A 1-D array of shape `(time, )` of the fraction (percentage) of type `1` 
        in the population.

    """
    assert N % 2 == 0, 'Individuals must be even !'
    m = N // 2 # population of type 1
    np.random.seed(seed)

    counts = np.ones(time)
    for i in range(time):

        prob_add   =  r * m  / (r * m + N - m) * (N - m) / N
        prob_minus = (N - m) / (r * m + N - m) *       m / N
        add_num = np.random.choice(
            [-1, 1, 0], 1, p=[prob_minus, prob_add, 1 - prob_add - prob_minus])
        m += int(add_num)
        counts[i] = m / N

    return counts


def init_graph_weight_matrix(N):
    """Helper function to init. the transition matrix on a bi-directional graph"""
    w = np.zeros((N, N))
    for i in range(N):
        if i == 0:
            w[i, 1] = w[i, N - 1] = 0.5
        elif i == N - 1:
            w[i, 0] = w[i, N - 2] = 0.5
        else:
            w[i, i - 1] = w[i, i + 1] = 0.5
    return w

def graph(N, r, time, seed=0):
    """Simulate a 2-state evolution on a bi-directional graph process

    The state space only consists of `[0, 1]` with relative fitness `r`.

    Parameters
    ----------
    N : int
        The number of individuals.
    r : float
        Relative fitness of type 1 to type 0.
    time : int
        Steps/index for simulation.
    seed : int
        Random seed.

    Returns
    -------
    numpy.array
        A 1-D array of shape `(time, )` of the fraction (percentage) of type `1` 
        in the population.

    """
    assert N % 2 == 0, 'Individuals must be even !'
    m = N // 2 # population of type 1
    np.random.seed(seed)
    w = init_graph_weight_matrix(N)
    v = np.concatenate((np.zeros(N // 2), np.ones(N // 2)), axis=None)
    filter_vector = np.matmul(w, v)

    counts = np.ones(time)

    for i in range(time):
        v_out = np.outer(v, 1 - v)
        v_out_alt = np.outer(1 - v, v)

        v_w = np.sum(np.multiply(v_out, w), axis=None)
        v_w_alt = np.sum(np.multiply(v_out_alt, w), axis=None)

        m = np.sum(v)

        prob_add = r * v_w / (r * m + N - m)
        prob_minus = v_w_alt / (r * m + N - m)

        # filter_vector = w * v should return a (N, ) vector
        # if 0 < filter_vector < 1:
        # if the elements in filter_vector is < 1 and > 0
        # the elements can switch state
        filter_vector = np.matmul(w, v)
        random_number = np.random.rand()
        if random_number < prob_add:
            # conditioning on zeros
            index = np.where((v == 0) & (filter_vector != 0))[0]
            index_chosen = np.random.choice(index)
            v[index_chosen] = 1
        elif random_number < (prob_add + prob_minus):
            # conditioning on ones
            index = np.where((v == 1) & (filter_vector != 1))[0]
            index_chosen = np.random.choice(index)
            v[index_chosen] = 0
        else:
            pass

        counts[i] = np.sum(v)

    return counts

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
    plot_graph(20, 1.1 , 200, 100, 'graph_new.png')
    plot_moran(20, 1.1 , 200, 100, 'moran_new.png')
