#Code adapted from the paper "Extended correlation functions for spatial analysis of
# multiplex imaging data" by Bull et al (2024),
# https://doi.org/10.1017/S2633903X24000011.

#GitHub: https://github.com/JABull1066/ExtendedCorrelationFunctions

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
from helperFunctions import *

sns.set_style('white')
sns.set(font_scale=5)

# create data frame of mouse ID strings
mouse_section_id = pd.read_csv('mouse_sections.csv', usecols=['Mouse_Sections'])

# choose image set for analysis
id_index = 0

#%% format data for cross-PCF

# import x and y locations of cancer cells from CellProfiler .csv file,
# convert from pixels to micrometers (0.62 um/px)
cancer_data = pd.read_csv(mouse_section_id.loc[id_index, 'Mouse_Sections']+'_Data_CancerCells.csv', usecols=['Location_Center_X', 'Location_Center_Y'])
cancer_data_um = cancer_data.mul(0.62)
cancer_array = cancer_data_um.to_numpy()

# import x and y locations of MDSCs from CellProfiler .csv file, convert from pixels to micrometers (0.62 um/px)
mdsc_data = pd.read_csv(mouse_section_id.loc[id_index, 'Mouse_Sections'] + '_Data_MDSC.csv', usecols=['Location_Center_X', 'Location_Center_Y'])
mdsc_data_um = mdsc_data.mul(0.62)
mdsc_array = mdsc_data_um.to_numpy()

# import x and y locations of T-cells from CellProfiler .csv file, convert from pixels to micrometers (0.62 um/px)
t_cell_data = pd.read_csv(mouse_section_id.loc[id_index, 'Mouse_Sections'] + '_Data_CD3.csv', usecols=['Location_Center_X', 'Location_Center_Y'])
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
labs_cancer_mdsc = np.concatenate((['Cancer Cells']*cancer_array.shape[0], ['MDSCs']*mdsc_array.shape[0]))
labs_cancer_t_cell = np.concatenate((['Cancer Cells']*cancer_array.shape[0], ['T-cells']*t_cell_array.shape[0]))
labs_mdsc_t_cell = np.concatenate((['MDSCs']*mdsc_array.shape[0], ['T-cells']*t_cell_array.shape[0]))
labs_cancer_cancer = np.concatenate((['Cancer Cells']*cancer_array.shape[0], ['Cancer Cells']*cancer_array.shape[0]))
labs_t_cell_t_cell = np.concatenate((['T-cells']*t_cell_array.shape[0], ['T-cells']*t_cell_array.shape[0]))
labs_mdsc_mdsc = np.concatenate((['MDSCs']*mdsc_array.shape[0], ['MDSCs']*mdsc_array.shape[0]))

# choose one comparison to run
labs = labs_cancer_mdsc

#%% plot cell types
pc = generatePointCloud(mouse_section_id, cancer_mdsc)
pc.addLabels('Celltype','categorical',labs,cmap='tab10')

visualisePointCloud(pc,'Celltype',markerSize=100)#,showBoundary=True)
c1mask = np.asarray(labs) == 'Cancer Cells'
plt.scatter(cancer_mdsc[c1mask,0],cancer_mdsc[c1mask,1],s=100,zorder=-1)
plt.gca().invert_yaxis()
plt.show()

#%% calculate cross-PCFs
a = 'Cancer Cells'
b = 'MDSCs'
maxR=1000
annulusStep = 1
annulusWidth = 10
r, pcf, contributions = pairCorrelationFunction(pc, 'Celltype', [a,b], maxR=maxR,annulusStep=annulusStep,annulusWidth=annulusWidth)
r2, pcf2, contributions2 = pairCorrelationFunction(pc, 'Celltype', [b,a], maxR=maxR,annulusStep=annulusStep,annulusWidth=annulusWidth)

plt.figure(figsize=(18,18))
plt.gca().axhline(1,c='k',linestyle=':',lw=3)
plt.plot(r,pcf,lw=7,label='$g_{Cancer MDSCs}(r)$',linestyle='-')
plt.plot(r2,pcf2,lw=7,label='$g_{MDSCs Cancer}(r)$',linestyle=(0,(1,1.5)))
plt.xlabel(r'Radius, $r$ ($\mu$m)')
plt.ylim([0,7])
plt.legend()
plt.show() # added this to see plots

print('r' + r + 'pcf' + pcf + 'contributions' + contributions)

#%% calculate TCMs
tcm = topographicalCorrelationMap(pc,'Celltype','Cancer Cells','Celltype','MDSCs',radiusOfInterest=50,maxCorrelationThreshold=5.0,kernelRadius=150,kernelSigma=50,visualiseStages=False)

plt.figure(figsize=(20,20))
l = int(np.ceil(np.max(np.abs([tcm.min(),tcm.max()]))))
plt.imshow(tcm,cmap='RdBu_r',vmin=-l,vmax=l,origin='lower')
plt.colorbar(label=r'$\Gamma_{Cancer MDSCs}(r=50)$')
ax = plt.gca()
ax.grid(False)
plt.gca().invert_yaxis()
plt.show() # added this to see plots

tcm = topographicalCorrelationMap(pc,'Celltype','MDSCs','Celltype','Cancer Cells',radiusOfInterest=50,maxCorrelationThreshold=5.0,kernelRadius=150,kernelSigma=50,visualiseStages=False)

plt.figure(figsize=(20,20))
l = int(np.ceil(np.max(np.abs([tcm.min(),tcm.max()]))))
plt.imshow(tcm,cmap='RdBu_r',vmin=-l,vmax=l,origin='lower')
plt.colorbar(label=r'$\Gamma_{MDCSs Cancer}(r=50)$')
ax = plt.gca()
ax.grid(False)
plt.gca().invert_yaxis()
plt.show() # added this to see plots
