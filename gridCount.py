import pandas as pd
import numpy as np


# create grid to use for all images
def make_grid(width, height):
    # get grid size from user input
    rows = int(input("Enter number of grid rows: "))
    columns = int(input("Enter numer of grid columns: "))

    # create grid
    xnodes = np.linspace(0, width, num=columns + 1)
    ynodes = np.linspace(0, height, num=rows + 1)

    return [xnodes, ynodes, rows, columns]


# return dataframe with centroid locations sorted onto grid
def grid_sort(locations, xnodes, ynodes):
    # sort data into bins based on x and y coordinates
    locations['X_Bin'] = pd.cut(x=locations.loc[:, 'Location_Center_X'], bins=xnodes)
    locations['Y_Bin'] = pd.cut(x=locations.loc[:, 'Location_Center_Y'], bins=ynodes)
    boxes = locations.groupby(['X_Bin', 'Y_Bin']).count()

    # check accuracy of count total
    total = boxes['Location_Center_X'].sum()
    if total != locations.shape[0]:
        print('Warning: grid sum does not match expected total!')

    return boxes


# calculate and display density
def density(width, height, rows, columns, boxes):
    # average density
    area = width*height/columns/rows
    av_density = boxes['Location_Center_X'].mean()/area
    return av_density
