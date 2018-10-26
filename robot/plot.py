import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

def create_plot(data,filename):
    for d in data: print(d)
    density = stats.gaussian_kde(data)
    start = 0
    end = 24
    #_, x, _ = plt.hist(data, bins=np.linspace(start, end, 100), 
    #                   histtype=u'step', normed=True)  
    x = np.arange(start, end, 0.001)
    plt.fill_between(x, 0, density(x), facecolor='green')
    plt.savefig(filename)
    plt.close()
