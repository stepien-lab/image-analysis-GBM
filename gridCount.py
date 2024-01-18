import pandas as pd
import numpy as np


# create grid to use for all images
def make_grid(image_width, image_height, grid_box_size_px):
    x_nodes = [0]
    y_nodes = [0]

    # create nodes that are a specified width apart
    while x_nodes[-1] + grid_box_size_px < image_width:
        x_nodes = np.append(x_nodes, [x_nodes[-1] + grid_box_size_px])

    # create nodes that are a specified height apart
    while y_nodes[-1] + grid_box_size_px < image_height:
        y_nodes = np.append(y_nodes, [y_nodes[-1] + grid_box_size_px])

    # add final nodes at image boundaries
    x_nodes = np.append(x_nodes, [image_width])
    y_nodes = np.append(y_nodes, [image_height])

    return [x_nodes, y_nodes]


# return dataframe with centroid locations sorted onto grid
def grid_sort(locations, xnodes, ynodes):
    # sort data into bins based on x and y coordinates
    locations['X_Bin'] = pd.cut(x=locations.loc[:, 'Location_Center_X'], bins=xnodes)
    locations['Y_Bin'] = pd.cut(x=locations.loc[:, 'Location_Center_Y'], bins=ynodes)
    boxes = locations.groupby(['X_Bin', 'Y_Bin']).count()

    # check accuracy of count total
    total = boxes['Location_Center_X'].sum()
    print(total, locations.shape[0])
    if total != locations.shape[0]:
        print('Warning: grid sum does not match expected total!')
    return boxes


# calculate and display density
def density(grid_box_size, boxes):
    # average density
    area = grid_box_size^2
    av_density = boxes['Location_Center_X'].mean()/area
    return av_density
