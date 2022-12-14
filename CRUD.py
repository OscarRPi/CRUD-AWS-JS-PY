'''
Esta aplicacion recorre las funcionalidades basicas de un CRUD mediante una interfaz sencilla en consola
'''

#------> Aplicación CRUD - Biblioteca

from time import sleep
from os import system

import requests
import json

url = "https://d4m2qw0ss3.execute-api.us-east-1.amazonaws.com/items"

# funciones

# Esta funcion se usa para agregar un nuevo registro a la base de datos.
# Se organizan los datos en formato json y luego se hace una peticion put para agregar los datos

def create(libroNuevo): 

    data_json = json.dumps(libroNuevo)

    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    response = requests.put(url, data=data_json, headers=headers)

    print(" ")
    print(response.json())
    print(" ")

# Esta funcion se usa para leer todos los registros en la base de datos
# Se reciben los datos en formato json haciendo una peticion get

def read_all():

    response = requests.get(url)
    json_data = json.loads(response.text)
    libros = json_data.get('Items')

    print("{:<10} {:<25} {:<25} {:<25}".format('ID', 'TITLE', 'AUTHOR', 'EDITORIAL'))
    print(" ")

    ids = []

    for i in range(len(libros)):
        ids.append(int(libros[i]['id']))

    ids.sort()

    for j in range(len(libros)):
        for i in range(len(libros)):
            if (int(libros[i]['id']) == ids[j]):
                print("{:<10} {:<25} {:<25} {:<25}".format(libros[i]['id'],libros[i]['title'], libros[i]['autor'],libros[i]['editorial']))

# Esta funcion se usa para leer solo un registro en la base de datos
# Se reciben los datos en formato json haciendo una peticion get

def read(identificador):

    response = requests.get(url+"/"+str(identificador))
    json_data = json.loads(response.text)
    libro = list(json_data.values())

    if libro == []:
        print(" ")
        print("No se encontro el libro")
        print(" ")
    else:
        print("{:<10} {:<25} {:<25} {:<25}".format('ID', 'TITLE', 'AUTHOR', 'EDITORIAL'))
        print(" ")
        print("{:<10} {:<25} {:<25} {:<25}".format(libro[0]['id'],libro[0]['title'], libro[0]['autor'],libro[0]['editorial']))

# Esta funcion se usa para eliminar un registro de la base de datos
# Se envia el identificador de la fila y se elimina este registro haciendo una peticion delete

def delete(identificador):

    response = requests.delete(url+"/"+str(identificador))
    print(" ")
    print(response.json())
    print(" ")

# Esta funcion se usa para determinar si un identificador se encuentra en la base de datos
# Se lee la base de datos y se agrupan los ids recibidosen una lista. Si el identificador coincide con alguno de los ids
# entonces se devuelve True, de lo contrario se devuelve False

def iselement(identificador):
    
    response = requests.get(url)
    json_data = json.loads(response.text)
    libros = json_data.get('Items')

    ids = []

    for i in range(len(libros)):
        ids.append(int(libros[i]['id']))
      
    if identificador in ids:
        return True
    else:
        return False
    
# Esta funcion es la encargada de mostrar el menu principal al usuario
# El usuario puede escoger entre 6 opciones para Crear/Actualizar/Leer todo/Leer un solo registro/Eliminar o salir

# El id debe ser un numero entero
# El titulo es de tipo string
# El autor es de tipo string
# La editorial es de tipo string

def loop():

    loop = True

    while loop: 
        
        print(" ")
        print("-- Aplicación CRUD Biblioteca ---")
        print(" ")
        print("1. Agregar libro")
        print("2. Consultar todos los libros")
        print("3. Consultar un libro")
        print("4. Actualizar libro")
        print("5. Eliminar libro")
        print("6. Salir")
        print(" ")

        opcion = int(input("Ingrese una opción: "))
        
        #Create
        if opcion == 1:
            print()
            print("->Agregando libro")        
            
            try:
                identificador = int(input("Ingrese id: "))
            except:
                print()
                print("El identificador debe ser un numero")
                print()
                sleep(2)
                system('cls')
                continue

            if iselement(identificador):
                print("El id ya se encuentra registrado")
                sleep(2)
                system('cls')
                continue

            titulo = str(input("Ingrese titulo: "))
            autor = str(input("Ingrese autor: "))
            editorial = str(input("Ingrese editorial: "))       
            
            libroNuevo = {
                            'id'			: str(identificador),
                            'title' 		: titulo,
                            'autor' 		: autor,
                            'editorial' 	: editorial       
                        }

            create(libroNuevo)
            
        #Read all
        elif opcion == 2:
            print()
            print("->Listado de todos los libros")
            print()

            read_all()               

        #Read once
        elif opcion == 3:
            print()
            print("->Consultar informacion de un libro")
            print()

            try:
                identificador = int(input("Ingrese identificador del libro: "))
            except:
                print()
                print("El identificador debe ser un numero")
                print()
                sleep(2)
                system('cls')
                continue

            read(identificador) 

        #Update
        elif opcion == 4:

            print()
            print("->Actualizar Libro")
            print()
            
            try:
                identificador = int(input("Ingrese identificador del libro a modificar: "))
            except:
                print()
                print("El identificador debe ser un numero")
                print()
                sleep(2)
                system('cls')
                continue
                 
            if iselement(identificador):
                
                flag_update = 0

                #Modificar los campos de interés
                nuevoTitulo = str(input('Nuevo titulo: '))
                if nuevoTitulo:
                    flag_update +=1

                nuevoAutor = str(input('Nuevo autor: '))
                if nuevoAutor:
                    flag_update +=1

                nuevaEditorial = input('Nueva editorial: ')
                if nuevaEditorial: 
                    flag_update +=1

                if flag_update == 3:

                    libroActualizado = {
                            'id'            : str(identificador),
                            'title'         : nuevoTitulo,
                            'autor'         : nuevoAutor,
                            'editorial'     : nuevaEditorial       
                    }

                    create(libroActualizado)

                else:
                    print("Introduzca todos los campos por favor")

            else:
                print("No ha sido encontrado el libro")     
               
        #Delete
        elif opcion == 5:

            print()
            print("->Eliminar libro")
            print()
            
            try:
                identificador = int(input("Ingrese identificador del libro a eliminar: "))
            except:
                print()
                print("El identificador debe ser un numero")
                print()
                sleep(2)
                system('cls')
                continue
      
            if iselement(identificador):
                         
                delete(identificador)    
                
            else:
                print("No ha sido encontrada el libro a eliminar")
            
        #Exit    
        elif opcion == 6:
            print("Ha salido exitosamente.")
            loop = False
            sleep(1)

        else:
            print("Seleccion invalida")

        if (loop == True):
            tiempo = 5
            for i in range(tiempo):
                print(" ")
                print("Volviendo al menu principal en ", tiempo-i, "segundos...")
                sleep(1)

        system('cls')

loop()