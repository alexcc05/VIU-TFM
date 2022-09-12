#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Código para recortar las imágenes Halpha

from astropy.io import fits
from astropy.nddata import Cutout2D
from astropy.wcs import WCS
import os
import pandas as pd

path = '..'

dataPositions = pd.read_excel(path+'RECORTE_POSICIONES.xlsx')

for filename in os.listdir(path+'/final_fits/HALPHA/'):

    if 'Ha' in filename and '4654' in filename:
        data = dataPositions[dataPositions['Name'] == filename[:-14]]
        
        if data.iloc[0].X != '-':
            position = (data.iloc[0].POSX, data.iloc[0].POSY)
            size = (data.iloc[0].Y, data.iloc[0].X,)
            f = os.path.join(path+'/final_fits/HALPHA/',filename)
            
            if os.path.isfile(f):
                hdu = fits.open(f)[0]
            
                wcs = WCS(hdu.header)
                
                cutout = Cutout2D(hdu.data, position=position, size=size, wcs=wcs)

                hdu.data = cutout.data
                
                hdu.header.update(cutout.wcs.to_header())
                
                hdu.writeto(path+'/RECORTADAS/'+filename+'_recortada.fits', overwrite=True)

