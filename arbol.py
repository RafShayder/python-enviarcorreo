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
    #'Movil Provincias'
    limpiarProvincias=Limpieza('CodigoUnicoEStacion',['FRU','BOARD','PRODUCTNUMBER','SERIAL','TEMP'],['TEMP'],[True],'Zona')
    limpiarProvincias.cantidadtop=8
    provinciadata=limpiarProvincias.leerarchivo('./inputvariable/ATENUACIONES FO Y TEMPERATURA DE RRU.xlsx','TEMPERATURA RRU')
    codunico_nombreunico=limpiarProvincias.leerarchivo('./datastatic/CLASE_ESTACIONES_BASE_SECTOR.csv')
    codunico_nombreunico=codunico_nombreunico.drop_duplicates(subset='Nombre Estacion Base Estandar(Ingenieria)', keep = 'first')
    marge1=limpiarProvincias.unirdataframe(provinciadata,codunico_nombreunico,'EB','Nombre Estacion Base Estandar(Ingenieria)')
    zonadata=limpiarProvincias.leerarchivo('./datastatic/codigounico-sector.xlsx','Base') #se repite
    marge=limpiarProvincias.unirdataframe(marge1,zonadata,'CodigoUnicoEStacion','Codigo Unico')
    newdata=limpiarProvincias.procesar(marge)
    newdata=limpiarProvincias.unirdataframe(newdata,zonadata,'ID_UNICO','Codigo Unico')
    newdata=limpiarProvincias.reordenar(['Departamento','Nombre Sitio','Tipo de Sitio HISPAM','zona','ID_UNICO','ESPECIALIDAD','PROBLEMA','ACCIONES'])
    #newdata.to_excel("Data_Provincia_movil.xlsx",index=False)
    return newdata
datalima=Lima_movil()
dataprovincia=Provincia_movil()
correo=Email('ticketsproactivos@gmail.com','tyez inuc oijr jitush','raf.leon@telefonica.com','Prueba',cc='angela.bastidas@telefonica.com')
correo.adjuntardata(datalima, 'data_Lima_Movil.xlsx')
correo.adjuntardata(dataprovincia,'data_Provincia_Movil.xlsx')
correo.enviarMail()