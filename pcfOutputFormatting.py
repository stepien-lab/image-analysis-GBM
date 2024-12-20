import pandas as pd
import os
import glob

path = os.getcwd()
csv_files = glob.glob(os.path.join('/Users/gillian/Desktop/UF/Thesis/Spreadsheets/PCF', "*.csv"))

df_list = []
for file in csv_files:
    if not('2332_3' in file):
        df = pd.read_csv(file)
        df_list.append(df)

pcf_results = pd.concat(df_list, axis=1)

# filter out cancer to mdsc data
CM = pcf_results.filter(like='Cancer CellsMDSCs')
CSM = pcf_results.filter(like='Cancer Cells SubsetMDSCs')
CM = pd.concat([CM, CSM], axis=1)
print(CM.columns)
print(CM.shape)

# filter out mdsc to cancer data
MC = pcf_results.filter(like='MDSCsCancer Cells')
print(MC.columns)
print(MC.shape)

# filter out cancer to t cell data
CT = pcf_results.filter(like='Cancer CellsT-cells')
CST = pcf_results.filter(like='Cancer Cells SubsetT-cells')
CT = pd.concat([CT, CST], axis=1)
print(CT.columns)
print(CT.shape)

# filter out t cell to cancer data
TC = pcf_results.filter(like='T-cellsCancer Cells')
print(TC.columns)
print(TC.shape)

# filter out mdsc to t cell data
MT = pcf_results.filter(like='MDSCsT-cells')
print(MT.columns)
print(MT.shape)

# filter out t cell to mdsc data
TM = pcf_results.filter(like='T-cellsMDSCs')
print(TM.columns)
print(TM.shape)

# filter out cancer to cancer data
C = pcf_results.filter(like='Cancer CellsCancer Cells')
CS = pcf_results.filter(like='Cancer Cells SubsetCancer Cells')
C = pd.concat([C, CS], axis=1)
print(C.columns)
print(C.shape)

# filter out mdsc to mdsc data
M = pcf_results.filter(like='MDSCsMDSCs')
print(M.columns)
print(M.shape)

# filter out t-cell to t-cell data
T = pcf_results.filter(like='T-cellsT-cells')
TS = pcf_results.filter(like='T-cells SubsetT-cells')
T = pd.concat([T, TS], axis=1)
print(T.columns)
print(T.shape)

CM = CM.transpose()
MC = MC.transpose()
CT = CT.transpose()
TC = TC.transpose()
MT = MT.transpose()
TM = TM.transpose()
C = C.transpose()
M = M.transpose()
T = T.transpose()

for column in CM:
    CM.rename(columns={column: 'r' + str(column)}, inplace=True)
for column in MC:
    MC.rename(columns={column: 'r' + str(column)}, inplace=True)
for column in CT:
    CT.rename(columns={column: 'r' + str(column)}, inplace=True)
for column in TC:
    TC.rename(columns={column: 'r' + str(column)}, inplace=True)
for column in MT:
    MT.rename(columns={column: 'r' + str(column)}, inplace=True)
for column in TM:
    TM.rename(columns={column: 'r' + str(column)}, inplace=True)
for column in C:
    C.rename(columns={column: 'r' + str(column)}, inplace=True)
for column in M:
    M.rename(columns={column: 'r' + str(column)}, inplace=True)
for column in T:
    T.rename(columns={column: 'r' + str(column)}, inplace=True)

CM.reset_index(inplace=True, drop=True)
MC.reset_index(inplace=True, drop=True)
CT.reset_index(inplace=True, drop=True)
TC.reset_index(inplace=True, drop=True)
MT.reset_index(inplace=True, drop=True)
TM.reset_index(inplace=True, drop=True)
C.reset_index(inplace=True, drop=True)
M.reset_index(inplace=True, drop=True)
T.reset_index(inplace=True, drop=True)

CM = CM.transpose()
MC = MC.transpose()
CT = CT.transpose()
TC = TC.transpose()
MT = MT.transpose()
TM = TM.transpose()
C = C.transpose()
M = M.transpose()
T = T.transpose()

for column in CM:
    CM.rename(columns={column: 'c' + str(column + 1)}, inplace=True)
for column in MC:
    MC.rename(columns={column: 'c' + str(column + 1)}, inplace=True)
for column in CT:
    CT.rename(columns={column: 'c' + str(column + 1)}, inplace=True)
for column in TC:
    TC.rename(columns={column: 'c' + str(column + 1)}, inplace=True)
for column in MT:
    MT.rename(columns={column: 'c' + str(column + 1)}, inplace=True)
for column in TM:
    TM.rename(columns={column: 'c' + str(column + 1)}, inplace=True)
for column in C:
    C.rename(columns={column: 'c' + str(column + 1)}, inplace=True)
for column in M:
    M.rename(columns={column: 'c' + str(column + 1)}, inplace=True)
for column in T:
    T.rename(columns={column: 'c' + str(column + 1)}, inplace=True)

CM.to_csv('CM.csv')
MC.to_csv('MC.csv')
CT.to_csv('CT.csv')
TC.to_csv('TC.csv')
MT.to_csv('MT.csv')
TM.to_csv('TM.csv')
C.to_csv('C.csv')
M.to_csv('M.csv')
T.to_csv('T.csv')
