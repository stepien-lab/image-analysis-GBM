# This program imports location data from Cell Profiler, creates a grid,
# and obtains counts within each grid box
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None  # default='warn'

# import x and y locations of each primary object from CellProfiler csv file
fullLocations = pd.read_csv('Counts_Cells.csv', usecols=['ImageNumber', 'ObjectNumber',
                                                   'Location_Center_X', 'Location_Center_Y'])

# limit data frame to one image and create coordinate vectors
image1 = fullLocations[fullLocations['ImageNumber'] == 1]
image2 = fullLocations[fullLocations['ImageNumber'] == 2]
image3 = fullLocations[fullLocations['ImageNumber'] == 3]
image4 = fullLocations[fullLocations['ImageNumber'] == 4]
locations = image4
x = locations.loc[:, 'Location_Center_X']
y = locations.loc[:, 'Location_Center_Y']

# plot centroids with origin at top left3
plt.scatter(x, y, s=0.1, color='darkblue')
plt.gca().invert_yaxis()
plt.xlabel('X Locations')
plt.ylabel('Y Locations')
plt.title('Cell Centroids')
plt.show()

# get grid size from user input
rows = int(input("Enter number of grid rows: "))
columns = int(input("Enter numer of grid columns: "))

# create grid
# image size: 3653×3657 pixels
xnodes = np.linspace(0, 3653, num=columns + 1)
ynodes = np.linspace(0, 3657, num=rows + 1)

# plot grid on scatterplot
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

# sort data into bins based on x and y coordinates
locations['X_Bin'] = pd.cut(x=locations.loc[:, 'Location_Center_X'], bins=xnodes)
locations['Y_Bin'] = pd.cut(x=locations.loc[:, 'Location_Center_Y'], bins=ynodes)
boxes = locations.groupby(['X_Bin', 'Y_Bin']).count()
print(boxes['ImageNumber'])

# check accuracy of count total
total = boxes['ImageNumber'].sum()
if total != locations.shape[0]:
    print('Warning: grid sum does not match expected total!')

# average density
area = 3653*3657/columns/rows
av_density = boxes['ImageNumber'].mean()/(area)
print('Average density for', rows, 'rows and', columns, 'columns:', av_density)

# export to spreadsheet
file_name = 'GridSort.xlsx'
boxes.to_excel(file_name)
