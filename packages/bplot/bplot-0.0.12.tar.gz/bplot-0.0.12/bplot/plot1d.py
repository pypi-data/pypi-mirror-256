import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse
import json
import sys

def __read_data(path):
    return pd.read_csv(path)


def main():
    '''
        Plot 1D variables

        Arguments
        ---------
        - -p/--path [required]: path of the pandas-readable file from where to load the data
        - -x/--xvar [optional]: name of the variable in the pandas-readable file to be used for the x-axis
        - -y/--yvar [optional]: name of the variable in the pandas-readable file to be used for the y-axis
        - -g/--grid [optional]: if True it will add grids to the plot
        - -t/--hist [optional]: if True it will add the histogram to the plot
    '''


    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', required=True,   action="store", help='Path to file')
    parser.add_argument('-x', '--xvar', default=None,    action="store", help='Variable for x-axis')
    parser.add_argument('-y', '--yvar', default=None,    action="store", help='Variable for y-axis')
    parser.add_argument('-g', '--grid', default='False', action="store", help='Activate Grid')
    parser.add_argument('-t', '--hist', default='False', action="store", help='Plot histogram')
    args = parser.parse_args()

    # Arguments    
    data = __read_data(args.path)
    xvar = args.xvar
    yvar = args.yvar
    grid = json.loads(args.grid.lower())
    hist = json.loads(args.hist.lower())

    # Plot with histogram
    if hist:
        _, ax = plt.subplots(nrows=1, ncols=2, gridspec_kw={'width_ratios': [3,1]})

        if xvar is not None and yvar is not None: 
            ax[0].plot(data[xvar], data[yvar])
            ax[1].hist(data[yvar], 200, orientation='horizontal')
        elif xvar is not None and yvar is None:   
            ax[0].plot(data[xvar], data)
            ax[1].hist(data, 200, orientation='horizontal')
        elif xvar is None and yvar is not None:   
            ax[0].plot(data[yvar])
            ax[1].hist(data, 200, orientation='horizontal')
        else:                                     
            ax[0].plot(data)
            ax[1].hist(data, 200, orientation='horizontal')
    # Plot without histogram
    else:
        _, ax = plt.subplots(nrows=1, ncols=1)

        if xvar is not None and yvar is not None: ax.plot(data[xvar], data[yvar])
        elif xvar is not None and yvar is None:   ax.plot(data[xvar], data)
        elif xvar is None and yvar is not None:   ax.plot(data[yvar])
        else:                                     ax.plot(data)
    if grid: ax.grid()



    plt.show()


if __name__ == '__main__':
    main()