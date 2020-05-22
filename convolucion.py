#INSTITUTO POLITÉCNICO NACIONAL - ESCUELA SUPERIOR DE CÓMPUTO
#Bonilla Reyes José Luis
#Domínguez Morales José Manuel

import os
from sys import platform
from matplotlib import pyplot as plt
import numpy as np

#Funcion que detecta el sistema operativo y relaciona su comando para borrar la pantalla
def clearScreen():
    if platform == "win32":
        os.system("cls")
    else:
        os.system("clear")

#Funcion que guarda la secuencia de los elementos introducidos por el usuario
#Recibe como parámetro el nombre de la secuencia
#Regresa una lista, que es la secuencia
def ingresa_serie(nom):
	s = []
	sn = int(input("Numero de elementos de " + nom + ": "))

	print("Ingresa la secuencia " + nom + " :\n ")
	while( len(s) < sn):
		number = input(( nom +" = " + str(s) + ": "))
		try:
			number = int(number)
		except ValueError :
			number = float(number)

		s.append(number)
	clearScreen()
	print(nom + " = " + str(s))
	return s

def graficar(serie,ini,titulo):
	n = len(serie)
	n_max = max(serie)
	n_min = min(serie)
	if(n_min > 0):
		n_min = 0

	aux = range(-n-2,n+2,1)
	#print(aux)
	grafica = [0 for i in aux]
	indice0 = int(len(grafica)/2)
	grafica[indice0] = serie[ini]
	#print(indice0)

	aux_ini = ini - 1
	var_aux = indice0 - 1
	while aux_ini >= 0:
		grafica[var_aux] = serie[aux_ini]
		aux_ini -=1
		var_aux -=1

	aux_ini = ini + 1
	var_aux = indice0 + 1
	while aux_ini < n:
		grafica[var_aux] = serie[aux_ini]
		aux_ini +=1
		var_aux +=1

	for index,element in enumerate(grafica):
		if element == 0 and grafica[index-1] == 0 or grafica[index-1] == None and grafica[index+1]==0 and index > 0 and index < len(grafica)-2:
			grafica[index]=None

	markerline, stemlines, baseline = plt.stem(aux, grafica, '-',use_line_collection=True)
	plt.setp(baseline,color='r', linewidth= 2)
	for i,j in zip(aux,grafica):
		if(i!=None and j!=None ):
			plt.annotate(str(j),xy=(i,j+0.1))

	#plt.plot(aux,grafica,'ro')
	plt.axhline(0,color="red")
	plt.axvline(0,color="red")
	plt.axis([-n-2,n+2,n_min-2,n_max+2])
	plt.grid(True)
	plt.title(titulo)
	plt.show()

#Funcion que muestra en pantalla la secuencia
#Recibe como parámetro la secuencia, su nombre, el indice de inicio n(0) y la bandera que indica si es periódica o no
def muestra_serie(s,nom,indice,periodica):
	#Si la secuencia es periodica se mostrará repetidamente
	if(periodica == True):
		s = s*5
		indice *= 3
		str_s = nom +" = { ... "
		for i in range(len(s)):
			str_s = str_s + ", " + str(s[i])
		str_s = str_s + " }      n(0) = "
	else:
		str_s = nom +" = { "
		for i in range(len(s)):
			if(i == 0):
				str_s = str_s + str(s[i])
			else:
				str_s = str_s + ", " + str(s[i])
		str_s = str_s + " }      n(0) = "

	print(str_s + str(s[indice]))

	graficar_ = input("Quieres mostrar la grafica? (s/n) : ")
	graficar_.lower()

	if (graficar_ == "s"):
		graficar(s,indice,nom)

def obtencionIndice0(serie):
	ini = input("¿Cuál es el elemento de inicio?: ")
	try:
		ini = float(ini)
	except :
		ini = int(ini)

	if ini in serie and serie.count(ini) == 1 :
		print("se encontro indice en = " +str(serie.index(ini)))
		return serie.index(ini)
	elif ini in serie and serie.count(ini) > 1 :
		repetidos = []
		for index,element in enumerate(serie):
			if element == ini:
				repetidos.append(index+1)
		print("El numero " + str(ini) +" se encuentra repetido varias veces en las posiciones " +", ".join(str(v) for v in repetidos))
		return int(input("Por favor elige que posicion es la adecuada: "))-1

