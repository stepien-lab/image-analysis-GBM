import random
from imageProcessingFunctions import *


# create data frame of mouse ID strings
mouse_section_id = pd.read_csv('mouse_sections.csv')
section_list = mouse_section_id['Mouse_Sections'].copy()

for section in section_list:
    # import x and y locations of cells from CellProfiler .csv file,
    # convert from pixels to micrometers (0.62 um/px)
    t_cell_data = pd.read_csv(section + '_Data_CD3.csv',
                              usecols=['Location_Center_X', 'Location_Center_Y'])
    t_cell_data_um = t_cell_data.mul(0.62)

    # import image size and convert to um
    image_sizes = pd.read_csv(section+'_Data_Image.csv', usecols=['Height_DAPI', 'Width_DAPI'])
    # image scale: .62 um/px
    height = image_sizes.loc[0, 'Height_DAPI']*0.62
    width = image_sizes.loc[0, 'Width_DAPI']*0.62

    # sort data into bins based on x and y coordinates
    grid = make_grid(width, height, 50)
    t_cell_data_um['X_Bin'] = pd.cut(x=t_cell_data_um.loc[:, 'Location_Center_X'], bins=grid[0])
    t_cell_data_um['Y_Bin'] = pd.cut(x=t_cell_data_um.loc[:, 'Location_Center_Y'], bins=grid[1])

    # select a random 10% of cells in each bin
    t_cell_subset = pd.DataFrame(columns=['Location_Center_X', 'Location_Center_Y', 'X_Bin', 'Y_Bin'])
    for name, group in t_cell_data_um.groupby(['X_Bin', 'Y_Bin'], observed=False):
        no_of_selected_cells = round(group.shape[0]/10)
        i = 0
        index_bank = []
        group.reset_index(inplace=True, drop=True)
        while i < no_of_selected_cells:
            cell_index = round(random.uniform(0, group.shape[0]))
            if cell_index == group.shape[0]:
                cell_index = 0
            if any(cell_index == element for element in index_bank):
                continue
            index_bank.append(cell_index)
            t_cell_subset.loc[len(t_cell_subset)] = group.iloc[cell_index]
            i += 1

    # save as spreadsheet
    t_cell_subset_data = t_cell_subset[['Location_Center_X', 'Location_Center_Y']].copy()
    t_cell_subset_data.to_csv(section + '_Data_TCellsSubset.csv')

    print(section + ' done!')
