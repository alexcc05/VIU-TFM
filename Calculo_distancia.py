#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Código para convertir las unidades de flujo de cada región HII y para calcular la distancia a las galaxias

import pandas as pd
import os
from astropy.io import fits


path =r"C:/Users/Alexander/Desktop/VIU-TFM/DATA/"

data = pd.DataFrame(columns=['Name', 'chalpha', 'fwhm'])

#Recorrer cada fichero fits para obtener chalpha de la cabecera
for filename in os.listdir(path+'/final_fits/HALPHA'):
    if 'Ha_final' in filename:
        f = os.path.join(path+'/final_fits/HALPHA',filename)
        if os.path.isfile(f):
            file = fits.open(f)[0]  

            data = data.append({'Name':filename[:-14], 'chalpha':file.header['CHALPHA'], 'fwhm': file.header['L1SEESEC']},ignore_index=True)

#Obtener el redshift

redshift = pd.read_excel(path+'observing_progress.xls')

data['z']= data.merge(redshift, on=['Name'], how='left')['z']

data['distance']= data['z']*299792.458/69.6

# data.to_csv(path+'galaxies_data_SINFWHM.csv')
data.to_excel(path+'galaxies_data.xlsx')

