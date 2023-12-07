from workflow import *

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

# analyze images
analyze(image1, grid, 1, width, height)
analyze(image2, grid, 2, width, height)
analyze(image3, grid, 3, width, height)
analyze(image4, grid, 4, width, height)
