"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import time
from typing import Mapping
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
#RECORDAR asmpm ((energy-danceability), (tempo-instrumentalness), (liveness-valence), (acousticness-speechness))

# Construccion de modelos
def initCat():
    catalog={'events':None, 'uni_artists':None, 'uni_tracks':None}
    catalog['events']=lt.newList('SINGLE_LINKED')
    catalog['uni_artists']={}
    catalog['uni_tracks']=mp.newMap(maptype='PROBING')
    catalog['sup_inf']={'liveness':'valence', 'acousticness':'speechiness', 'tempo':'instrumentalness', 'energy':'danceability'}
    catalog['inf_sup']={'valence':'liveness', 'speechiness':'acousticness', 'instrumentalness':'tempo', 'danceability':'energy'}
    catalog['hashtag_vader']=mp.newMap(maptype='PROBING')
    catalog['time_stamps']=om.newMap()
    return catalog


# Funciones para agregar informacion al catalogo
def addEvent(catalog, event):
    ccs=['energy', 'tempo', 'liveness', 'acousticness']
    lt.addFirst(catalog['events'], event)
    artist=event['artist_id']
    track=event['track_id']
    
    if mp.contains(catalog['uni_tracks'], track)==False:
        a={'tempo': event['tempo'], 'hashtags': lt.newList(), 't_vader':0}
        mp.put(catalog['uni_tracks'], track, a)

    catalog['uni_artists'][artist]=1

    y=0

    while y<len(ccs):
        main=ccs[y]
        main_val=event[main]
        mini=catalog['sup_inf'][main]
        mini_val=event[mini]
        
        if not main in catalog:
            catalog[main]=om.newMap()
        
        if (om.contains(catalog[main], main_val))==False:
            om.put(catalog[main], main_val, om.newMap())

        a=om.get(catalog[main], main_val)
        a=me.getValue(a)
        if (om.contains(a, mini_val))==False:
            a=om.get(catalog[main], main_val)
            a=me.getValue(a)
            om.put(a, mini_val, lt.newList())

        alpha=om.get(catalog[main], main_val)
        alpha=me.getValue(alpha)
        alpha=om.get(alpha, mini_val)
        alpha=me.getValue(alpha)
        lt.addFirst(alpha, event)

        y+=1
    
def addSentiment(catalog, pair):
    mp.put(catalog['hashtag_vader'], pair['hashtag'], pair['vader_avg'])

def addRegister(catalog, register):
    t=time.strptime(register['created_at'], '%Y-%m-%d %H:%M:%S' )
    tid=register['track_id']
    htag=register['hashtag']

    hh=t.tm_hour
    mm=t.tm_min
    ss=t.tm_sec

    if (om.contains(catalog['time_stamps'], hh))==False:
        om.put(catalog['time_stamps'], hh, om.newMap())

    hm=om.get(catalog['time_stamps'], hh)
    hm=me.getValue(hm)
    if (om.contains(hm, mm))==False:
        om.put(hm, mm, om.newMap())
    
    minmap=om.get(hm, mm)
    minmap=me.getValue(minmap)
    if (om.contains(minmap, ss))==False:
        om.put(minmap, ss, lt.newList())
    
    sm=om.get(minmap, ss)
    main=me.getValue(sm)
    lt.addFirst(main, tid)

    sub=mp.get(catalog['uni_tracks'], tid)
    if sub!=None:
        mini=me.getValue(sub)

        if lt.isPresent(mini['hashtags'], htag)==0 and mp.get(catalog['hashtag_vader'], htag)!=None :
            vader=mp.get(catalog['hashtag_vader'], htag)
            vader=me.getValue(vader)
            if vader!= '':
                lt.addFirst(mini['hashtags'], htag)
                mini['t_vader']+=float(vader)
    
# Funciones para creacion de datos


# Funciones de consulta
def reque1_SUP(main, m, M):
    if (float(om.minKey(main)))>m: m==(float(om.minKey(main)))
    if (float(om.maxKey(main)))<M: M==(float(om.maxKey(main)))
    nums=get_inter(om.keySet(main), m, M)
    dans=count_intervalSUP(main, nums)
    k=len(dans['id_list'].keys())
    ans={'t_eve':dans['events'], 't_art': k}
    return ans

def reque1_INF(main, m, M):
    dans=count_intervalINF(main, m , M)
    k=len(dans['id_list'].keys())
    ans={'t_eve':dans['events'], 't_art': k}
    return ans

def reque2(main, e, E, d, D):
    if float(om.minKey(main))>e: e==float(om.minKey(main))
    if float(om.maxKey(main))<E: E==float(om.maxKey(main))
    nums=get_inter(om.keySet(main), e, E)

    ans={'idlist':{}, 'for_show':lt.newList('SINGLE_LINKED')}
    y=1
    while y<=lt.size(nums):
        num=lt.getElement(nums, y)
        pair=om.get(main, num)
        mini=me.getValue(pair)
        
        if float(om.minKey(mini))>d: d==float(om.minKey(mini))
        if float(om.maxKey(mini))<D: D==float(om.maxKey(mini))
        sub_nums=get_inter(om.keySet(mini), d, D)
        x=1
        while x<=lt.size(sub_nums):
            sub_num=lt.getElement(sub_nums, x)
            sub_pair=om.get(mini, sub_num)
            events=me.getValue(sub_pair)

            z=1
            while z<=lt.size(events):
                e=lt.getElement(events, z)
                id=e['track_id']
                lt.addFirst(ans['for_show'], e)
                ans['idlist'][id]=1
                
                z+=1
            x+=1
        y+=1
    return ans
    

# Funciones utilizadas para comparar elementos dentro de una lista


# Funciones de ordenamiento
def get_inter(lista, m, M):
    y=1
    a=lt.newList('ARRAY_LIST')

    while y<=lt.size(lista):
        e=lt.getElement(lista, y)
        if m<=float(e)<=M: lt.addFirst(a, e)

        y+=1
    return a

def count_intervalSUP(main, nums):
    ans={'events':0, 'idlist':{}}
    y=1

    while y<=lt.size(nums):
        num=lt.getElement(nums, y)
        pair=om.get(main, num)
        mini=me.getValue(pair)
        
        sub_nums=om.keySet(mini)
        x=1
        while x<=lt.size(sub_nums):
            sub_num=lt.getElement(sub_nums, x)
            sub_pair=om.get(mini, sub_num)
            events=me.getValue(sub_pair)

            z=1
            while z<=lt.size(events):
                e=lt.getElement(events, z)
                ans['events']+=1
                id=e['artist_id']

                ans['idlist'][id]=1
                
                z+=1
            x+=1
        y+=1
    return ans

def count_intervalINF(main, m, M):
    ans={'events':0, 'idlist':lt.newList('SINGLE_LINKED')}
    y=1
    nums=om.keySet(main)

    while y<=lt.size(nums):
        num=lt.getElement(nums, y)
        pair=om.get(main, num)
        mini=me.getValue(pair)

        if float(om.minKey(mini))>m: m==float(om.minKey(mini))
        if float(om.maxKey(mini))<M: M==float(om.maxKey(mini))
        sub_nums=get_inter(om.keySet(mini), m, M)

        x=1
        while x<=lt.size(sub_nums):
            sub_num=lt.getElement(sub_nums, x)
            sub_pair=om.get(mini, sub_num)
            events=me.getValue(sub_pair)

            z=1
            while z<=lt.size(events):
                e=lt.getElement(events, z)
                id=e['artist_id']
                ans['events']+=1
                ans['idlist'][id]=1
                
                z+=1
            x+=1
        y+=1
    return ans