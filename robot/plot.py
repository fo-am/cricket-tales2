import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

def create_plot(data,filename):
    density = stats.gaussian_kde(data)
    start = 0
    end = 24
    #_, x, _ = plt.hist(data, bins=np.linspace(start, end, 100), 
    #                   histtype=u'step', normed=True)  
    x = np.arange(start, end, 0.001)
    plt.fill_between(x, 0, density(x), lw=2, facecolor='yellow')
    plt.axis('off')
    #plt.setp(x, linewidth=2)
    plt.savefig(filename, transparent=True)
    plt.close()
