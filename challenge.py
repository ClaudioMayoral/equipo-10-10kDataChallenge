# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 16:45:08 2022

@author: jose_
"""

from pandas import DataFrame
from pandas import read_csv

# Leer base de datos acuíferos
data = read_csv("UnionRegiosDOFShape.csv")

# Separa las variables de la base de datos
variables = data.columns

# Guarda los municipios registrados en la base de datos
municipios_1 = data.iloc[:,20]

# Obtén el número de municipios y el municipio con mayor coincidencia
num_municipios = municipios_1.describe()

# Guarda todos los municipios que tienen un acuifero en una lista
municipios = []

for municipio in data.iloc[:,20]:
    if municipio not in municipios:
        municipios.append(municipio)

# Ordena la lista
municipios.sort()

# Obtén el número de acuíferos por municipio
acu_per_mun = data.iloc[:,20].value_counts()

# Convierte en un diccionario acu_per_num
acu_per_num_dict = acu_per_mun.to_dict()

# Datos de interés
new_data = data.iloc[:,[2,4,8,10,16,19,20,23,24,25,26,27,28,29,31,37,38,39,40]]
new_data = new_data.drop(columns=['CLAVE DE MUNICIPIO','ACUIFERO QUE MENCIONA EL TITULO',
                                  'VOLUMEN DE EXTRACCIÓN ANUAL DE APROVECHAMIENTOS SUBTERRÁNEOS EN m3',
                                  'GRADOS LATITUD','MINUTOS LATITUD','SEGUNDOS LATITUD',
                                  'GRADOS LONGITUD','MINUTOS LONGITUD','SEGUNDOS LONGITUD',
                                  'Recarga_total_media_anual','Descarga_natural_media_anual'])
# Nuevas variables
new_variables = new_data.columns

# Obtén los acuíferos
acuiferos = new_data.iloc[:,-1].value_counts()

# Filtrar por acuíferos públicos
new_data_filt = new_data[new_data['PubPrivEjid']=='PUBLICO']

# Contar el total de m3 por municipio disponibles
muns = new_data_filt.iloc[:,-4].to_list()
m3s = new_data_filt.iloc[:,-3].to_list()

mun_dict = {}

for mun, m3 in zip(muns,m3s):
    mun_dict[mun] = mun_dict.get(mun,0) + m3

# Abrir tabla de Viviendas Acceso al Agua 2020 NL
viviendas = read_csv('Vivienda_AccesoAgua_Municipio_2020_NL.csv')
viviendas_filt = viviendas.drop(columns=['% Entubada dentro de la vivienda',
                                         '% Entubada fuera de la vivienda'])       
viviendas_filt = viviendas_filt.drop([0])

# Actualizar diccionario con municipios que no tienen acuíferos públicos
for mun in municipios:
    mun_dict[mun] = mun_dict.get(mun,0)
    
# Filtrar por acuíferos públicos
pub_urb_filt = new_data[new_data['USO QUE AMPARA EL TITULO']=='PÚBLICO URBANO']

# Contar el total de m3 por municipio disponibles y de uso público
muns = pub_urb_filt.iloc[:,-4].to_list()
m3s = pub_urb_filt.iloc[:,-3].to_list()

mun_dict = {}

for mun, m3 in zip(muns,m3s):
    mun_dict[mun] = mun_dict.get(mun,0) + m3