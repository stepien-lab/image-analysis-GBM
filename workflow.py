from gridPlot import *
from gridCount import *


# use functions to follow data analysis process for all colors in a set
def analyze(image, grid, density_data, cell_type, width, height, data_folder):
    # plotting and data analysis
    plot_points(image, cell_type)
    grid_plot(image, grid[0], grid[1], width, height, cell_type)
    image_data = grid_sort(image, grid[0], grid[1])
    av_density = density(width, height, grid[2], grid[3], image_data)

    # export to spreadsheet
    file_name = 'GridSort' + '_' + cell_type + '_' + str(grid[2]) + 'x' + str(grid[3]) + '.xlsx'
    image_data.to_excel(data_folder + file_name)

    # add density data to dataframe
    density_data.loc[len(density_data)] = [cell_type, grid[2], grid[3], av_density]
