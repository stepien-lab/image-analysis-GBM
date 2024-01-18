from workflow import *


def image_set(data_folder, plot_folder, mouse_section_id):
    # import x and y locations of cancer cells from CellProfiler csv file
    cancer_data = pd.read_csv(mouse_section_id+'_Data_CancerCells.csv', usecols=['Location_Center_X',
                                                                                 'Location_Center_Y'])

    # import x and y locations of MDSCs from CellProfiler csv file
    mdsc_data = pd.read_csv(mouse_section_id+'_Data_MDSC.csv', usecols=['Location_Center_X', 'Location_Center_Y'])

    # import x and y locations of CD3 from CellProfiler csv file
    cd3_data = pd.read_csv(mouse_section_id+'_Data_CD3.csv', usecols=['Location_Center_X', 'Location_Center_Y'])

    # import image sizes
    image_sizes = pd.read_csv(mouse_section_id+'_Data_Image.csv', usecols=['Height_DAPI', 'Width_DAPI'])
    # image scale: .62 um/px
    height = image_sizes.loc[0, 'Height_DAPI']*0.62
    width = image_sizes.loc[0, 'Width_DAPI']*0.62

    # multiple grid sizes
    grid_box_size_px = [400, 200, 100, 50]

    for size in grid_box_size_px:
        # create grid for to use for all images
        grid = make_grid(width, height, size)
        # create spreadsheet for density data
        density_data = pd.DataFrame(columns=['Cell Type', 'Grid Box Size (px)', 'Density'])
        # analyze images
        analyze(cancer_data, grid, size, density_data, 'Cancer Cell', width, height, data_folder,
                plot_folder)
        analyze(mdsc_data, grid, size, density_data, 'MDSC', width, height, data_folder, plot_folder)
        analyze(cd3_data, grid, size, density_data, 'CD3', width, height, data_folder, plot_folder)
        # save density data as spreadsheet
        density_data.to_excel(data_folder + 'AverageDensity' + '_' + str(size) + 'px.xlsx')
