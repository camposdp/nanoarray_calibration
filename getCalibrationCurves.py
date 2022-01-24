#O objetivo principal desse processamento é definir qual o valor de 
#sensibilidade de cada arranjo de nanoburacos: 
#qual a variação de intensidade por unidade de índice de refração. 

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import time

df=pd.read_csv('calibra.csv', sep=';',header=None)
cal=df.values


ch = np.zeros((10,3))

r = 6
c = 3

reps = 3
samples = 10
f=1
for k in range(r):
    for w in range(c):

        for j in range(reps):
            for i in range(samples):
        
            
                path = os.getcwd()
                folder = '\\data_glicose'
                prefix = '_GLICOSE_R'
                sufix = '_max.npy'
                
                file = '\\'+str(i+1)+prefix+str(j+1)+sufix
                trial=np.load(path+folder+file)
                ch[i,j]=trial[k,w]
        
        y=np.mean(ch,1)
        y_std=np.std(ch,1)
     
        x = cal[1:11,2]
        plt.figure(f)
        f = f+1
        plt.plot(x,y)
        
        
        #plt.errorbar(x, y, yerr=y_std, xerr=None)


