import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

#abrindo imagem
data = np.load('0_H20_15h10.npy')

img_avg = np.average(data,axis=0) # MÉDIA DOS FRAMES
img = img_avg[:,400:1500]   #CORTANDO A IMAGEM

# plotar para ver como ficou
fig,ax = plt.subplots()
cax = plt.imshow(img, cmap='gray')
cbar = fig.colorbar(cax)
plt.show()

# vamos plotar o histograma dos valores
fig,ax = plt.subplots()
# 2^12 = 4096 é a resolução da câmera
histogram, bin_edges = np.histogram(img, bins=2**12, range=(0.0, 2**12))

plt.plot(bin_edges[0:-1], histogram)
plt.title("Grayscale Histogram")
plt.xlabel("grayscale value")
plt.ylabel("pixels")
plt.xlim(0, 1000)
plt.show()

#chegamos na conclusão que o limiar do fundo é 400
t = 400
#cria a máscara binária 
binary_mask = img > t

#Plotar a máscara
fig, ax = plt.subplots()
plt.imshow(binary_mask, cmap='gray')
plt.show()

#Somar os valores binários em y
# eu vou querer saber onde estão os canais
sum_ydir = np.sum(binary_mask,axis=1)
#encontrar os picos
peaks = find_peaks(sum_ydir, height = 40, distance = 200)
height = peaks[1]['peak_heights'] #list of the heights of the peaks
peak_pos = peaks[0] #list of the peaks positions

#plotar os picos
fig, ax = plt.subplots()
ax.plot(sum_ydir)
ax.scatter(peak_pos,height, color = 'r', s = 15, marker = 'D', label = 'Maxima')
ax.legend()
ax.grid()
plt.show()
#plt.close('all')

#Já encontrei os valores nas "linhas"
#agora vou encontrar nas colunas

xpeak_pos = np.zeros((3,6))
ypeak_pos = np.zeros((3,6))
k=0
for p in peak_pos:
    #encontra a coluna
    binary_crop=binary_mask[int(p-80):int(p+80),:]
    sum_xdir = np.sum(binary_crop,axis=0)
    xpeaks = find_peaks(sum_xdir, height = 20, distance = 200)
    xpeak_pos[:,k] = xpeaks[0]
    j=0
    #reecontra a linha para aum ajuste funo
    for xp in xpeak_pos[:,k]:
         xbinary_crop=binary_mask[:,int(xp-100):int(xp+100)]
         sum_xydir=np.sum(xbinary_crop,axis=1)
         ypeaks = find_peaks(sum_xydir, height = 20, distance = 200)
         ypeak_pos[j,k]=ypeaks[0][k]
         j = j+1
    k = k+1

#até aqui encontramos as coordenadas


#multiplicar a máscara binária pela imagem original
img_mask = img*binary_mask

#plotar a imgem sem fundo junto com as coordenadas
fig, ax = plt.subplots()
plt.imshow(img_mask, cmap='gray')
ax.scatter(xpeak_pos,ypeak_pos, color = 'r', s = 15, marker = 'D')
plt.show()


#Fazer a média dos canais
ch_values = np.zeros((18,1))
i = 0
for x, y in zip(np.reshape(xpeak_pos,(18,1)), np.reshape(ypeak_pos,(18,1))):
    #Pegando 30 px para os lados
    img_ch = img_mask[int(y-30):int(y+30),int(x-30):int(x+30)]
    nz = np.nonzero(img_ch)
    ch_values[i]=np.average(img_ch[nz]/2**12)
    
    #Para ver todos os recortes, descomentar abaixo:
    
    #fig, ax = plt.subplots()
    #plt.imshow(img_ch, cmap='gray')
    #plt.show()
    
    i = i+1
    
ch_values_array = np.reshape(ch_values,(3,6))


