from gridPlot import *
from gridCount import *


# use functions to follow data analysis process for all colors in a set
def analyze(image, grid, grid_box_size, density_data, cell_type, width, height, data_folder, plot_folder):
    # plotting and data analysis
    plot_points(image, cell_type, plot_folder)
    grid_plot(image, grid[0], grid[1], width, height, cell_type, grid_box_size, plot_folder)
    image_data = grid_sort(image, grid[0], grid[1])
    av_density = density(grid_box_size, image_data)

    # export to spreadsheet
    file_name = 'GridSort' + '_' + cell_type + '_' + str(grid_box_size) + 'px.xlsx'
    image_data.to_excel(data_folder + file_name)

    # add density data to dataframe
    density_data.loc[len(density_data)] = [cell_type, grid_box_size, av_density]
