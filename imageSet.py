from workflow import *


def image_set(data_folder, mouse_section_id):
    # import x and y locations of cancer cells from CellProfiler csv file
    cancer_data = pd.read_csv(mouse_section_id+'_Data_CancerCells.csv', usecols=['Location_Center_X',
                                                                                 'Location_Center_Y'])

    # import x and y locations of MDSCs from CellProfiler csv file
    mdsc_data = pd.read_csv(mouse_section_id+'_Data_MDSC.csv', usecols=['Location_Center_X', 'Location_Center_Y'])

    # import x and y locations of CD3 from CellProfiler csv file
    cd3_data = pd.read_csv(mouse_section_id+'_Data_CD3.csv', usecols=['Location_Center_X', 'Location_Center_Y'])

    # import image sizes
    image_sizes = pd.read_csv(mouse_section_id+'_Data_Image.csv', usecols=['Height_DAPI', 'Width_DAPI'])
    height = image_sizes.loc[0, 'Height_DAPI']
    width = image_sizes.loc[0, 'Width_DAPI']

    # create grid for to use for all images
    grid = make_grid(width, height)

    # create spreadsheet for density data
    density_data = pd.DataFrame(columns=['Cell Type', 'Rows', 'Columns', 'Density'])

    # analyze images
    analyze(cancer_data, grid, density_data, 'Cancer Cell', width, height, data_folder)
    analyze(mdsc_data, grid, density_data, 'MDSC', width, height, data_folder)
    analyze(cd3_data, grid, density_data, 'CD3', width, height, data_folder)

    # save density data as spreadsheet
    density_data.to_excel(data_folder + 'AverageDensity' + str(grid[2]) + 'x' + str(grid[3]) + '.xlsx')