#Funcion que hace el algoritmo de convolución periódica
def conv_periodica():
	clearScreen()
	print("\tCONVOLUCIÓN PERIÓDICA\nINSTRUCCIONES\n1.Considera a x(n) como la funcion periodica y no repita elementos (se entiende que los elementos que ingrese van a repetir infinitamente) \n2.Ingresa un elemento a la vez\n")
	input("\nPresiona enter para continuar...")
	clearScreen()

	#Se ingresa la secuencia x(n)
	x = ingresa_serie("x(n)")
	x_ini = obtencionIndice0(x)

	clearScreen()

	#Se ingresa la secuencia h(n)
	h = ingresa_serie("h(n)")
	h_ini = obtencionIndice0(h)
	clearScreen()

	#Se muestran las secuencias ingresadas
	muestra_serie(x,"x(n)",x_ini,True)
	muestra_serie(h,"h(n)",h_ini,False)

	#ALGORITMO CONVOLUCIÓN PERIÓDICA:

	renglones = []

	#Se obtiene la secuencia de mayor tamaño
	sec_mayor = x
	sec_menor = h
	if(len(h) > len(x)):
		sec_mayor = h
		sec_menor = x

	renglones = []
	#Multiplicacion Invertida
	for i in range(len(sec_menor)):
		rengaux = []
		for j in range(len(sec_mayor)):
			rengaux.append(sec_mayor[j]*sec_menor[i])
		renglones.append(rengaux)

	#Suma de renglones:
	for i in range (len(sec_menor)-1):
		if(i == 0):
			for j in range (len(sec_menor)-1):
				renglones[i].append(0)
				renglones[len(sec_menor)-1].insert(0,0)
		else:
			for j in range (i):
				renglones[i].insert(0,0)
				renglones[len(sec_menor)-1-i].append(0)

	sum_resul = []
	for i in range (len(renglones[0])):
		suma = 0
		for j in range (len(sec_menor)):
			suma = suma + renglones[j][i]
		sum_resul.insert(i,suma)

	#Se separa la secuencia en bloques de tamaño del periodo
	secuencia_bloques = []

	periodo = len(x)
	for i in range(len(sum_resul)//periodo):
		secuencia_bloques.append(sum_resul[periodo*i:periodo*(i+1)])

	#Suma de la secuencia en bloques para obtener la secuencia final
	y = []
	for i in range(len(secuencia_bloques[0])):
		suma = 0
		for j in range (len(secuencia_bloques)):
			suma = suma + secuencia_bloques[j][i]
		y.insert(i,suma)

	#Se obtiene el indice de inicio de la secuencia
	y_ini = ((x_ini*-1)+(h_ini*-1))*-1
	indice = 0
	for i in range(y_ini):
		if(indice == periodo-1):
			indice = 0
		else:
			indice += 1

	y_ini = indice

	print("y_ini ="+str(y_ini))

	muestra_serie(y,"y(n)",y_ini,True)
	input("\nPresiona enter para continuar...")

#Funcion que hace el algoritmo de convolución circular
def conv_circular():
	clearScreen()
	print("\tCONVOLUCIÓN CIRCULAR\nINSTRUCCIONES\n1.Considera a x(n) y h(n) como funciones periodicas y no repita elementos (se entiende que los elementos que ingrese van a repetir infinitamente) \n2.Ingresa un elemento a la vez\n")
	input("\nPresiona enter para continuar...")
	clearScreen()

	#Se ingresa la secuencia x(n)
	x = ingresa_serie("x(n)")
	x_ini = obtencionIndice0(x)
	clearScreen()

	#Se ingresa la secuencia h(n)
	h = ingresa_serie("h(n)")
	h_ini = obtencionIndice0(h)
	clearScreen()

	#Se muestran las secuencias ingresadas
	muestra_serie(x,"x(n)",x_ini,True)
	muestra_serie(h,"h(n)",h_ini,True)

	#ALGORITMO CONVOLUCIÓN CIRCULAR:

	#Se obtiene el mayor de los periodos
	sec_mayor = x
	sec_menor = h
	periodo = len(x)
	if(len(h) > periodo):
		periodo = len(h)
		sec_mayor = h
		sec_menor = x

	renglones = []
	#Multiplicacion Invertida
	for i in range(len(sec_menor)):
		rengaux = []
		for j in range(len(sec_mayor)):
			rengaux.append(sec_mayor[j]*sec_menor[i])
		renglones.append(rengaux)

	#Suma de renglones:
	for i in range (len(sec_menor)-1):
		if(i == 0):
			for j in range (len(sec_menor)-1):
				renglones[i].append(0)
				renglones[len(sec_menor)-1].insert(0,0)
		else:
			for j in range (i):
				renglones[i].insert(0,0)
				renglones[len(sec_menor)-1-i].append(0)

	sum_resul = []
	for i in range (len(renglones[0])):
		suma = 0
		for j in range (len(sec_menor)):
			suma = suma + renglones[j][i]
		sum_resul.insert(i,suma)

	#Se rellena la secuencia con ceros para poder separarla
	while(len(sum_resul)%periodo != 0):
		sum_resul.append(0)

	#Se separa la secuencia en bloques de tamaño del periodo
	secuencia_bloques = []

	for i in range(len(sum_resul)//periodo):
		secuencia_bloques.append(sum_resul[periodo*i:periodo*(i+1)])

	#Suma de la secuencia en bloques para obtener la secuencia final
	y = []
	for i in range(len(secuencia_bloques[0])):
		suma = 0
		for j in range (len(secuencia_bloques)):
			suma = suma + secuencia_bloques[j][i]
		y.insert(i,suma)

	#Se obtiene el indice de inicio de la secuencia
	y_ini = ((x_ini*-1)+(h_ini*-1))*-1
	indice = 0
	for i in range(y_ini):
		if(indice == periodo-1):
			indice = 0
		else:
			indice += 1

	y_ini = indice
	print("y_ini ="+str(y_ini))


	muestra_serie(y,"y(n)",y_ini,True)
	input("\nPresiona enter para continuar...")

def conv_finita():
	clearScreen()
	print("\tCONVOLUCIÓN FINITA\nINSTRUCCIONES\n1.Considera a x(n) y h(n) como funciones no periodicas \n2.Ingresa un elemento a la vez\n")
	input("\nPresiona enter para continuar...")
	clearScreen()

	#Se ingresa la secuencia x(n)
	x = ingresa_serie("x(n)")
	x_ini = obtencionIndice0(x)
	clearScreen()

	#Se ingresa la secuencia h(n)
	h = ingresa_serie("h(n)")
	h_ini = obtencionIndice0(h)
	clearScreen()

	#Se muestran las secuencias ingresadas
	muestra_serie(x,"x(n)",x_ini,False)
	muestra_serie(h,"h(n)",h_ini,False)

	n = len(x) + len(h) - 1

	cx = [[0 for i in range(n)] for i in range(n)]
	aux = [0 for i in range(n - len(x))]
	aux_x = x + aux
	for i in range(n):
		for j in range(n):
			cx[j][i] = aux_x[j]
		last_item = aux_x[-1]
		aux_x = aux_x[:len(aux_x)-1]
		aux_x.insert(0,last_item)

	aux = [0 for i in range(n - len(h))]
	aux_h = h + aux

	y=[]
	aux_suma=0
	for j in range(n):
		for k in range(n):
			aux_suma += cx[j][k] * aux_h[k]
		y.append(aux_suma)
		aux_suma = 0

	y_ini = ((x_ini*-1)+(h_ini*-1))*-1

	print("y_ini ="+str(y_ini))

	muestra_serie(y,"y(n)",y_ini,False)


clearScreen()


op = 0
while(op != 4):
	try:
		op = int(input("\tCONVOLUCIÓN DISCRETA\n\nSi y(n) = x(n)*y(n)\n\n1.Convolución Finita\n2.Convolución Periodica\n3.Convolución Circular\n4.Salir\nOpcion:"))
	except:
		op = 4
	if( op == 1):
		conv_finita()
	if( op == 2):
		conv_periodica()
	if( op == 3):
		conv_circular()

	clearScreen()
