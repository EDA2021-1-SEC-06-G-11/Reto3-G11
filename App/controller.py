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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initcat():
    return model.initCat()

# Funciones para la carga de datos
def loadData(catalog):
    Dfile = cf.data_dir + 'context_content_features-small.csv'
    main_file = csv.DictReader(open(Dfile, encoding='utf-8'))

    for event in main_file:
        model.addEvent(catalog, event)

    HVfile = cf.data_dir + 'sentiment_values.csv'
    sv_file = csv.DictReader(open(HVfile, encoding='utf-8'))

    for pair in sv_file:
        model.addSentiment(catalog, pair)
    
    TSfile = cf.data_dir + 'user_track_hashtag_timestamp-small.csv'
    ts_sub= csv.DictReader(open(TSfile, encoding='utf-8'))

    for register in ts_sub:
        model.addRegister(catalog, register)

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def reque1(catalog, cc, m, M):
    a=cc.lower().strip()
    if a in catalog['sup_inf']:
        main=catalog[a]
        ans=model.reque1_SUP(main, m, M)
        return ans
    
    else:
        cc=catalog['inf_sup'][cc]
        main=catalog[cc]
        ans=model.reque1_INF(main, m, M)
        return ans


def reque2(catalog, e, E, d, D):
    main=catalog['energy']
    ans=model.reque2(main, e, E, d, D)
    return ans

def reque3(catalog, e, E, d, D):
    main=catalog['tempo']
    ans=model.reque2(main, e, E, d, D)
    return ans

def reque4(catalog,new_genres, lista):
    main = catalog['tempo_req4']
    dic = {}
    for i in lista:
        dic[i] = new_genres[i]
    ans = model.req4(main,dic)
    return ans

def reque5(catalog, new_genres,h,m,s,H,M,S):
    mainh = catalog['time_stamps']
    mainhash = catalog['hashtag_vader']
    ans = model.req5(mainh,mainhash,new_genres,h,m,s,H,M,S)

    return ans

