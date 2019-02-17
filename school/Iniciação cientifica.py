from math import *
import os
import random

def lerserie(arquivo):# TODO fazer ler serie e retornar serie_k preenchida para k =1,2,...,c
	pass
	
def preencheserie(serietemporal): # preenche serie temporal com valores aleatorios para teste
	cont = 0
	while cont<10:
		x = random.uniform(7,10)
		serietemporal.append(round(x,2))
		cont = cont + 1
	#serietemporal = [7.07,7.09,7.41,7.41,7.5,7.71,7.89,7.95,8.44,8.64,9.13,9.18,9.2,9.81,9.92]
	return serietemporal

def sort(serietemporal):   # quicksort FUNCIONANDO
    less = []
    equal = []
    greater = []

    if len(serietemporal) > 1:
        pivot = serietemporal[0]
        for x in serietemporal:
            if x < pivot:
                less.append(x)
            if x == pivot:
                equal.append(x)
            if x > pivot:
                greater.append(x)
        return sort(less)+equal+sort(greater)
    else:
        return serietemporal	

def calculot(serietemporal): # calcula o valor de parada do algoritmo FUNCIONANDO
	cont = 0
	t = 0
	while (cont<(len(serietemporal)-1)):
		t = t + (serietemporal[cont+1]-serietemporal[cont])
		cont += 1
	t = round(t/(len(serietemporal)-1),3)
	return t
		
def separaclusters(serie,seriefuzzificada): #separa todos os termos iniciais cada um em seu cluster
	cont = 0
	while (cont<len(serie)):
		locals()["cluster"+str(cont)] = []
		locals()["cluster"+str(cont)].append(serie[cont])
		locals()["cluster"+str(cont)].append(serie[cont])
		seriefuzzificada.append(locals()["cluster"+str(cont)])
		cont += 1
	return seriefuzzificada
		
def calculacentroide(seriefuzzificada): ####termo [0] da matrix é o centroide
	cont = 0
	while cont<len(seriefuzzificada):
		seriefuzzificada[cont][0] = round(sum2(seriefuzzificada,cont)/(len(seriefuzzificada[cont])-1),3)
		cont += 1
	return seriefuzzificada

def sum2(seriefuzzificada,cont):  #somatorio dos valores da matrix excluindo o primeiro digito
	cont2 = 1
	s = 0
	while cont2<len(seriefuzzificada[cont]):
		s += seriefuzzificada[cont][cont2]
		cont2 += 1
	return s
	
def calculadistancia(seriefuzzificada): #retorna a distancia entre os centroides
	cont = 0
	dif = []
	while cont<len(seriefuzzificada) - 1:
		dif.append(round(seriefuzzificada[cont+1][0] - seriefuzzificada[cont][0], 3))
		cont += 1
	return dif

def removeunitarios(seriefuzzificada,excluidos): #remove os valores isolados(centroides) da matrix	
	cont = 0
	while cont < len(excluidos):
		seriefuzzificada[excluidos[cont]] = 0
		cont += 1
	cont = 0
	while cont < len(seriefuzzificada):
		if seriefuzzificada[cont] == 0:
			seriefuzzificada.pop(cont)
			cont -= 1
		cont +=1
	return seriefuzzificada

def juntaClusters(seriefuzzificada,dif,t): # junta os clusters
	cont = 0
	excluidos = []
	while cont<len(dif):
		contaux = cont
		while dif[cont] < t:
			seriefuzzificada[cont+1].pop(0)
			excluidos.append(cont+1)
			seriefuzzificada[contaux] = seriefuzzificada[contaux] + seriefuzzificada[cont+1]
			cont += 1
			if cont>len(dif)-1:
				break
		cont += 1
	seriefuzzificada = removeunitarios(seriefuzzificada,excluidos)
	#### funcionando até aqui
	menorT = sum(i<t for i in dif)
	if menorT > 0:
		seriefuzzificada = calculacentroide(seriefuzzificada)
		dif = calculadistancia(seriefuzzificada)
		seriefuzzificada = juntaClusters(seriefuzzificada,dif,t)
		return seriefuzzificada
	else:
		return seriefuzzificada
		
def fuzzyficacao(serie,seriefuzzificada): # realiza fuzzyficacao da serie
	dif = []
	serie = sort(serie)
	t = calculot(serie)
	seriefuzzificada = separaclusters(serie,seriefuzzificada)
	dif = calculadistancia(seriefuzzificada)
	seriefuzzificada = juntaClusters(seriefuzzificada,dif,t)
	return seriefuzzificada
	
def preencheclusters(matrixclusters,seriefuzzificada): # preenche clusters, e cria automaticamente o 1 e o ultimo cluster variando de -infinito a +infinito
	cluster0 = [-1e200,seriefuzzificada[0][0],seriefuzzificada[1][0]]
	matrixclusters.append(cluster0)
	cont = 1
	while cont<len(seriefuzzificada)-1:
		ci = seriefuzzificada[cont-1][0]
		cc = seriefuzzificada[cont][0]
		cf = seriefuzzificada[cont+1][0]
		locals()["cluster"+str(cont)] = []
		locals()["cluster"+str(cont)].append(ci)
		locals()["cluster"+str(cont)].append(cc)
		locals()["cluster"+str(cont)].append(cf)
		matrixclusters.append(locals()["cluster"+str(cont)])
		cont=cont+1
	alto = [seriefuzzificada[cont-1][0],seriefuzzificada[cont][0],1e200]
	matrixclusters.append(alto)
	return matrixclusters	
	
