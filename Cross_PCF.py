# Code adapted from the paper "Extended correlation functions for spatial analysis of
# multiplex imaging data" by Bull et al. (2024),
# https://doi.org/10.1017/S2633903X24000011.

# GitHub: https://github.com/JABull1066/ExtendedCorrelationFunctions

import time

from helperFunctions import *

start = time.time()

sns.set_theme(style='ticks', font_scale=5)

# create data frame of mouse ID strings
mouse_section_id = pd.read_csv('mouse_sections.csv')

# choose image set for analysis
id_index = 0

# format labels for plots
section_name = mouse_section_id.loc[id_index, 'Mouse_Sections']
section_name = section_name.replace('_', '-', 1)
section_name = section_name.replace('_', ' ')
section_name = 'Mouse ' + section_name[:14] + ' ' + section_name[14:]
days = str(mouse_section_id.loc[id_index, 'Days'])

# %% format data for cross-PCF

# import x and y locations of cancer cells from CellProfiler .csv file,
# convert from pixels to micrometers (0.62 um/px)
cancer_data = pd.read_csv(mouse_section_id.loc[id_index, 'Mouse_Sections'] + '_Data_CancerCells.csv',
                          usecols=['Location_Center_X', 'Location_Center_Y'])
cancer_data_um = cancer_data.mul(0.62)
cancer_array = cancer_data_um.to_numpy()

# import x and y locations of MDSCs from CellProfiler .csv file, convert from pixels to micrometers (0.62 um/px)
mdsc_data = pd.read_csv(mouse_section_id.loc[id_index, 'Mouse_Sections'] + '_Data_MDSC.csv',
                        usecols=['Location_Center_X', 'Location_Center_Y'])
mdsc_data_um = mdsc_data.mul(0.62)
mdsc_array = mdsc_data_um.to_numpy()

# import x and y locations of T-cells from CellProfiler .csv file, convert from pixels to micrometers (0.62 um/px)
t_cell_data = pd.read_csv(mouse_section_id.loc[id_index, 'Mouse_Sections'] + '_Data_CD3.csv',
                          usecols=['Location_Center_X', 'Location_Center_Y'])
t_cell_data_um = t_cell_data.mul(0.62)
t_cell_array = t_cell_data_um.to_numpy()

# combine cell types into one array for later use in cross-PCFs
cancer_mdsc = arr1 = np.vstack((cancer_array, mdsc_array))
cancer_t_cell = arr2 = np.vstack((cancer_array, t_cell_array))
mdsc_t_cell = arr3 = np.vstack((mdsc_array, t_cell_array))
cancer_cancer = arr4 = np.vstack((cancer_array, cancer_array))
t_cell_t_cell = arr5 = np.vstack((t_cell_array, t_cell_array))
mdsc_mdsc = arr6 = np.vstack((mdsc_array, mdsc_array))

# create array of cell labels for later use in cross-PCFs
labs_cancer_mdsc = np.concatenate((['Cancer Cells'] * cancer_array.shape[0], ['MDSCs'] * mdsc_array.shape[0]))
labs_cancer_t_cell = np.concatenate((['Cancer Cells'] * cancer_array.shape[0], ['T-cells'] * t_cell_array.shape[0]))
labs_mdsc_t_cell = np.concatenate((['MDSCs'] * mdsc_array.shape[0], ['T-cells'] * t_cell_array.shape[0]))
labs_cancer_cancer = np.concatenate(
    (['Cancer Cells'] * cancer_array.shape[0], ['Cancer Cells'] * cancer_array.shape[0]))
labs_t_cell_t_cell = np.concatenate((['T-cells'] * t_cell_array.shape[0], ['T-cells'] * t_cell_array.shape[0]))
labs_mdsc_mdsc = np.concatenate((['MDSCs'] * mdsc_array.shape[0], ['MDSCs'] * mdsc_array.shape[0]))

# choose one comparison to run
array = cancer_mdsc
labs = labs_cancer_mdsc
gamma1 = r'$g_{CM}$'
gamma2 = r'$g_{MC}$'


# %% plot cell types
pc = generatePointCloud("Points", array)
pc.addLabels('Cell type', 'categorical', labs, cmap='tab10')

visualisePointCloud(pc, 'Cell type', markerSize=10)
c1mask = np.asarray(labs) == labs[0]
plt.scatter(array[c1mask, 0], array[c1mask, 1], s=10, zorder=-1)
plt.gca().invert_yaxis()
plt.title(section_name + ' (' + days + ' days)')
plt.xlabel(r'$\mu$m')
plt.ylabel(r'$\mu$m')
plt.savefig('/Users/gillian/Desktop/UF/Thesis/Plots/PCF/Scatter_Plot_'
            + mouse_section_id.loc[id_index, 'Mouse_Sections'] + '_' + labs[0] + '_' + labs[labs.shape[0] - 1]
            + '.png', bbox_inches='tight')
