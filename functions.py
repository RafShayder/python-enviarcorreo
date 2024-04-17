import pandas as pd
def leerarchivo(ruta,campos,sheetname=None):
    if(sheetname==None):
        data=pd.read_excel(ruta)
    else:
        data=pd.read_excel(ruta,sheet_name=sheetname)
    data=data[campos]
    return data
def unirdataframe(data1,data2,left,right):
    data=pd.merge(data1,data2,left_on=left,right_on=right,how='inner')
    return data
def columnaunica(data,columna):
    return data[columna].unique()

def __evaluar(x, columnas, codunico,cantidad=10,firstfilter=200):
    newdata=pd.DataFrame()
    tenfirst = x.sort_values(by=columnas, ascending=False).head(firstfilter)
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
    return newdata.head(cantidad)   
 
def procesar(data,grupo,filtro,evalular_columnas,especialidad='RADIO-RADIO',acciones='EN SITIO REVISAR Y CORRECCION DE PROBLEMA REPORTADO POR CALIDAD MOVIL'):                
    filtroarbol=pd.DataFrame()
    for registro in grupo:
        datazona=data[data[filtro]==registro]
        datazona=__evaluar(datazona,columnas=evalular_columnas,codunico='CODIGO UNICO',cantidad=10)
        datazona['zona']=registro
        filtroarbol=pd.concat([filtroarbol,datazona])     
    filtroarbol['ESPECIALIDAD']=especialidad
    filtroarbol['ACCIONES']=acciones
    return filtroarbol
 