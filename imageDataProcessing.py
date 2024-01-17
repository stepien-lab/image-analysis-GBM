from imageSet import *

# specify spreadsheet output folder
data_folder = "/Users/gillian/Desktop/UF/Thesis/Spreadsheets/"

mouse_section_id = pd.read_csv('mouse_sections.csv', usecols=['Mouse_Sections'])

for index, row in mouse_section_id.iterrows():
    image_set(data_folder, row['Mouse_Sections'])
