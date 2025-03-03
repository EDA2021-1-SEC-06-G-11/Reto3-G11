﻿"""
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
import time
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
default_limit = 10000
sys.setrecursionlimit(default_limit*10) 

linea=('==========================================================================================')
"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

dic_genres = {'Jazz and Funk':{'minimo':120,'maximo':125},
                'R&B':{'minimo':60,'maximo':80},
                'Metal':{'minimo':100,'maximo':160},
                'Rock':{'minimo':110,'maximo':140},
                'Pop':{'minimo':100,'maximo':130},
                'Chill-out':{'minimo':90,'maximo':120},
                'Hip-hop':{'minimo':85,'maximo':115},
                'Down-tempo':{'minimo':70,'maximo':100},
                'Reggae':{'minimo':60,'maximo': 90},}

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

def printResultsR4(ans,lista):
    print('++++++ Req No. 4 results ++++++')
    t = mp.get(ans,'total')
    to = me.getValue(t)
    print('Total of reproductions: ',to)
    for i in lista:
        n = mp.get(ans,i)
        events = me.getValue(n)['events']
        artists = me.getValue(n)['artists']
        minimo = me.getValue(n)['minimo']
        maximo = me.getValue(n)['maximo']
        lstartists = me.getValue(n)['lstartists']
        print('======== ',i,' ========')
        print('For ',i,' the tempo is between ',minimo,' and ',maximo,' BPM')
        print(i,' reproductions: ',events,' with ', artists, ' different artists')
        print('----- Some artists for ',i,' -----')
        print('Artist 1: ',lstartists[1])
        print('Artist 2: ',lstartists[2])
        print('Artist 3: ',lstartists[3])
        print('Artist 4: ',lstartists[4])
        print('Artist 5: ',lstartists[5])
        print('Artist 6: ',lstartists[6])
        print('Artist 7: ',lstartists[7])
        print('Artist 8: ',lstartists[8])
        print('Artist 9: ',lstartists[9])
        print('Artist 10: ',lstartists[10])

def printResultsR5(dic,min_t,max_t):
    total = 0
    mayor = 0
    genre = ''
    dic_genre = None
    for i in dic:
        total += dic[i]['reps']
        if dic[i]['reps'] > mayor:
            mayor = dic[i]['reps']
            dic_genre = dic[i]
            genre = i


    print('++++++ Req No. 5 results... ++++++')
    print('There is a total of ',total,' reproductions between ',min_t,' and ',max_t)
    print('====================== GENRES SORTED REPRODUCTIONS ======================')
    for m in range(0,9):
        mayor1 = 0
        lol = ''
        for j in dic:
            if dic[j]['reps'] > mayor1:
                mayor1 = dic[j]['reps']
                lol = j
        x = dic.pop(lol)
        print('Top',(m+1),': ',lol,' with',mayor1,' reps')
    print('...')
    print('')
    print('The TOP GENRE is ',genre,' with ',dic_genre['reps'],' reproductions...')
    print('')
    print('========================== ',genre,' SENTIMENT ANALYSIS ==========================')
    print(genre, 'has ',dic_genre['unique'],' unique tracks...')
    print('The first TOP 10 tracks are...')
    print('')
    for k in range(0,10):
        mayor2 = 0
        lol1 = ''
        for tracks in dic_genre['tracks']:
            if dic_genre['tracks'][tracks]['hashtag'] >= mayor2:
                mayor2 = dic_genre['tracks'][tracks]['hashtag']
                vader = dic_genre['tracks'][tracks]['vader']
                lol1 = tracks
        y = dic_genre['tracks'].pop(lol1)
        print('TOP ',(k+1),'track: ',lol1,' with ',mayor2,' hashtag and VADER = ',vader)

        


        




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
        print('Se encontraron {0} eventos, {1} artistas y {2} pistas únicas'.format(lt.size(catalog['events']), len(catalog['uni_artists'].keys()), lt.size(mp.keySet(catalog['uni_tracks']))))

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


        respuesta = input('Desea agregar un nuevo genero? ')
        
        if respuesta == 'si':
            name = input('Escriba el nombre del nuevo genero: ')
            vminimo = input('Escriba el valor minimo del Tempo: ')
            vmaximo = input('Escriba el valor maximo del Tempo: ')
            dic_genres[name] = {'minimo':vminimo,'maximo':vmaximo}
        
        lista = input('Escriba una lista con los generos que desea buscar separados por ", ": ')
        lista = lista.split(', ')
        ans = controller.reque4(catalog,dic_genres,lista)
        printResultsR4(ans,lista)
        
        
    elif int(inputs[0]) == 6:
        print('Por favor escribir las horas en formato 24h y "hh:mm:ss"')
        min_time = input('Escriba la hora minima: ')
        max_time = input('Escriba la hora maxima: ')
        min_t = time.strptime(min_time,'%H:%M:%S')
        max_t = time.strptime(max_time,'%H:%M:%S')
        ans = controller.reque5(catalog, dic_genres,min_t,max_t)
        printResultsR5(ans,min_time,max_time)

 
    

    else:
        sys.exit(0)
sys.exit(0)

