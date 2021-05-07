# -*- coding: utf-8 -*-
"""
Diego Oliveira de Lemos
"""
import numpy as np
 #gerar matriz com linhas suficientes para cada restrição e função obejtivo
p = ["x1","x2","x3","x4","x5","x6","x7","x8","x9","x10","x11","x12","x13","x14","x15","x16","x17"]
problema = "3x1+3x2+2x3<=30;6x1+3x2+0x3<=48;10x1+8x2+1x3"
def gerar_matriz(var,rest,artif):
    if (artif==0):
        matriz = np.zeros((rest+1, var+rest+2))
    else:
        matriz = np.zeros((rest+2, var+rest+artif+2))
    return matriz

#matriz = gerar_matriz(3, 2,0)
#matriz[0][:] = [0,3,3,2,1,0,30]
#matriz[1][:] = [0,6,3,0,0,1,48]
#matriz[2][:] = [1,-10,-8,-1,0,0,0] # f objetivo
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
    
    
def simplex(matriz):    
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
    print(matriz)
    return matriz  
def fase2_simplex(matriz, n_artif):    
#minimizar as variaveis artificiais (zerar)
    return 0
def resultado_simplex(matriz):
    matriz = np.round(matriz,2)
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


        
def build_matriz(problema):
    temp = []
    for x in range(len(problema)):
        if(problema[x]=="x"):
            temp.append(int(problema[x+1]))
    n_var = max(temp)
    n_artif = problema.count(">=") + problema.count("==")
    n_folga = problema.count("<=")
    n_folga_temp = 0
    n_artif_temp = 0
    linha_folgada = " "
    coluna_folgada = " "
    matriz = gerar_matriz(n_var,n_artif + n_folga, n_artif)
    numlinhas = len(matriz) 
    numcolunas = len(matriz[0])
    
    for x in range(len(p)):
        if(p[x] in problema):
            problema = problema.replace(p[x],"")
    problema = problema.replace("<=","+")
    problema = problema.replace(";","+")    
    lista = problema.split("+")
    print(lista)
    if (n_artif>0):
        for i in range(numlinhas):
            for j in range(numcolunas):
                matriz[i][j] = 0
                
                
                
        fase2_simplex(matriz,n_artif)
        
        
    else:
        for i in range(numlinhas):
            for j in range(numcolunas):
                if (j==0 and i==(numlinhas-1)): #coluno inicial
                    matriz[i][j] = 1
                if (j==0 and i!=(numlinhas-1)): #coluno inicial
                    matriz[i][j] = 0
                if (j>n_var and j!=(numcolunas-1) and i!=(numlinhas-1)): #preenche folga  
                    if (n_folga_temp==i and n_folga_temp < n_folga and (str(i) not in linha_folgada)and (str(j) not in coluna_folgada)):
                        matriz[i][j] = 1
                        n_folga_temp+=1
                        linha_folgada+= (str(i)+" ")
                        coluna_folgada+= (str(j)+" ")
                    else:
                          matriz[i][j] = 0
                if ((j<=n_var and j!=0) or (j==numcolunas-1)):
                    if((j==numcolunas-1)and i==(numlinhas-1)):
                        matriz[i][j] = 0
                    elif (i==(numlinhas-1)):    
                        matriz[i][j] = float(lista.pop(0))*-1
                    else:
                        matriz[i][j] = float(lista.pop(0))
        print(matriz)
        return resultado_simplex(simplex(matriz))
   
   
#matriz = gerar_matriz(2, 2)
#matriz[0][:] =[0, 3, 6, 1, 0, 10]
#matriz[1][:] =[0, 3, 3, 0, 1, 8]
#matriz[2][:] =[1, -30,-48, 0, 0, 0] # f objetivo

 

        
        
resultado_dual =[]  
print(build_matriz(problema))

#print(matriz)
#print(resultado_simplex(simplex(matriz)))   