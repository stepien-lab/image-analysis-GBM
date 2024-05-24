import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time


#%% Read coordinates from data frame and plot centroids with origin at top left
def plot_points(locations, cell_type, plot_folder, mouse_section_id):
    x = locations.loc[:, 'Location_Center_X']
    y = locations.loc[:, 'Location_Center_Y']

    plt.scatter(x, y, s=0.1, color='darkblue')
    plt.gca().invert_yaxis()
    plt.xlabel('X Locations (um)')
    plt.ylabel('Y Locations (um)')
    plt.title('Mouse ' + mouse_section_id + ' ' + cell_type + ' Centroids')
    plt.savefig(plot_folder + mouse_section_id + '_' + cell_type + '_plot.png', bbox_inches='tight')
    plt.show()
    plt.close()


#%% Read coordinates and plot grid on scatterplot
def grid_plot(locations, xnodes, ynodes, width, height, cell_type, grid_box_size, plot_folder, mouse_section_id):
    x = locations.loc[:, 'Location_Center_X']
    y = locations.loc[:, 'Location_Center_Y']

    plt.scatter(x, y, s=0.1, color='darkblue')
    plt.gca().invert_yaxis()
    plt.xlabel('X Locations (um)')
    plt.ylabel('Y Locations (um)')
    plt.title('Mouse ' + mouse_section_id + ' ' + cell_type + ' Centroids with ' + str(grid_box_size) + ' um Grid')
    for i in xnodes:
        plt.vlines(x=i, ymin=0, ymax=height, color='red', alpha=0.9)
    for j in ynodes:
        plt.hlines(y=j, xmin=0, xmax=width, color='red', alpha=0.9)
    plt.savefig(plot_folder + mouse_section_id + '_' + cell_type + '_' + str(grid_box_size) + '_um_plot.png',
                bbox_inches='tight')
    plt.show()
    plt.close()


#%% Create grid to use for all images
def make_grid(image_width, image_height, grid_box_size_um):
    x_nodes = [0]
    y_nodes = [0]

    # create nodes that are a specified width apart
    while x_nodes[-1] + grid_box_size_um < image_width:
        x_nodes = np.append(x_nodes, [x_nodes[-1] + grid_box_size_um])

    # create nodes that are a specified height apart
    while y_nodes[-1] + grid_box_size_um < image_height:
        y_nodes = np.append(y_nodes, [y_nodes[-1] + grid_box_size_um])

    # add final nodes at image boundaries
    x_nodes = np.append(x_nodes, [image_width])
    y_nodes = np.append(y_nodes, [image_height])

    return [x_nodes, y_nodes]


#%% Return dataframe with centroid locations sorted onto grid
def grid_sort(locations, xnodes, ynodes):
    # sort data into bins based on x and y coordinates
    locations['X_Bin'] = pd.cut(x=locations.loc[:, 'Location_Center_X'], bins=xnodes)
    locations['Y_Bin'] = pd.cut(x=locations.loc[:, 'Location_Center_Y'], bins=ynodes)
    boxes = locations.groupby(['X_Bin', 'Y_Bin'], observed=False).count()

    # check accuracy of count total
    total = boxes['Location_Center_X'].sum()
    if total != locations.shape[0]:
        print('Warning: grid sum does not match expected total!')
    return boxes


#%% Calculate and display density
def density(grid_box_size, boxes):
    # average density
    area = grid_box_size ^ 2
    av_density = boxes['Location_Center_X'].mean() / area
    return av_density


#%% Use above functions to follow data analysis workflow for each cell types in image set
def analyze(image, grid, grid_box_size, density_data, cell_type, width, height, data_folder, plot_folder,
            mouse_section_id):
    # plotting and data analysis
    plot_points(image, cell_type, plot_folder, mouse_section_id)
    grid_plot(image, grid[0], grid[1], width, height, cell_type, grid_box_size, plot_folder, mouse_section_id)
    image_data = grid_sort(image, grid[0], grid[1])
    av_density = density(grid_box_size, image_data)

    # export to spreadsheet
    file_name = 'GridSort' + '_' + cell_type + '_' + mouse_section_id + '_' + str(grid_box_size) + 'px.xlsx'
    image_data.to_excel(data_folder + file_name)

    # add density data to dataframe
    density_data.loc[len(density_data)] = [cell_type, grid_box_size, av_density]
    time.sleep(5)


#%% Import data and run analysis for three cell types in each data set
def image_set(data_folder, plot_folder, mouse_section_id):
    # import x and y locations of cancer cells from CellProfiler .csv file
    cancer_data = pd.read_csv(mouse_section_id+'_Data_CancerCells.csv', usecols=['Location_Center_X',
                                                                                 'Location_Center_Y'])
    cancer_data_px = cancer_data.mul(0.62)

    # import x and y locations of MDSCs from CellProfiler .csv file
    mdsc_data = pd.read_csv(mouse_section_id+'_Data_MDSC.csv', usecols=['Location_Center_X', 'Location_Center_Y'])
    mdsc_data_px = mdsc_data.mul(0.62)

    # import x and y locations of CD3 from CellProfiler .csv file
    cd3_data = pd.read_csv(mouse_section_id+'_Data_CD3.csv', usecols=['Location_Center_X', 'Location_Center_Y'])
    cd3_data_px = cd3_data.mul(0.62)

    # import image sizes and convert to um
    image_sizes = pd.read_csv(mouse_section_id+'_Data_Image.csv', usecols=['Height_DAPI', 'Width_DAPI'])
    # image scale: .62 um/px
    height = image_sizes.loc[0, 'Height_DAPI']*0.62
    width = image_sizes.loc[0, 'Width_DAPI']*0.62

    # choose multiple grid sizes
    grid_box_size_um = [1000, 500, 250]

    for size in grid_box_size_um:
        # create grid for to use for all images
        grid = make_grid(width, height, size)
        # create spreadsheet for density data
        density_data = pd.DataFrame(columns=['Cell Type', 'Grid Box Size (um)', 'Density'])
        # analyze images
        analyze(cancer_data_px, grid, size, density_data, 'CancerCell', width, height, data_folder,
                plot_folder, mouse_section_id)
        analyze(mdsc_data_px, grid, size, density_data, 'MDSC', width, height, data_folder, plot_folder, mouse_section_id)
        analyze(cd3_data_px, grid, size, density_data, 'CD3', width, height, data_folder, plot_folder, mouse_section_id)
        # save density data as spreadsheet
        density_data.to_excel(data_folder + 'AverageDensity' + '_' + mouse_section_id + '_' + str(size) + 'um.xlsx')
        print(mouse_section_id + ' ' + str(size) + ' um sort complete!')
