import matplotlib.pyplot as plt
import numpy as np
import argparse



def plot1d(args):
    grid = args.grid

    fig, ax = plt.subplots(nrows=1, ncols=1)

    ax.plot(np.sin(np.linspace(-np.pi, np.pi, 1000)))


    if grid: ax.grid()

    plt.show()





if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument('--grid', type=bool, default=True, help='Add grid to the plot')
    args = parser.parse_args()


    plot1d(args)



    