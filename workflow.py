from gridPlot import *
from gridCount import *


# use functions to follow data analysis process for all colors in a set
def analyze(image, grid, number):
    # plotting and data analysis
    plot_points(image)
    grid_plot(image, grid[0], grid[1])
    image_data = grid_sort(image, grid[0], grid[1])
    density(grid[2], grid[3], image_data)

    # export to spreadsheet
    file_name = 'GridSort' + str(number) + ':' + str(grid[2]) + 'x'+ str(grid[3]) + '.xlsx'
    image_data.to_excel(file_name)