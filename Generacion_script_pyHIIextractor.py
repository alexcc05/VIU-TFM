#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Código para generar los scripts de ejecución de pyHIIextractor de cada galaxia 

import pandas as pd

path = '..'

data = pd.read_excel(path+'galaxies_data.xlsx',index_col=0)

for j in data[data['sigma']!= '-'].iterrows():
    
    row = j[1]
    galaxy = row['Name']
    
    pathOutput = 'C:/Users/Alexander/Desktop/VIU-TFM/EXECUTIONS/'+galaxy+'/'


    sigma = row['sigma']
    fwhm = row['fwhm']
    output=''


    for alpha in [ 0.1,0.3,0.5, 0.7, 1, 1.1, 1.3, 1.5, 1.7, 2, 2.1, 2.3, 2.5, 2.7, 3]:
        for size in [fwhm, 1.5, 1.8, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5]:

            name = galaxy+'_'+str(alpha)+'_'+str(size)
            sigmaalpha = sigma*alpha
            output+='%run pyHIIdet_img.py '+ name +' ../'+galaxy+'_Ha_final.fits_recortada.fits 0 '+str(fwhm)+' 0.3037 '+ str(sigmaalpha)+' '+str(sigma)+' 1 0 0 0 '+str(size)+' '+pathOutput+'\n'

    print(output)

    with open(pathOutput+"/exec_commands.txt", "w") as text_file:
       text_file.write(output)

