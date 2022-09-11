#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Código para obtener las luminosidades de las regiones HII

import xlsxwriter
import os
import re
import pandas as pd
import numpy as np

path =r".."

data = pd.read_excel(path+'\galaxies_data.xlsx',index_col=0)

os.chdir(path)
    
for root, subdirectories, files in os.walk(path+'\FINAL_EXEC'):
    for file in files:
        if 'HIIblob_HII.tab' in file and '1087' in file:
            result_excel = pd.DataFrame (columns={'IDRegion','X','Y','R','flux','luminosity'})

            file_path =os.path.join(root, file)
            m = re.match("([a-zA-Z0-9]*)(\w)(\d\.*\d*)_((\d)\.*(\d)*)\.(\w+)\.(\w){3}\.(\w){4}", f"{file}")
            
            distance = data[data['Name'] == m.group(1)].iloc[0].distance*100000000*30856775812799588
            chalpha = data[data['Name'] == m.group(1)].iloc[0].chalpha

            with open(file_path, 'r') as file:
               counter = 0
               for line in file:
                    counter+=1
                    if line != "\n" and counter > 11:
                        s=line.split(',')
                        print(line.split(','))
                        result_excel = result_excel.append({'IDRegion':s[0], 'X':s[1], 'Y':s[2], 'R':s[3], 'flux':s[4], 'luminosity':4*np.pi*distance*distance*float(s[4])*chalpha}, ignore_index=True)
    
            
            result_excel.to_excel(path+'/FINAL_EXEC/'+m.group(1)+'/'+m.group(1)+'_datosluminosidad.xlsx')

