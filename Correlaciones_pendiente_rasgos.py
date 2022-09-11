#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Código para obtener las correlaciones entre las pendientes de las funciones de luminosidad y los rasgos globales de las galaxias

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy import stats
from matplotlib import container

#Masa estelar

path =r""

mpl.rcParams['xtick.major.size'] = 15
mpl.rcParams['xtick.major.width'] = 4
mpl.rcParams['xtick.minor.size'] = 5
mpl.rcParams['xtick.minor.width'] = 2

mpl.rcParams['ytick.major.size'] = 15
mpl.rcParams['ytick.major.width'] = 4
mpl.rcParams['ytick.minor.size'] = 5
mpl.rcParams['ytick.minor.width'] = 2

data = pd.read_excel(path+'/galaxies_data - Copy.xlsx',index_col=0) 

#PLOT
plt.figure(figsize=(20,10))
plt.rcParams["figure.figsize"] = [7.50, 3.50]

#Separación de datos con anomalías

dataok = data[(data.Name != 'NGC3486') &(data.Name != 'NGC5448') &(data.Name != 'NGC7606') 
              & (data.Name != 'NGC4654') & (data.Name != 'UGC4621') & (data.Name != 'NGC4814')
              & (data.Name != 'NGC5364') & (data.Name != 'UGC11818') & (data.Name != 'NGC3430') & (data.Name != 'UGC4375')]

datawrong = data[(data.Name == 'NGC3486') |(data.Name == 'NGC5448')
                 |(data.Name == 'NGC7606') |(data.Name == 'NGC4654')
                 | (data.Name == 'UGC4621') | (data.Name == 'NGC4814')
                 | (data.Name == 'NGC5364') | (data.Name == 'UGC11818')
                 | (data.Name == 'NGC3430') | (data.Name == 'UGC4375')]


#Tests de Spearman
print('SPEARMAN')
print(stats.spearmanr(data.mass,data.slope))

spearman = stats.spearmanr(dataok.mass,dataok.slope)

corr = str(round(spearman.correlation,4))
pval =str(round(spearman.pvalue,4))

spearman2 = stats.spearmanr(datawrong.mass,datawrong.slope)

corr2 = str(round(spearman2.correlation,4))
pval2 =str(round(spearman2.pvalue,4))

#Gráfica

fig,ax = plt.subplots(figsize=(14,8))


fig1 = ax.errorbar(dataok.mass,dataok.slope, yerr=dataok.error, color='mediumblue', fmt='o', markersize='9', label=r' ${\rho}$='+corr+r' / p-value='+pval)

fig2 = ax.errorbar(datawrong.mass,datawrong.slope, yerr=datawrong.error, color='#8C000F', fmt='o', markersize='9', label=r' ${\rho}$='+corr2+r' / p-value='+pval2)

plt.xlabel(r'log(${M_{\star}}$[${M_{\odot}}$])', fontsize=30)
plt.ylabel(r"$\alpha$", fontsize=30)
plt.title(r"$\alpha$ vs log(${M_{\star}}$[${M_{\odot}}$])", fontsize=30, fontname='Helvetica')   
plt.tick_params(labelsize=25, rotation=45)
ax = plt.gca()
plt.legend(loc="upper right", handlelength=0, handletextpad=0, fancybox=True, fontsize=27, markerscale=1)

plt.savefig(r'../alphavsmasa.png',bbox_inches='tight')
plt.show()
            


# In[ ]:


#Tipo morfológico

plt.figure(figsize=(20,10))
plt.rcParams["figure.figsize"] = [7.50, 3.50]

#Separación de datos con anomalías

dataok = data[(data.Name != 'NGC3486') &(data.Name != 'NGC5448') &(data.Name != 'NGC7606') 
              & (data.Name != 'NGC4654') & (data.Name != 'UGC4621') & (data.Name != 'NGC4814')
              & (data.Name != 'NGC5364') & (data.Name != 'UGC11818') & (data.Name != 'NGC3430') & (data.Name != 'UGC4375')]

datawrong = data[(data.Name == 'NGC3486') |(data.Name == 'NGC5448')
                 |(data.Name == 'NGC7606') |(data.Name == 'NGC4654')
                 | (data.Name == 'UGC4621') | (data.Name == 'NGC4814')
                 | (data.Name == 'NGC5364') | (data.Name == 'UGC11818')
                 | (data.Name == 'NGC3430') | (data.Name == 'UGC4375')]

#Tests de Spearman
print('SPEARMAN')
spearman = stats.spearmanr(dataok.numtype,dataok.slope)

corr = str(round(spearman.correlation,4))
pval =str(round(spearman.pvalue,4))
print(spearman)


spearman2 = stats.spearmanr(datawrong.numtype,datawrong.slope)

corr2 = str(round(spearman2.correlation,4))
pval2 =str(round(spearman2.pvalue,4))

#Gráfica

fig,ax = plt.subplots(figsize=(14,8))


fig1 = ax.errorbar(dataok.numtype,dataok.slope, yerr=dataok.error, color='mediumblue', fmt='o', markersize='9', label=r' ${\rho}$='+corr+r' / p-value='+pval)
fig2 = ax.errorbar(datawrong.numtype,datawrong.slope, yerr=datawrong.error, color='#8C000F', fmt='o', markersize='9', label=r' ${\rho}$='+corr2+r' / p-value='+pval2)


plt.xlabel(r'T', fontsize=30)
plt.ylabel(r"$\alpha$", fontsize=30)
plt.title(r"$\alpha$ vs T", fontsize=30, fontname='Helvetica')   
plt.tick_params(labelsize=25, rotation=45)
ax = plt.gca()
plt.legend(loc="upper right", handlelength=0, handletextpad=0, fancybox=True, fontsize=27, markerscale=1)

plt.savefig(r'../alphavst.png',bbox_inches='tight')
plt.show()
            