def inferencia(seriefuzzificada,matrixclusters): #management oara calculo da inferencia
	seriemaiorinferencia = []
	seriemenorinferencia = []
	cont = 0
	while cont<len(seriefuzzificada):
		contn = 1
		while contn<len(seriefuzzificada[cont]):
			inf1,inf2 = calculainferencia(seriefuzzificada[cont][contn],matrixclusters)
			seriemaiorinferencia.append(inf1)
			seriemenorinferencia.append(inf2)
			contn+=1
		cont +=1 
	return seriemaiorinferencia,seriemenorinferencia

def calculainferencia(x,matrixclusters): #calculo real da inferencia
	inft1 = []
	inft2 = []
	if (x < matrixclusters[0][1]):
		inft1.append(1)
		inft1.append(1)
		inft2.append(0)
		inft2.append(2)
		return inft1,inft2
	if (x > matrixclusters[len(matrixclusters)-1][1]):
		inft1.append(1)
		inft1.append(len(matrixclusters))
		inft2.append(0)
		inft2.append(len(matrixclusters)-1)
		return inft1,inft2
	cont = 0
	while x>matrixclusters[cont][1]:
		cont +=1
	if cont+1 == len(matrixclusters):
		inf1 = round((x - matrixclusters[cont][0])/(matrixclusters[cont][1] - matrixclusters[cont][0]),3)
		inf2 = round(1 - inf1,3)
		inft1.append(inf1)
		inft1.append(cont)
		inft2.append(inf2)
		inft2.append(cont+1)
		inft1,inft2 = verificamaior(inft1,inft2)
		return inft1,inft2
	if matrixclusters[cont+1][1] - x > x - matrixclusters[cont][1]:
		cont -= 1
		inf1 = round((matrixclusters[cont][2] - x)/(matrixclusters[cont][2] - matrixclusters[cont][1]),3)
		inf2 = round(1 - inf1,3)
		inft1.append(inf1)
		inft1.append(cont+1)
		inft2.append(inf2)
		inft2.append(cont+2)
	else:
		inf1 = round((x - matrixclusters[cont][0])/(matrixclusters[cont][1] - matrixclusters[cont][0]),3)
		inf2 = round(1 - inf1,3)
		inft1.append(inf1)
		inft1.append(cont+2)
		inft2.append(inf2)
		inft2.append(cont+1)
	inft1,inft2 = verificamaior(inft1,inft2)
	return inft1,inft2

def verificamaior(inft1,inft2):  #verifica a maior inferencia
	if(inft1[0] > inft2[0]):
		return inft1,inft2
	else:
		return inft2,inft1

def printmatrix(matrix):
	cont = 0
	while cont<len(matrix):
		print(matrix[cont])
		cont += 1

def calculodtw(seriemaiorinferencia,seriemaiorinferencia2): #monta a matrix dtw com todas as distancias euclidianas
	dtw = [[0 for x in range(len(seriemaiorinferencia))] for y in range(len(seriemaiorinferencia2))]
	cont = 0
	while cont<len(seriemaiorinferencia):
		cont2 = 0
		while cont2 < len(seriemaiorinferencia2):
			distancia = seriemaiorinferencia[cont][0] - seriemaiorinferencia2[cont2][0]
			if distancia<0:
				distancia = distancia * -1
			dtw[cont][cont2] = round(distancia,3)
			cont2 += 1
		cont += 1
	return sumultimacasa(dtw,len(seriemaiorinferencia),len(seriemaiorinferencia2))

def sumultimacasa(dtw,col,lin):
	print("matrix DTW :\n")
	printmatrix(dtw)
	soma = dtw[0][0]
	x = 0
	y = 0
	while (x<lin and y<col):
		if x + 1 == lin:
			while y+1<col:
				y += 1
				soma += dtw[x][y]
			return soma
		if y + 1 == col:
			while x+1<lin:
				x += 1
				soma += dtw[x][y]
			return soma	
		if dtw[x+1][y] < dtw[x+1][y+1] and dtw[x+1][y] < dtw[x][y+1]:
			soma += dtw[x+1][y]
			x += 1
		else:
			if dtw[x][y+1] < dtw[x+1][y+1] and dtw[x][y+1] < dtw[x+1][y]:
				soma += dtw[x][y+1]
				y +=1
			else:
				soma += dtw[x+1][y+1]
				x += 1
				y += 1
	return soma

#tudo funcionando daqui pra cima



#main
serie = []
seriefuzzificada = []
matrixclusters = []
serie = preencheserie(serie)
seriefuzzificada = fuzzyficacao(serie,seriefuzzificada)
matrixclusters = preencheclusters(matrixclusters,seriefuzzificada)
seriemaiorinferencia = []
seriemenorinferencia = []
seriemaiorinferencia,seriemenorinferencia = inferencia(seriefuzzificada,matrixclusters)

serie2 = []
seriefuzzificada2 = []
matrixclusters2 = []
serie2 = preencheserie(serie2)
seriefuzzificada2 = fuzzyficacao(serie2,seriefuzzificada2)
matrixclusters2 = preencheclusters(matrixclusters2,seriefuzzificada2)
seriemaiorinferencia2 = []
seriemenorinferencia2 = []
seriemaiorinferencia2,seriemenorinferencia2 = inferencia(seriefuzzificada2,matrixclusters2)
dtw = calculodtw(seriemaiorinferencia,seriemaiorinferencia2)
print("valor final do DTW i,j = ",dtw)

