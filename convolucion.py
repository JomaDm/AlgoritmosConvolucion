#INSTITUTO POLITÉCNICO NACIONAL - ESCUELA SUPERIOR DE CÓMPUTO
#Bonilla Reyes José Luis
#Domínguez Morales José Manuel

import os
from sys import platform

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
		s.append(int(input(( nom +" = " + str(s) + ": "))))
	clearScreen()
	print(nom + " = " + str(s))
	return s

#Funcion que muestra en pantalla la secuencia
#Recibe como parámetro la secuencia, su nombre, el indice de inicio n(0) y la bandera que indica si es periódica o no
def muestra_serie(s,nom,indice,periodica):
	#Si la secuencia es periodica se mostrará repetidamente
	if(periodica == True):
		str_s = nom +" = { ... "
		for i in range(len(s)):
			str_s = str_s + ", " + str(s[i])
		for i in range(len(s)):
			str_s = str_s + ", " + str(s[i])
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

#Funcion que hace el algoritmo de convolución periódica
def conv_periodica():
	clearScreen()
	print("\tCONVOLUCIÓN PERIÓDICA\nINSTRUCCIONES\n1.Considera a x(n) como la funcion periodica y no repita elementos (se entiende que los elementos que ingrese van a repetir infinitamente) \n2.Ingresa un elemento a la vez\n")
	input("\nPresiona enter para continuar...")
	clearScreen()

	#Se ingresa la secuencia x(n)
	x = ingresa_serie("x(n)")
	x_ini = input("¿Cuál es el elemento de inicio?")
	x_ini = x.index(x_ini)
	clearScreen()

	#Se ingresa la secuencia h(n)
	h = ingresa_serie("h(n)")
	h_ini = input("¿Cuál es el elemento de inicio?")
	h_ini = h.index(h_ini)
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

	muestra_serie(y,"y(n)",y_ini,True)
	input("\nPresiona enter para continuar...")

#Funcion que hace el algoritmo de convolución periódica
def conv_circular():
	clearScreen()
	print("\tCONVOLUCIÓN CIRCULAR\nINSTRUCCIONES\n1.Considera a x(n) y h(n) como funciones periodicas y no repita elementos (se entiende que los elementos que ingrese van a repetir infinitamente) \n2.Ingresa un elemento a la vez\n")
	input("\nPresiona enter para continuar...")
	clearScreen()

	#Se ingresa la secuencia x(n)
	x = ingresa_serie("x(n)")
	x_ini = input("¿Cuál es el elemento de inicio?")
	x_ini = x.index(x_ini)
	clearScreen()

	#Se ingresa la secuencia h(n)
	h = ingresa_serie("h(n)")
	h_ini = input("¿Cuál es el elemento de inicio?")
	h_ini = h.index(h_ini)
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


	muestra_serie(y,"y(n)",y_ini,True)
	input("\nPresiona enter para continuar...")

def conv_finita():


clearScreen()
op = 0
while(op != 5):
	op = int(input("\tCONVOLUCIÓN DISCRETA\n\nSi y(n) = x(n)*y(n)\n\n1.Convolución Finita\n2.Convolución Periodica\n3.Convolución Circular\n4.Gráficas de Entrada/Salida\n5.Salir\nOpcion:"))
	if( op == 1):
		print("CONVOLUCIÓN Finita")
	if( op == 2):
		conv_periodica()
	if( op == 3):
		conv_circular()
	if( op == 4):
		print("GRÁFICAS")
	clearScreen()
