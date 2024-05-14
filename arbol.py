# Author: Raf Shayder Leon Gutierrez, Telco Asociado : https://www.linkedin.com/in/raf-shayder-leon
 #2024-04-12 
from src.limpieza import Limpieza
from src.enviogmail import Email
#'Movil Lima'
def Lima_movil():
    limpiarLima=Limpieza('CODIGO UNICO',['DELTA RTWP (dB) > 2 dB','# drops 4g','SECTOR','CEI','BANDA'],['CEI','DELTA RTWP (dB) > 2 dB', '# drops 4g'],[True,False,False],'Zona')
    limadata=limpiarLima.leerarchivo('./inputvariable/LimaMovil.xlsx')
    limadata=limpiarLima.blacklist(limadata,'CODIGO UNICO','./datastatic/blacklist.xlsx')
    zonadata=limpiarLima.leerarchivo('./datastatic/codigounico-sector.xlsx','Base')
    marge=limpiarLima.unirdataframe(limadata,zonadata,'CODIGO UNICO','Codigo Unico')
    newdata=limpiarLima.procesar(marge)
    newdata=limpiarLima.unirdataframe(newdata,zonadata,'ID_UNICO','Codigo Unico')
    newdata=limpiarLima.reordenar(['Departamento','Nombre Sitio','Tipo de Sitio HISPAM','zona','ID_UNICO','ESPECIALIDAD','PROBLEMA','ACCIONES'])
    #newdata.to_excel("Data_Lima_movil.xlsx",index=False)
    return newdata
def Provincia_movil():
    limpiarProvincia=Limpieza('CODIGO UNICO',['DELTA RTWP (dB) > 2 dB','# drops 4g','SECTOR','CEI','BANDA'],['DELTA RTWP (dB) > 2 dB', '# drops 4g'],[False,False],'Zona')
    limadata=limpiarProvincia.leerarchivo('./inputvariable/ProvinciaMovil.xlsx')
    limadata=limpiarProvincia.blacklist(limadata,'CODIGO UNICO','./datastatic/blacklist.xlsx')
    zonadata=limpiarProvincia.leerarchivo('./datastatic/codigounico-sector.xlsx','Base')
    marge=limpiarProvincia.unirdataframe(limadata,zonadata,'CODIGO UNICO','Codigo Unico')
    newdata=limpiarProvincia.procesar(marge)
    newdata=limpiarProvincia.unirdataframe(newdata,zonadata,'ID_UNICO','Codigo Unico')
    newdata=limpiarProvincia.reordenar(['Departamento','Nombre Sitio','Tipo de Sitio HISPAM','zona','ID_UNICO','ESPECIALIDAD','PROBLEMA','ACCIONES'])
    #newdata.to_excel("Data_Lima_movil.xlsx",index=False)
    return newdata


def Temperatura():
    #'Temperatura'
    temperatura=Limpieza('CodigoUnicoEStacion',['FRU','BOARD','PRODUCTNUMBER','SERIAL','TEMP'],['TEMP'],[False],'Zona')
    temperatura.cantidadtop=8
    temperatura.problemainicial='*PROACTIVO ATENUACIONES |'
    temperatura.acciones='EN SITIO REVISAR Y CORRECCION DE PROBLEMA REPORTADO POR Temperatura'
    temperaturadata=temperatura.leerarchivo('./inputvariable/ATENUACIONES FO Y TEMPERATURA DE RRU.xlsx','TEMPERATURA RRU')
    codunico_nombreunico=temperatura.leerarchivo('./datastatic/CLASE_ESTACIONES_BASE_SECTOR.csv')
    codunico_nombreunico=codunico_nombreunico.drop_duplicates(subset='Nombre Estacion Base Estandar(Ingenieria)', keep = 'first')
    marge1=temperatura.unirdataframe(temperaturadata,codunico_nombreunico,'EB','Nombre Estacion Base Estandar(Ingenieria)')
    zonadata=temperatura.leerarchivo('./datastatic/codigounico-sector.xlsx','Base') #se repite
    marge=temperatura.unirdataframe(marge1,zonadata,'CodigoUnicoEStacion','Codigo Unico')
    newdata=temperatura.procesar(marge)
    newdata=temperatura.unirdataframe(newdata,zonadata,'ID_UNICO','Codigo Unico')
    newdata=temperatura.reordenar(['Departamento','Nombre Sitio','Tipo de Sitio HISPAM','zona','ID_UNICO','ESPECIALIDAD','PROBLEMA','ACCIONES'])
    #newdata.to_excel("Data_Provincia_movil.xlsx",index=False)
    return newdata

def Atenuaciones():
    #'Atenuaciones'
    atenuaciones=Limpieza('CodigoUnicoEStacion',['WL1','WL2','DlLoss','UlLoss','mmax'],['mmax'],[False],'Zona')
    atenuaciones.cantidadtop=8
    atenuaciones.problemainicial='*PROACTIVO ATENUACIONES |'
    atenuaciones.acciones='EN SITIO REVISAR Y CORRECCION DE PROBLEMA REPORTADO POR ATENUACIONES'
    atenuacionesdata=atenuaciones.leerarchivo('./inputvariable/ATENUACIONES FO Y TEMPERATURA DE RRU.xlsx','ATENUACIONES EN FO')
    atenuacionesdata['mmax']=atenuacionesdata[['DlLoss','UlLoss']].max(axis=1)
    codunico_nombreunico=atenuaciones.leerarchivo('./datastatic/CLASE_ESTACIONES_BASE_SECTOR.csv')
    codunico_nombreunico=codunico_nombreunico.drop_duplicates(subset='Nombre Estacion Base Estandar(Ingenieria)', keep = 'first')
    marge1=atenuaciones.unirdataframe(atenuacionesdata,codunico_nombreunico,'EB','Nombre Estacion Base Estandar(Ingenieria)')
    zonadata=atenuaciones.leerarchivo('./datastatic/codigounico-sector.xlsx','Base') #se repite
    marge=atenuaciones.unirdataframe(marge1,zonadata,'CodigoUnicoEStacion','Codigo Unico')
    newdata=atenuaciones.procesar(marge)
    newdata=atenuaciones.unirdataframe(newdata,zonadata,'ID_UNICO','Codigo Unico')
    newdata=atenuaciones.reordenar(['Departamento','Nombre Sitio','Tipo de Sitio HISPAM','zona','ID_UNICO','ESPECIALIDAD','PROBLEMA','ACCIONES'])
    #newdata.to_excel("Data_Atenuaciones_movil.xlsx",index=False)
    return newdata



datalima=Lima_movil()
dataprovincia=Provincia_movil()
datatemperatura=Temperatura()
dataatenuacion=Atenuaciones()
correo=Email('ticketsproactivos@gmail.com','tyez inuc oijr jitushadw','raf.leon@telefonica.com,dalia.rodriguez@telefonica.com','Prueba',cc='angela.bastidas@telefonica.com')
correo.adjuntardata(datalima, 'data_Lima_Movil.xlsx')
correo.adjuntardata(dataprovincia,'data_Provincia_Movil.xlsx')
correo.adjuntardata(datatemperatura,'dataTemperatura.xlsx')
correo.adjuntardata(dataatenuacion,'dataAtenuaciones.xlsx')
correo.enviarMail()



