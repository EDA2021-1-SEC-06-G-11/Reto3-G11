"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """
import random
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
assert cf

linea=('==========================================================================================')
"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
def p_rq1(ans, cc, m, M):
    print(linea)
    print('Resultados requerimiento 1:')
    print('Se encontraron {0} eventos, con un total de {1} artistas, para los requisitos de {2} entre {3} y {4}'
    .format(ans['t_eve'], ans['t_art'], cc, m, M))
    print(linea)

def p_rq2(ans, e, E, d, D):
    print(linea)
    print('Resultados requerimiento 2:')
    print('ENERGY entre {0} - {1} , DANCEABILITY entre {2} - {3}'. format(e, E, d, D))
    print('Se encontraton un total de {0} pistas unicas, entre las cuales están: '. format(lt.size(ans['idlist'])))

    y=1
    while y<=5:
        a=random.randint(0, lt.size(ans['for_show']))
        e=lt.getElement(ans['for_show'], a)
        
        print('Track {0} : {1} , ENERGY:{2} , DANCEABILITY: {3}'.format(y, e['track_id'], e['energy'], e['danceability']))
        y+=1

def p_rq3(ans, e, E, d, D):
    print(linea)
    print('Resultados requerimiento 2:')
    print('TEMPO entre {0} - {1} ,INSTRUMENTALNESS entre {2} - {3}'. format(e, E, d, D))
    print('Se encontraton un total de {0} pistas unicas, entre las cuales están: '. format(lt.size(ans['idlist'])))

    y=1
    while y<=5:
        a=random.randint(0, lt.size(ans['for_show']))
        e=lt.getElement(ans['for_show'], a)
        
        print('Track {0} : {1} , TEMPO:{2} , INSTRUMENTALNESS: {3}'.format(y, e['track_id'], e['tempo'], e['instrumentalness']))
        y+=1

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- (R1) Caracterizar las reproducciones")
    print("3- (R2) Encontrar musica para festejar")
    print("4- (R3) Encontrar musica para estudiar")
    print("5- (R4) Estudiar los géneros musicales")
    print("6- (R5) Indicar el género musical más escuchado en el tiempo")
    print("0- Salir")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog=controller.initcat()
        controller.loadData(catalog)
        print('Se encontraron {0} eventos, {1} artistas y {2} pistas únicas'.format(lt.size(catalog['events']), len(catalog['uni_artists'].keys()), len(catalog['uni_tracks'].keys())))

    elif int(inputs[0]) == 2:
        cc=str(input('Escriba la caracteristica de contenido que le interesa: '))
        v=float(input('Escriba el valor minimo de la caracteristica: '))
        V=float(input('Escriba el valor maximo de la caracteristica: '))
        ans=controller.reque1(catalog, cc, v, V)
        p_rq1(ans,cc, v, V)

    elif int(inputs[0]) == 3:
        e=float(input('Escriba el valor minimo de la caracteristica ENERGY: '))
        E=float(input('Escriba el valor maximo de la caracteristica ENERGY: '))
        d=float(input('Escriba el valor minimo de la caracteristica DANCEABILITY: '))
        D=float(input('Escriba el valor maximo de la caracteristica DANCEABILITY: '))
        ans=controller.reque2(catalog, e, E, d, D)
        p_rq2(ans, e, E, d, D)

    elif int(inputs[0]) == 3:
        e=float(input('Escriba el valor minimo de la caracteristica TEMPO: '))
        E=float(input('Escriba el valor maximo de la caracteristica TEMPO: '))
        d=float(input('Escriba el valor minimo de la caracteristica INSTRUMENTALNESS: '))
        D=float(input('Escriba el valor maximo de la caracteristica INSTRUMENTALNESS: '))
        ans=controller.reque3(catalog, e, E, d, D)
        p_rq3(ans, e, E, d, D)

    elif int(inputs[0])== 5:
        dic_genres = {'Reggae':{'minimo':60,'maximo': 90},
                    'Down-tempo':{'minimo':70,'maximo':100},
                    'Chill-out':{'minimo':90,'maximo':120},
                    'Hip-hop':{'minimo':85,'maximo':115},
                    'Jazz and Funk':{'minimo':120,'maximo':125},
                    'Pop':{'minimo':100,'maximo':130},
                    'R&B':{'minimo':60,'maximo':80},
                    'Rock':{'minimo':110,'maximo':140},
                    'Metal':{'minimo':100,'maximo':160},}

        respuesta = input('Desea agregar un nuevo genero? ')
        
        if respuesta == 'si':
            name = input('Escriba el nombre del nuevo genero: ')
            vminimo = input('Escriba el valor minimo del Tempo: ')
            vmaximo = input('Escriba el valor maximo del Tempo: ')
            dic_genres[name] = {'minimo':vminimo,'maximo':vmaximo}
        
        lista = input('Escriba una lista con los generos que desea buscar separados por ", ": ')
        lista = lista.split(', ')

        ans = controller.reque4(catalog,dic_genres,lista)
        print(catalog['tempo'])


    

    else:
        sys.exit(0)
sys.exit(0)
