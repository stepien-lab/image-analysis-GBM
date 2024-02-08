from workflow import *


def image_set(data_folder, plot_folder, mouse_section_id):
    # import x and y locations of cancer cells from CellProfiler csv file
    cancer_data = pd.read_csv(mouse_section_id+'_Data_CancerCells.csv', usecols=['Location_Center_X',
                                                                                 'Location_Center_Y'])
    cancer_data_px = cancer_data.mul(0.62)

    # import x and y locations of MDSCs from CellProfiler csv file
    mdsc_data = pd.read_csv(mouse_section_id+'_Data_MDSC.csv', usecols=['Location_Center_X', 'Location_Center_Y'])
    mdsc_data_px = mdsc_data.mul(0.62)

    # import x and y locations of CD3 from CellProfiler csv file
    cd3_data = pd.read_csv(mouse_section_id+'_Data_CD3.csv', usecols=['Location_Center_X', 'Location_Center_Y'])
    cd3_data_px = cd3_data.mul(0.62)

    # import image sizes
    image_sizes = pd.read_csv(mouse_section_id+'_Data_Image.csv', usecols=['Height_DAPI', 'Width_DAPI'])
    # image scale: .62 um/px
    height = image_sizes.loc[0, 'Height_DAPI']*0.62
    width = image_sizes.loc[0, 'Width_DAPI']*0.62

    # multiple grid sizes
    grid_box_size_px = [1000, 500, 250]

    for size in grid_box_size_px:
        # create grid for to use for all images
        grid = make_grid(width, height, size)
        # create spreadsheet for density data
        density_data = pd.DataFrame(columns=['Cell Type', 'Grid Box Size (px)', 'Density'])
        # analyze images
        analyze(cancer_data_px, grid, size, density_data, 'CancerCell', width, height, data_folder,
                plot_folder, mouse_section_id)
        analyze(mdsc_data_px, grid, size, density_data, 'MDSC', width, height, data_folder, plot_folder, mouse_section_id)
        analyze(cd3_data_px, grid, size, density_data, 'CD3', width, height, data_folder, plot_folder, mouse_section_id)
        # save density data as spreadsheet
        density_data.to_excel(data_folder + 'AverageDensity' + '_' + mouse_section_id + '_' + str(size) + 'px.xlsx')
        print(mouse_section_id + ' ' + str(size) + ' px sort complete!')
