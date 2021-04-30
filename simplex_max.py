# -*- coding: utf-8 -*-
"""
Diego Oliveira de Lemos
"""
import numpy as np
 #gerar matriz com linhas suficientes para cada restrição e função obejtivo
def gerar_matriz(var,rest):
    matriz = np.zeros((rest+1, var+rest+2))
    return matriz

matriz = gerar_matriz(3, 2)
matriz[0][:] = [0,3,3,2,1,0,30]
matriz[1][:] = [0,6,3,0,0,1,48]
matriz[2][:] = [1,-10,-8,-1,0,0,0] # f objetivo

#matriz = gerar_matriz(2, 2)
#matriz[0][:] =[0, 3, 6, 1, 0, 10]
#matriz[1][:] =[0, 3, 3, 0, 1, 8]
#matriz[2][:] =[1, -30,-48, 0, 0, 0] # f objetivo

def coluna_pivo(matriz):
    r = len(matriz[:,0])
    arrayTemp = matriz[r-1,:-1].tolist()
    x = min(matriz[r-1,:-1])
    #print(x) #encontra o indice da coluna com menor valor na linha da f objetivo
    if x>=0:
        return False
    else:
        return arrayTemp.index(x)
   
def linha_pivo(matriz):     
    if coluna_pivo(matriz)!= False:
        temp = []
        for i, b in zip(matriz[:-1,coluna_pivo(matriz)],matriz[:-1,-1]):
            if b/i>0:
                temp.append(b/i)
                #print(b/i)
            #else:                
                #temp.append(10000)
        indice = temp.index(min(temp))
        return indice
    
    
    
while coluna_pivo(matriz)!=False:   
    linha = linha_pivo(matriz)
    coluna = coluna_pivo(matriz)
    print(linha)
    print(coluna)

    matriz[linha][:]= (matriz[linha][:])/matriz[linha][coluna] #atualizei a linha pivo
    pivo = matriz[linha][coluna]

    numlinhas = len(matriz) 
    numcolunas = len(matriz[0])
 
    for i in range (numlinhas):
        n = -(matriz[i][coluna])/pivo
        print (n)
        for j in range (numcolunas):
            if i!=(linha):
                matriz[i][j] =  matriz[linha][j]*n + matriz[i][j]
    
    #print(matriz)   

        
        
resultado_dual =[]  
matriz = np.round(matriz,2)
def resultado_simplex(matriz):
    res_simplex =[]
    numlinhas = len(matriz) 
    numcolunas = len(matriz[0])
    for i in range (numlinhas):
        for j in range (numcolunas-1):
            if j>0:
                if (matriz[i][j]) ==1:
                    res_simplex.append(matriz[i][numcolunas-1])
            if ( j==0 and matriz[i][j]==1):
                res_simplex.append(matriz[i][numcolunas-1])
    return res_simplex


print(matriz)
print(resultado_simplex(matriz))   