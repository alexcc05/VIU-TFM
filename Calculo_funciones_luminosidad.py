#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Código para obtener las funciones de luminosidad de las galaxias

import powerlaw
import xlsxwriter
import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


path =r".."

mpl.rcParams['xtick.major.size'] = 15
mpl.rcParams['xtick.major.width'] = 4
mpl.rcParams['xtick.minor.size'] = 5
mpl.rcParams['xtick.minor.width'] = 2

mpl.rcParams['ytick.major.size'] = 15
mpl.rcParams['ytick.major.width'] = 4
mpl.rcParams['ytick.minor.size'] = 5
mpl.rcParams['ytick.minor.width'] = 2

slopes = pd.DataFrame(columns={'Name','Slope', 'Error', 'Lmin'})
        

for root, subdirectories, files in os.walk(path+'\FINAL_EXEC'):
      for s in subdirectories:
        data = pd.read_excel(path+'\FINAL_EXEC/'+s+'/'+s+'_datosluminosidad.xlsx',index_col=0)    
        plt.figure(figsize=(20,10))
        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        fit = powerlaw.Fit(data=data.luminosity, xmin= min(data.luminosity), xmax= max(data.luminosity))

        print(fit.power_law.sigma)
        print(fit.power_law.xmin)
        fig2 = fit.plot_pdf(color='#8C000F', linestyle=None,linewidth=0, marker='o', markersize=15 )

        alpha = str(round(fit.power_law.alpha,2))
        err ="{:.2f}".format(round(fit.power_law.sigma,2))

        if float(err) > 0.1:
            alpha = str(round(fit.power_law.alpha,1))
            err ="{:.1f}".format(round(fit.power_law.sigma,1))

        fig = fit.power_law.plot_pdf(color='#006400', linewidth=3,linestyle='--', 
                                     ax=fig2, label='\u03B1='+alpha+'\u00B1'+str(err))
        fig.set_title(s)

        slopes = slopes.append({'Name':s, 'Slope':alpha, 'Error':err, 'Lmin':fit.power_law.xmin}, ignore_index=True)


        plt.xlabel(r'$L_{H_{\alpha}}$[$ergs^{-1}$]', fontsize=30)
        plt.ylabel(r"$\rho$(L)", fontsize=30)
        plt.title(s, fontsize=30, fontname='Helvetica')   
        plt.tick_params(labelsize=25, rotation=45)

        plt.legend(loc="upper right", handlelength=0, handletextpad=0, fancybox=True, fontsize=27)
        plt.savefig(path+'\POWERLAW/'+s[3:]+'.png',bbox_inches='tight')
        plt.show()


# In[ ]:


slopes.to_excel(path+'/POWERLAW/slopes.xlsx')

