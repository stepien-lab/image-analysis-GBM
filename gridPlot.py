import matplotlib.pyplot as plt


# read coordinates from data frame and plot centroids with origin at top left
def plot_points(locations):
    x = locations.loc[:, 'Location_Center_X']
    y = locations.loc[:, 'Location_Center_Y']

    plt.scatter(x, y, s=0.1, color='darkblue')
    plt.gca().invert_yaxis()
    plt.xlabel('X Locations')
    plt.ylabel('Y Locations')
    plt.title('Cell Centroids')
    plt.show()


# read coordinates and plot grid on scatterplot
def grid_plot(locations, xnodes, ynodes):
    x = locations.loc[:, 'Location_Center_X']
    y = locations.loc[:, 'Location_Center_Y']

    plt.scatter(x, y, s=0.1, color='darkblue')
    plt.gca().invert_yaxis()
    plt.xlabel('X Locations')
    plt.ylabel('Y Locations')
    plt.title('Cell Centroids with Grid')
    for i in xnodes:
        plt.plot([i, i], [0, 3657], color='red', alpha=0.9)
    for j in ynodes:
        plt.plot([0, 3653], [j, j], color='red', alpha=0.9)
    plt.show()
