from imageProcessingFunctions import *


# Specify spreadsheet and plots output folder
data_folder = "/Users/gillian/Desktop/UF/Thesis/Spreadsheets/"
plot_folder = "/Users/gillian/Desktop/UF/Thesis/Plots/"

# Import mouse ids and section numbers from spreadsheet
mouse_section_id = pd.read_csv('mouse_sections.csv', usecols=['Mouse_Sections'])

# Run analysis workflow for each image set (16 cross-sectional tumor image sets, three cell types per set)
for index, row in mouse_section_id.iterrows():
    image_set(data_folder, plot_folder, row['Mouse_Sections'])

print('Grid sort complete!')
