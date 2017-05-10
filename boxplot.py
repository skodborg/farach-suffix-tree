import matplotlib.pyplot as plt
import numpy as np



def load_file(aFilename):
    return np.genfromtxt(aFilename, delimiter=',')

def gen_boxplot(aFilename):
    data = load_file(aFilename)
    print(data[:3])

    data_to_plot = [data for data in np.delete(data, 0, 1)]
    # print('DELETED:')
    # print(_data[:3])


    # lol = [x for x in data_to_plot]

    # Create a figure instance
    fig = plt.figure(1, figsize=(9, 6))

    # Create an axes instance
    ax = fig.add_subplot(111)

    # Create the boxplot
    # bp = ax.boxplot(data_to_plot, 0, '')  # no outliers shown
    bp = ax.boxplot(data_to_plot)

    # Save the figure
    fig.savefig('fig1.png', bbox_inches='tight')


def main():
    # print('type file name of file with data points:')
    # filename = input()
    filename = 'testData/noise.txt'
    gen_boxplot(filename)

if __name__ == '__main__':
    main()
