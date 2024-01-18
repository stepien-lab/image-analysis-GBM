from imageSet import *

# specify spreadsheet output folder
data_folder = "/Users/gillian/Desktop/UF/Thesis/Spreadsheets/"
plot_folder = "/Users/gillian/Desktop/UF/Thesis/Plots"

# import mouse ids and section numbers
mouse_section_id = pd.read_csv('mouse_sections.csv', usecols=['Mouse_Sections'])

# run analysis for each image set
for index, row in mouse_section_id.iterrows():
    image_set(data_folder, plot_folder, row['Mouse_Sections'])
