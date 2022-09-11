#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Código para obtener el desglose de los tipos de regiones HII detectadas

import xlsxwriter
import os
import re
import pandas as pd
import numpy as np

path =r''

os.chdir(path)

result_excel = pd.DataFrame (columns={'Galaxia','Clasica','Gigante','Supergigante'})

for root, subdirectories, files in os.walk(path+'\FINAL_EXEC'):
    for file in files:
        if '_datosluminosidad' in file:
            data = pd.read_excel(path+"\FINAL_EXEC/"+file[:-22]+'/'+file)
            print(data.iloc[0].luminosity > pow(10,40))
            print(data[data.luminosity < pow(10,37)].shape[0])         
            cl = data[data.luminosity < pow(10,37)].shape[0]
            g = data[data.luminosity >= pow(10,37)][data.luminosity <= pow(10,39)].shape[0]
            sg = data[data.luminosity > pow(10,39)].shape[0]
            result_excel = result_excel.append({'Galaxia':file[:-22], 'Clasica':cl, 'Gigante':g, 'Supergigante':sg}, ignore_index=True)
            print(result_excel)
            
result_excel.to_excel(path+'/tiposhii.xlsx')