plt.show()

# %% calculate cross-PCFs
a = labs[0]
b = labs[labs.shape[0] - 1]
maxR = 1000
annulusStep = 1
annulusWidth = 10
r, pcf, contributions = pairCorrelationFunction(pc, 'Cell type', [a, b], maxR=maxR, annulusStep=annulusStep,
                                                annulusWidth=annulusWidth)
r2, pcf2, contributions2 = pairCorrelationFunction(pc, 'Cell type', [b, a], maxR=maxR, annulusStep=annulusStep,
                                                   annulusWidth=annulusWidth)

plt.figure(figsize=(20, 20))
plt.gca().axhline(1, c='k', linestyle=':', lw=3)
plt.plot(r, pcf, lw=7, label=gamma1 + r'(r)', linestyle='-')
plt.plot(r2, pcf2, lw=7, label=gamma2 + r'(r)', linestyle=(0, (1, 1.5)))
plt.title(section_name + a + '/' + b + 'PCF Plot')
plt.xlabel(r'radius $r$ ($\mu$m)')
plt.legend()
plt.savefig('/Users/gillian/Desktop/UF/Thesis/Plots/PCF/Cross_PCF_Plot_' +
            mouse_section_id.loc[id_index, 'Mouse_Sections'] + '_' + labs[0] + '_' + labs[labs.shape[0] - 1]
            + '.png', bbox_inches='tight')
plt.show()

# save cross pcf data
cross_pcf_data = pd.DataFrame(columns=['r', str(a) + str(b), 'r2', str(b) + str(a)])
cross_pcf_data['r'] = r
cross_pcf_data[str(a) + str(b)] = pcf
cross_pcf_data['r2'] = r2
cross_pcf_data[str(b) + str(a)] = pcf2
cross_pcf_data.to_csv('/Users/gillian/Desktop/UF/Thesis/Spreadsheets/PCF/Cross_PCF_'
                      + mouse_section_id.loc[id_index, 'Mouse_Sections'] + '_' + labs[0] + '_' + labs[labs.shape[0] - 1]
                      + '.csv')

# %% calculate TCMs
tcm = topographicalCorrelationMap(pc, 'Cell type', a, 'Cell type', b, radiusOfInterest=50,
                                  maxCorrelationThreshold=5.0, kernelRadius=150, kernelSigma=50, visualiseStages=False)

plt.figure(figsize=(20, 20))
limit = int(np.ceil(np.max(np.abs([tcm.min(), tcm.max()]))))
plt.imshow(tcm, cmap='RdBu_r', vmin=-limit, vmax=limit, origin='lower')
plt.colorbar(label=gamma1 + r'(r=50)')
plt.title(section_name + ' Topographical Correlation Map A')
plt.xlabel(r'$\mu$m')
plt.ylabel(r'$\mu$m')
plt.gca().invert_yaxis()
plt.savefig('/Users/gillian/Desktop/UF/Thesis/Plots/PCF/TCM1_Plot_' + mouse_section_id.loc[id_index, 'Mouse_Sections']
            + '_' + labs[0] + '_' + labs[labs.shape[0] - 1] + '.png', bbox_inches='tight')
plt.show()

tcm = topographicalCorrelationMap(pc, 'Cell type', b, 'Cell type', a, radiusOfInterest=50,
                                  maxCorrelationThreshold=5.0, kernelRadius=150, kernelSigma=50, visualiseStages=False)

plt.figure(figsize=(20, 20))
limit = int(np.ceil(np.max(np.abs([tcm.min(), tcm.max()]))))
plt.imshow(tcm, cmap='RdBu_r', vmin=-limit, vmax=limit, origin='lower')
plt.colorbar(label=gamma2 + r'(r=50)')
plt.title(section_name + ' Topographical Correlation Map B')
plt.xlabel(r'$\mu$m')
plt.ylabel(r'$\mu$m')
plt.gca().invert_yaxis()
plt.savefig('/Users/gillian/Desktop/UF/Thesis/Plots/PCF/TCM2_Plot_' + mouse_section_id.loc[id_index, 'Mouse_Sections']
            + '_' + labs[0] + '_' + labs[labs.shape[0] - 1] + '.png', bbox_inches='tight')
plt.show()

end = time.time()

print('Execution time: ' + str((end - start)/60) + ' min')
