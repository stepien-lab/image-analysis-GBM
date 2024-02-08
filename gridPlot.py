import matplotlib.pyplot as plt


# read coordinates from data frame and plot centroids with origin at top left
def plot_points(locations, cell_type, plot_folder, mouse_section_id):
    x = locations.loc[:, 'Location_Center_X']
    y = locations.loc[:, 'Location_Center_Y']

    plt.scatter(x, y, s=0.1, color='darkblue')
    plt.gca().invert_yaxis()
    plt.xlabel('X Locations')
    plt.ylabel('Y Locations')
    plt.title('Mouse ' + mouse_section_id + ' ' + cell_type + ' Centroids')
    plt.savefig(plot_folder + mouse_section_id + '_' + cell_type + '_plot.png', bbox_inches='tight')
    plt.show()
    plt.close()


# read coordinates and plot grid on scatterplot
def grid_plot(locations, xnodes, ynodes, width, height, cell_type, grid_box_size, plot_folder, mouse_section_id):
    x = locations.loc[:, 'Location_Center_X']
    y = locations.loc[:, 'Location_Center_Y']

    plt.scatter(x, y, s=0.1, color='darkblue')
    plt.gca().invert_yaxis()
    plt.xlabel('X Locations')
    plt.ylabel('Y Locations')
    plt.title('Mouse ' + mouse_section_id + ' ' + cell_type + ' Centroids with ' + str(grid_box_size) + ' px Grid')
    for i in xnodes:
        plt.vlines(x=i, ymin=0, ymax=height, color='red', alpha=0.9)
    for j in ynodes:
        plt.hlines(y=j, xmin=0, xmax=width, color='red', alpha=0.9)
    plt.savefig(plot_folder + mouse_section_id + '_' + cell_type + '_' + str(grid_box_size) + '_px_plot.png',
                bbox_inches='tight')
    plt.show()
    plt.close()
