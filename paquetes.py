import pandas as pd
import numpy as np

t1=pd.read_excel('./data/lista_lima.xlsx') #Input variable
campos_t1=['CODIGO UNICO','NOMBRE_EBC','DELTA RTWP (dB) > 2 dB', '# drops 4g','SECTOR']
t2=pd.read_excel('./data/codigounico-sector.xlsx',sheet_name='Base') #input fijo
campos_t2=['Codigo Unico','Zona']
t1=t1[campos_t1]
t2=t2[campos_t2]

data=pd.merge(t1,t2,left_on=campos_t1[0],right_on=campos_t2[0],how='inner')

grupo=data['Zona'].unique()


def evaluar(x, columnas, codunico):
    newdata=pd.DataFrame()
    tenfirst = x.sort_values(by=columnas, ascending=False).head(100)
    registros=tenfirst[codunico].unique()
    for ss,cod in enumerate(registros):
        row ={'codunico':cod,'detalle':'*PROACTIVO CALIDAD MOVIL |'}
        unirdup=tenfirst[tenfirst[codunico]==cod]
        for index, unir in unirdup.iterrows():
            row['detalle']+='*'
            row["detalle"]+='- Delta RTWP: {}'.format(unir['DELTA RTWP (dB) > 2 dB'])
            row["detalle"]+='- Drops 4g: {}'.format(unir['# drops 4g'])
            row["detalle"]+='- Sector: {}'.format(unir['SECTOR'])
        row["detalle"]=[row['detalle']]
        temp=pd.DataFrame(row,index=[ss])
        newdata=pd.concat([newdata,temp],sort=False)
    return newdata.head(10)   
           
filtroarbol=pd.DataFrame()
for registro in grupo:
    datazona=data[data['Zona']==registro]
    datazona=evaluar(datazona,columnas=['DELTA RTWP (dB) > 2 dB', '# drops 4g'],codunico='CODIGO UNICO')
    datazona['zona']=registro
    filtroarbol=pd.concat([filtroarbol,datazona])

filtroarbol['ESPECIALIDAD']='RADIO-RADIO'
filtroarbol['ACCIONES']='EN SITIO REVISAR Y CORRECCION DE PROBLEMA REPORTADO POR CALIDAD MOVIL'
filtroarbol.to_excel("prueba.xlsx",sheet_name='movil_prioridad_zona',index=False)


