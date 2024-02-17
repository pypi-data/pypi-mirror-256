import matplotlib.pyplot as plt
import numpy as np

def plot():

    fig, ax = plt.subplots(nrows=1, ncols=1)

    ax.imshow(np.sin(np.linspace(-np.pi, np.pi, 1000)))
    plt.show()