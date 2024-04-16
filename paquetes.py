import pandas as pd
import numpy as np

t1=pd.read_excel('./data/lista_lima.xlsx') #Input variable
campos_t1=['CODIGO UNICO','NOMBRE_EBC','DELTA RTWP (dB) > 2 dB', '# drops 4g','SECTOR']
t2=pd.read_excel('./data/codigounico-sector.xlsx',sheet_name='Base') #input fijo
campos_t2=['Codigo Unico','Zona']
t1=t1[campos_t1]
t2=t2[campos_t2]

data=pd.merge(t1,t2,left_on=campos_t1[0],right_on=campos_t2[0],how='inner')

top_10_by_zone = data.groupby('Zona').apply(lambda x: x.nlargest(10, columns=['DELTA RTWP (dB) > 2 dB', '# drops 4g']))

top_10_by_zone.to_excel("prueba.xlsx")
