from gridPlot import *
from gridCount import *


# use functions to follow data analysis process for all colors in a set
def analyze(image, grid, density_data, number, width, height, data_folder):
    # plotting and data analysis
    plot_points(image)
    grid_plot(image, grid[0], grid[1])
    image_data = grid_sort(image, grid[0], grid[1])
    av_density = density(grid[2], grid[3], image_data, width, height)

    # export to spreadsheet
    file_name = 'GridSort' + str(number) + '_' + str(grid[2]) + 'x' + str(grid[3]) + '.xlsx'
    image_data.to_excel(data_folder + file_name)

    # add density data to dataframe
    density_data.loc[len(density_data)] = [number, grid[2], grid[3], av_density]
