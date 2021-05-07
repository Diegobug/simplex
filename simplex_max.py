# -*- coding: utf-8 -*-
"""
Diego Oliveira de Lemos
"""
import numpy as np
import matplotlib.pyplot as plt

FOLGA = 0
EXCESSO = 1
ARTIFICIAL = 2
controle=[]

p = ["x1","x2","x3","x4","x5","x6","x7","x8","x9","x10","x11","x12","x13","x14","x15","x16","x17"]

problema = "3x1+3x2+2x3<=30;6x1+3x2+0x3<=48;10x1+8x2+1x3"

#problema = "2x1+2x2<=4;1x1+0x2>=1;1x1+1x2==2;2x1+3x2"
temp = problema.split(";")
for i in range (len(temp)-1):
    if "==" in temp[i]:
        controle.append(ARTIFICIAL)
    elif ">=" in temp[i]:
        controle.append(EXCESSO)
    elif "<=" in temp[i]:
        controle.append(FOLGA)
#gerar matriz com linhas suficientes para cada restrição e função obejtivo       
def gerar_matriz(var,rest,artif):
    if (artif==0):
        matriz = np.zeros((rest+1, var+rest+2))
    else: #consertar
        matriz = np.zeros((rest+1, var+rest+artif+1))
    return matriz

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
            for j in range (numcolunas):
                if i!=(linha):
                    matriz[i][j] =  matriz[linha][j]*n + matriz[i][j]
    return matriz  

def fase2_simplex(matriz, n_artif, l):    
#minimizar as variaveis artificiais (zerar)
    print(l)
    numlinhas = len(matriz) 
    numcolunas = len(matriz[0])

    for i in range(len(l)):
        for j in range(numcolunas):
            matriz[numlinhas-1][j] -= matriz[l[i]][j]
     
    matriz = simplex(matriz)
#remover linha e colunas artificiais
    matriz = np.delete(matriz,numlinhas-1,0)
    for i in range(len(l)):
        matriz = np.delete(matriz,numcolunas-3,1)
#chama o simplex novamente       
    return resultado_simplex(simplex(matriz))

def resultado_simplex(matriz):
    matriz = np.round(matriz,2)
    res_simplex =[]
    numlinhas = len(matriz) 
    numcolunas = len(matriz[0])
    for i in range (numlinhas): 
        for j in range (numcolunas-1):
            if j>0 and j < numcolunas-2: #consertar
                if (matriz[i][j]) ==1:
                    res_simplex.append(matriz[i][numcolunas-1])
            if ( j==0 and matriz[i][j]==1):
                res_simplex.append(matriz[i][numcolunas-1])
    print(matriz)
    return res_simplex


        
def build_matriz(problema): #linha 113 à 140 é só ajustes
    temp = []
    for x in range(len(problema)):
        if(problema[x]=="x"):
            temp.append(int(problema[x+1]))
    n_var = max(temp)
    n_artif = problema.count(">=") + problema.count("==")
    n_folga = problema.count("<=") #+ problema.count(">=")
    n_folga_temp = 0
    n_artif_temp = 0
    linha_folgada = " "
    coluna_folgada = " "
    linha_artificial=[]
    linha_artificializada= ""
    coluna_artificializada= ""
    
    matriz = gerar_matriz(n_var,n_artif + n_folga, n_artif)

    numlinhas = len(matriz) 
    numcolunas = len(matriz[0])
    
    for x in range(len(p)):
        if(p[x] in problema):
            problema = problema.replace(p[x],"")
    problema = problema.replace("==","+")  
    problema = problema.replace(">=","+")        
    problema = problema.replace("<=","+")
    problema = problema.replace(";","+")    
    lista = problema.split("+")
 
    if (n_artif>0):#duas fases
        for i in range(numlinhas):
            for j in range(numcolunas):
                if (j==0 and i==(numlinhas-1)): #coluno inicial
                    matriz[i][j] = 1
                if (j==0 and i!=(numlinhas-1)): #coluno inicial
                    matriz[i][j] = 0
                if (j>n_var and j!=(numcolunas-1) and i!=(numlinhas-1)): #preenche folga  
                    if ( n_folga_temp <= n_folga and (str(i) not in linha_folgada)and (str(j) not in coluna_folgada)):
                        if controle[i] == EXCESSO: 
                            matriz[i][j] = -1
                        else:
                            matriz[i][j] = 1
                        n_folga_temp+=1
                        linha_folgada+= (str(i)+" ")
                        coluna_folgada+= (str(j)+" ")
                        
                if (j>(n_var + n_folga) and j!=(numcolunas-1) and i!=(numlinhas-1)): #preenche ARTIFICAL  
                    if ( n_artif_temp <= n_artif and (str(i) not in linha_artificializada)and (str(j) not in coluna_artificializada) and matriz[i][j]==0):
                        if controle[i] == EXCESSO or controle[i] == ARTIFICIAL: #consertar
                            matriz[i][j] = 1
                            linha_artificial.append(i)
                        n_artif_temp+=1
                        linha_artificializada+= (str(i)+" ")
                        coluna_artificializada+= (str(j)+" ")
                        
                if ((j<=n_var and j!=0) or (j==numcolunas-1)): #preenche a f obj
                    if((j==numcolunas-1)and i==(numlinhas-1)):
                        matriz[i][j] = 0
                    elif (i==(numlinhas-1)):    
                        matriz[i][j] = float(lista.pop(0))*-1
                    else:
                        matriz[i][j] = float(lista.pop(0))
                
        #inclusão da linha artificial na parte de baixo da matriz       
        vet_artif = [0]*numcolunas
        temp = n_artif
        while(temp>0):
            vet_artif[numcolunas-temp-1] = 1
            temp-=1
        nova_matriz = np.zeros((numlinhas+1,numcolunas))
        for i in range(numlinhas+1):
            for j in range(numcolunas):
                if i< numlinhas: 
                    nova_matriz[i][j]=matriz[i][j]
                else:
                    nova_matriz[i][j]=vet_artif[j]
        print(linha_artificializada[1:])

        print(fase2_simplex(nova_matriz,n_artif,linha_artificial))
        
        
    else: #simplex normal
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
          
        
resultado_dual = []  
print(build_matriz(problema))

#print(matriz)
#print(resultado_simplex(simplex(matriz)))   