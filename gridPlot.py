import matplotlib.pyplot as plt


# read coordinates from data frame and plot centroids with origin at top left
def plot_points(locations, cell_type, plot_folder):
    x = locations.loc[:, 'Location_Center_X']
    y = locations.loc[:, 'Location_Center_Y']

    plt.scatter(x, y, s=0.1, color='darkblue')
    plt.gca().invert_yaxis()
    plt.xlabel('X Locations')
    plt.ylabel('Y Locations')
    plt.title(cell_type + ' Centroids')
    plt.show()
    plt.savefig(plot_folder + 'Plot' + cell_type + '.png', bbox_inches='tight')
    plt.close()


# read coordinates and plot grid on scatterplot
def grid_plot(locations, xnodes, ynodes, width, height, cell_type, grid_box_size, plot_folder):
    x = locations.loc[:, 'Location_Center_X']
    y = locations.loc[:, 'Location_Center_Y']

    plt.scatter(x, y, s=0.1, color='darkblue')
    plt.gca().invert_yaxis()
    plt.xlabel('X Locations')
    plt.ylabel('Y Locations')
    plt.title(cell_type + ' Centroids with Grid')
    for i in xnodes:
        plt.plot([i, i], [0, width], color='red', alpha=0.9)
    for j in ynodes:
        plt.plot([0, height], [j, j], color='red', alpha=0.9)
    # plt.show()
    # plt.savefig(plot_folder + 'Centroid Grid Plot' + '_' + cell_type + '_' + str(grid_box_size) + 'px.png',
    # bbox_inches='tight')
    plt.close()
