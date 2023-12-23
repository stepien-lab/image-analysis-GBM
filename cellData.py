from workflow import *

# specify spreadsheet output folder
data_folder = "/Users/gillian/Desktop/UF/Thesis/Spreadsheets/"

# import x and y locations of each primary object from CellProfiler csv file
fullLocations = pd.read_csv('Counts_Cells.csv', usecols=['ImageNumber', 'ObjectNumber',
                                                         'Location_Center_X', 'Location_Center_Y'])

# import image sizes
imageSizes = pd.read_csv('Counts_Image.csv', usecols=['Height_ColorCells', 'Width_ColorCells'])
height = imageSizes.loc[0, 'Height_ColorCells']
width = imageSizes.loc[0, 'Width_ColorCells']

# limit data frame to one image and create coordinate vectors
image1 = fullLocations[fullLocations['ImageNumber'] == 1]
image2 = fullLocations[fullLocations['ImageNumber'] == 2]
image3 = fullLocations[fullLocations['ImageNumber'] == 3]
image4 = fullLocations[fullLocations['ImageNumber'] == 4]

# create grid for to use for all images
grid = make_grid(width, height)

# create spreadsheet for density data
density_data = pd.DataFrame(columns=['Number', 'Rows', 'Columns', 'Density'])

# analyze images
analyze(image1, grid, density_data, 1, width, height, data_folder)
analyze(image2, grid, density_data, 2, width, height, data_folder)
analyze(image3, grid, density_data, 3, width, height, data_folder)
analyze(image4, grid, density_data, 4, width, height, data_folder)

# save density data as spreadsheet
density_data.to_excel(data_folder + 'AverageDensity' + str(grid[2]) + 'x' + str(grid[3]) + '.xlsx')