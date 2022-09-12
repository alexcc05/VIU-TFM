#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Código para hallar el número de regiones y X^2 de cada ejecución, y generar los histogramas de las ejecuciones de cada galaxia y seleccionar la mejor de ellas

import xlsxwriter
import os
import re
import pandas as pd
from astropy.io import fits
import glob
import numpy as np
import matplotlib.pyplot as plt
import shutil
import matplotlib.font_manager
import matplotlib as mpl

path =r".."
pathdata = r".."

def count_lines(file_path):
   with open(file_path, 'r') as file:
       line_count = 0
       for line in file:
           if line != "\n":
               line_count += 1
       file.close()
       return line_count
    
    
def get_regions(galaxy):

    data = pd.read_excel(pathdata+'\galaxies_data.xlsx',index_col=0)    

    workbook = xlsxwriter.Workbook(pathdata+'/FINAL_EXEC/'+galaxy+'/datos_finales_'+galaxy+'.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write('A1', 'Name')
    worksheet.write('B1', 'S-ALPHA')
    worksheet.write('C1', 'SIZE')
    worksheet.write('D1', 'REGIONES')

    position = 2

    os.chdir(path+'/'+galaxy)
    counthii=0
    
    for i in os.listdir():
        if '.HIIblob_HII.tab.ecsv' in i:
            counthii+=1
                    
    if counthii !=165 and len(os.listdir()) > 1:
        print('LAS EJECUCIONES ESTÁN INCOMPLETAS PARA LA GALAXIA: '+galaxy +' AHORA HAY '+str(len(os.listdir())))
    else:
        for file in os.listdir():

            if 'HIIblob_HII.tab' in file:
                file_path =f"{path}/{galaxy}/{file}"
                m = re.match("([a-zA-Z0-9]*)(\w)(\d\.*\d*)_((\d)\.*(\d)*)\.(\w+)\.(\w){3}\.(\w){4}", f"{file}")

                if m :
                    worksheet.write('A'+str(position), m.group(0))
                    worksheet.write('B'+str(position), float(m.group(3))*data[data['Name'] == m.group(1)].iloc[0].sigma)
                    worksheet.write('C'+str(position), m.group(4))
                    worksheet.write('D'+str(position), count_lines(file_path)-11)
                    position+=1


        workbook.close()
             

def get_X2(galaxy,o,u,forb):

    data = pd.read_excel(pathdata+'\FINAL_EXEC/'+galaxy+'/datos_finales_'+galaxy+'.xlsx')
    if forb == False:
        data['X2'] = ''
    ref = fits.getdata(pathdata+'/RECORTADAS/'+galaxy+'_Ha_final.fits_recortada.fits') # by default it reads the first "data" extension

    for index, n in data.iloc[o:u].iterrows():
        
        dig = fits.getdata(path+'/'+galaxy+'/'+n.Name[:-21]+'_image_DIG.fits', ext=0) # by default it reads the first "data" extension
        hii = fits.getdata(path+'/'+galaxy+'/'+n.Name[:-21]+'_image_HII.fits', ext=0)
        aux = hii+dig
        res = ((aux-ref)*(aux-ref))/(ref)
        data.at[index,'X2']= np.abs(np.sum(res))

    data.to_excel(pathdata+'\FINAL_EXEC/'+galaxy+'/datos_finales_'+galaxy+'.xlsx', index=False)
    
    
    
def select_best(galaxy):
    
    mpl.rcParams['xtick.major.size'] = 15
    mpl.rcParams['xtick.major.width'] = 4
    mpl.rcParams['xtick.minor.size'] = 5
    mpl.rcParams['xtick.minor.width'] = 2

    mpl.rcParams['ytick.major.size'] = 15
    mpl.rcParams['ytick.major.width'] = 4
    mpl.rcParams['ytick.minor.size'] = 5
    mpl.rcParams['ytick.minor.width'] = 2
    data = pd.read_excel(pathdata+'\FINAL_EXEC/'+galaxy+'/datos_finales_'+galaxy+'.xlsx')

    if data.shape[0] == 165:

        workbook = xlsxwriter.Workbook(pathdata+'/FINAL_EXEC/'+galaxy+'/datos_mejores_'+galaxy+'.xlsx')
        worksheet = workbook.add_worksheet()
        
        #HISTOGRAMA
        plt.figure(figsize=(20,10))
        n, bins, patches = plt.hist(x=data['REGIONES'], 
                                    bins='auto',
                                alpha=0.7, rwidth=0.85)

        plt.tick_params(labelsize=25, rotation=45)
        plt.xlabel('Regiones', fontsize=30)
        plt.ylabel('Frecuencia', fontsize=30)
        plt.title(galaxy, fontsize=30, fontname='Helvetica')        
        plt.savefig(pathdata+'\HSTOGRAMS/'+galaxy[3:]+'.png',bbox_inches='tight')
        plt.show()
        
        limit = 0
        for i in range(0,len(n)+1):
            if i < len(n):
                error = np.sqrt(n[i])
                diff = n[i] - n[i+1]

                if error > diff and diff>=0:
                    limit = bins[i]
                    print("LIMITE EN EL NÚMERO DE REGIONES "+str(bins[i]))
                    print("ERROR "+str(error))
                    print("DIFERENCIA "+str(diff))
                    break;
                    
        
                    
        data = pd.read_excel(pathdata+'\FINAL_EXEC/'+galaxy+'/datos_finales_'+galaxy+'.xlsx')
        data = data[data.REGIONES <= limit]
        
        data.sort_values(by=['X2'], inplace=True, ascending=True)

        shutil.copy(path+'/'+galaxy+'/'+data.iloc[0].Name, pathdata+'\FINAL_EXEC/'+galaxy)
        shutil.copy(path+'/'+galaxy+'/'+data.iloc[0].Name[:-21]+'_image_HII.fits', pathdata+'\FINAL_EXEC/'+galaxy)  
        
        return [limit, error, data.iloc[0].X2, data.iloc[0].REGIONES, data.iloc[0]['S-ALPHA'], data.iloc[0].SIZE]
    else:
        return [0,0]


# In[ ]:


for root, subdirectories, files in os.walk(path):
    for s in subdirectories:
        get_regions(s)


# In[ ]:


for root, subdirectories, files in os.walk(path):
    for s in subdirectories:
        get_X2(s)


# In[ ]:


limitdata = pd.DataFrame (columns={'Name','Limit', 'Error', 'X2', 'REGIONES', 'S-ALPHA', 'SIZE'})

for root, subdirectories, files in os.walk(path):
    for s in subdirectories:
        res = select_best(s)
        limitdata = limitdata.append({'Name':s, 'Limit':res[0], 'Error':res[1], 'X2':res[2], 'REGIONES':res[3], 'S-ALPHA':res[4], 'SIZE':res[5]}, ignore_index=True)

limitdata.to_excel(pathdata+'/galaxies_finalEXECDATA.xlsx')

