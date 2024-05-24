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

# import x and y locations of cancer cells from CellProfiler .csv file, convert from pixels to micrometers (0.62 um/px)
cancer_data = pd.read_csv(mouse_section_id.loc[0, 'Mouse_Sections']+'_Data_CancerCells.csv', usecols=['Location_Center_X', 'Location_Center_Y'])
cancer_data_um = cancer_data.mul(0.62)
cancer_array = cancer_data_um.to_numpy()

# import x and y locations of MDSCs from CellProfiler .csv file, convert from pixels to micrometers (0.62 um/px)
mdsc_data = pd.read_csv(mouse_section_id.loc[0, 'Mouse_Sections'] + '_Data_MDSC.csv', usecols=['Location_Center_X', 'Location_Center_Y'])
mdsc_data_um = mdsc_data.mul(0.62)
mdsc_array = mdsc_data_um.to_numpy()

# import x and y locations of T-cells from CellProfiler .csv file, convert from pixels to micrometers (0.62 um/px)
cd3_data = pd.read_csv(mouse_section_id.loc[0, 'Mouse_Sections'] + '_Data_CD3.csv', usecols=['Location_Center_X', 'Location_Center_Y'])
cd3_data_um = cd3_data.mul(0.62)
cd3_array = cd3_data_um.to_numpy()

# combine cell types into one array for later use in cross-PCFs
cancer_mdsc = arr = np.vstack((cancer_array, mdsc_array))

# create array of cell labels for later use in cross-PCFs
labs = np.concatenate((['Cancer Cells']*cancer_array.shape[0], ['MDSCs']*mdsc_array.shape[0]))

pc = generatePointCloud(mouse_section_id, cancer_mdsc)
pc.addLabels('Celltype','categorical',labs,cmap='tab10')
#pc.addLabels('$m$','continuous',contuslabs,cmap='RdBu_r')

visualisePointCloud(pc,'Celltype',markerSize=100)#,showBoundary=True)
#visualisePointCloud(pc,'$m$',markerSize=100,cmap='Oranges')#,showBoundary=True)
c1mask = np.asarray(labs) == 'Cancer Cells'
plt.scatter(cancer_mdsc[c1mask,0],cancer_mdsc[c1mask,1],s=100,zorder=-1)
plt.gca().invert_yaxis()
plt.show()

#%% Calculate cross-PCFs
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
plt.show() # I added this to see plots

#%% Calculate TCMs
tcm = topographicalCorrelationMap(pc,'Celltype','Cancer Cells','Celltype','MDSCs',radiusOfInterest=50,maxCorrelationThreshold=5.0,kernelRadius=150,kernelSigma=50,visualiseStages=False)

plt.figure(figsize=(20,20))
l = int(np.ceil(np.max(np.abs([tcm.min(),tcm.max()]))))
plt.imshow(tcm,cmap='RdBu_r',vmin=-l,vmax=l,origin='lower')
plt.colorbar(label=r'$\Gamma_{Cancer MDSCs}(r=50)$')
ax = plt.gca()
ax.grid(False)
plt.gca().invert_yaxis()
plt.show() # I added this to see plots

tcm = topographicalCorrelationMap(pc,'Celltype','MDSCs','Celltype','Cancer Cells',radiusOfInterest=50,maxCorrelationThreshold=5.0,kernelRadius=150,kernelSigma=50,visualiseStages=False)

plt.figure(figsize=(20,20))
l = int(np.ceil(np.max(np.abs([tcm.min(),tcm.max()]))))
plt.imshow(tcm,cmap='RdBu_r',vmin=-l,vmax=l,origin='lower')
plt.colorbar(label=r'$\Gamma_{MDCSs Cancer}(r=50)$')
ax = plt.gca()
ax.grid(False)
plt.gca().invert_yaxis()
plt.show() # I added this to see plots
