# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 20:57:56 2021

@author: danoc
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


def prepareImage(data,interval):
    img_avg = np.average(data,axis=0)
    img = img_avg[:,interval[0]:interval[1]]
    return img

def plotGray(img):    
    fig,ax = plt.subplots()
    cax = plt.imshow(img, cmap='gray')
    cbar = fig.colorbar(cax)
    plt.show()
    
def plotHistogram(img,Nbits,xmax):
    img[img == 0] = np.nan

    # vamos plotar o histograma dos valores
    fig,ax = plt.subplots()
    histogram, bin_edges = np.histogram(img, bins=2**Nbits, range=(0.0, 2**Nbits))
    
    plt.plot(bin_edges[0:-1], histogram)
    plt.title("Grayscale Histogram")
    plt.xlabel("grayscale value")
    plt.ylabel("pixels")
    plt.xlim(0, xmax)
    plt.show()
    
def getBinaryMask(img,t):

    binary_mask = img > t
    return binary_mask
    

def findPositions(binary_mask,N,dt=200,ht=20,L=80,showPeaks = 'False'):
        
    #Somar os valores binários em y
    # eu vou querer saber onde estão os canais
    sum_ydir = np.sum(binary_mask,axis=1)
    #encontrar os picos
    peaks = find_peaks(sum_ydir, height=ht, distance=dt)
    h = peaks[1]['peak_heights'] #list of the heights of the peaks
    peak_pos = peaks[0] #list of the peaks positions
    
    if showPeaks == 'True':
        plotPeaks(sum_ydir,peak_pos,h)
    #plt.close('all')
    
    #Já encontrei os valores nas "linhas"
    #agora vou encontrar nas colunas
    
    xpeak_pos = np.zeros((N[0],N[1]))
    ypeak_pos = np.zeros((N[0],N[1]))
    k=0
    for p in peak_pos:
        #encontra a coluna
        binary_crop=binary_mask[int(p-L):int(p+L),:]
        sum_xdir = np.sum(binary_crop,axis=0)
        xpeaks = find_peaks(sum_xdir, height=ht, distance=dt)
        xpeak_pos[k,:] = xpeaks[0]
        j=0
        #reecontra a linha para aum ajuste funo
        for xp in xpeak_pos[k,:]:
             xbinary_crop=binary_mask[:,int(xp-L):int(xp+L)]
             sum_xydir=np.sum(xbinary_crop,axis=1)
             ypeaks = find_peaks(sum_xydir, height=ht, distance=dt)
             ypeak_pos[k,j]=ypeaks[0][k]
             j = j+1
        k = k+1
        
    return xpeak_pos, ypeak_pos   
    
    #até aqui encontramos as coordenadas
    

def plotPeaks(y,peak_pos,height):
    #plotar os picos
    fig, ax = plt.subplots()
    ax.plot(y)
    ax.scatter(peak_pos,height, color = 'r', s = 15, marker = 'D', label = 'Maxima')
    ax.legend()
    ax.grid()
    plt.show()
    

def plotxyPeaks(img,x,y):
#plotar a imgem sem fundo junto com as coordenadas
    fig, ax = plt.subplots()
    plt.imshow(img, cmap='gray')
    ax.scatter(x,y, color = 'r', s = 15, marker = 'D')
    plt.show()


def averageROI(img_mask,xpeak_pos,ypeak_pos,N,Nbits,roiSz=30,plotROI='False'):    
     #Fazer a média dos canais
    ch_values = np.zeros((N[0]*N[1],1))
    i = 0
    for x, y in zip(np.reshape(xpeak_pos,(N[0]*N[1],1)), np.reshape(ypeak_pos,(N[0]*N[1],1))):
        #Pegando 30 px para os lados
        img_ch = img_mask[int(y-roiSz):int(y+roiSz),int(x-roiSz):int(x+roiSz)]
        nz = np.nonzero(img_ch)
        ch_values[i]=np.average(img_ch[nz]/2**Nbits)
        
        #Para ver todos os recortes, descomentar abaixo:
        
        if plotROI == 'True': 
        
            fig, ax = plt.subplots()
            plt.imshow(img_ch, cmap='gray')
            plt.show()
        
        i = i+1
        
    ch_values_array = np.reshape(ch_values,(N[0],N[1]))
    return ch_values_array   



def maxROI(img_mask,xpeak_pos,ypeak_pos,N,Nbits,roiSz=30,plotROI='False'):    
     #Fazer a média dos canais
    ch_values = np.zeros((N[0]*N[1],1))
    i = 0
    for x, y in zip(np.reshape(xpeak_pos,(N[0]*N[1],1)), np.reshape(ypeak_pos,(N[0]*N[1],1))):
        #Pegando 30 px para os lados
        img_ch = img_mask[int(y-roiSz):int(y+roiSz),int(x-roiSz):int(x+roiSz)]
        nz = np.nonzero(img_ch)
        ch_values[i]=np.max(img_ch[nz]/2**Nbits)
        
        #Para ver todos os recortes, descomentar abaixo:
        
        if plotROI == 'True': 
        
            fig, ax = plt.subplots()
            plt.imshow(img_ch, cmap='gray')
            plt.show()
        
        i = i+1
        
    ch_values_array = np.reshape(ch_values,(N[0],N[1]))
    return ch_values_array       




def sumROI(img_mask,xpeak_pos,ypeak_pos,N,Nbits,roiSz=30,plotROI='False'):    
     #Fazer a média dos canais
    ch_values = np.zeros((N[0]*N[1],1))
    i = 0
    for x, y in zip(np.reshape(xpeak_pos,(N[0]*N[1],1)), np.reshape(ypeak_pos,(N[0]*N[1],1))):
        #Pegando 30 px para os lados
        img_ch = img_mask[int(y-roiSz):int(y+roiSz),int(x-roiSz):int(x+roiSz)]
        nz = np.nonzero(img_ch)
        ch_values[i]=np.sum(img_ch[nz]/2**Nbits)
        
        #Para ver todos os recortes, descomentar abaixo:
        
        if plotROI == 'True': 
        
            fig, ax = plt.subplots()
            plt.imshow(img_ch, cmap='gray')
            plt.show()
        
        i = i+1
        
    ch_values_array = np.reshape(ch_values,(N[0],N[1]))
    return ch_values_array   


def topROI(img_mask,xpeak_pos,ypeak_pos,N,Nbits,n,roiSz=30,plotROI='False'):    
     #Fazer a média dos canais
    ch_values = np.zeros((N[0]*N[1],1))
    i = 0
    for x, y in zip(np.reshape(xpeak_pos,(N[0]*N[1],1)), np.reshape(ypeak_pos,(N[0]*N[1],1))):
        #Pegando 30 px para os lados
        img_ch = img_mask[int(y-roiSz):int(y+roiSz),int(x-roiSz):int(x+roiSz)]
        nz = np.nonzero(img_ch)
        ch_values[i]=avg_of_top_n(img_ch[nz]/2**Nbits, n)
        
        #Para ver todos os recortes, descomentar abaixo:
        
        if plotROI == 'True': 
        
            fig, ax = plt.subplots()
            plt.imshow(img_ch, cmap='gray')
            plt.show()
        
        i = i+1
        
    ch_values_array = np.reshape(ch_values,(N[0],N[1]))
    return ch_values_array   


def avg_of_top_n(l, n):
    return sum(sorted(l)[-n:]) / n