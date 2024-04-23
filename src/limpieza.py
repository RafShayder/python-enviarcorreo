# Author: Raf Shayder Leon Gutierrez, Telco Asociado : https://www.linkedin.com/in/raf-shayder-leon
 #2024-04-12 
import pandas as pd
class Limpieza:
    data=None
    especialidad='RADIO-RADIO'
    acciones='EN SITIO REVISAR Y CORRECCION DE PROBLEMA REPORTADO POR CALIDAD MOVIL'
    cantidadtop=10
    cantidadfirsttop=100
    
    def __init__(self,nombrecodunico,concatenardetalle,listsort,ordenlista,nombrezona): 
        self.nombrecodunico=nombrecodunico
        self.concatenardetalle=concatenardetalle
        self.listsort=listsort
        self.ordenlista=ordenlista
        self.nombrezona=nombrezona
        
    def leerarchivo(self,rutaexcel,nombrehoja=None):
        if(rutaexcel.endswith('.csv')):
            #prueba
            data= pd.read_csv(rutaexcel,on_bad_lines='skip',sep=';',low_memory=False)
        elif (rutaexcel.endswith('.xlsx')):   
            data= pd.read_excel(rutaexcel) if nombrehoja==None else pd.read_excel(rutaexcel,sheet_name=nombrehoja)
        else:
            print('Error al leer datos, tipo de archivo')
            data=None
        #data=data[campos]
        return data
    def unirdataframe(self,data1,data2,keyleft,keyright):
        data=pd.merge(data1,data2,left_on=keyleft,right_on=keyright,how='inner')
        self.data=data
        return data
    def procesar(self,data):
        filtroarbol=pd.DataFrame()
        grupo= data[self.nombrezona].unique()
        for registro in grupo:
            datazona=data[data[self.nombrezona]==registro] #zona
            datazona=self.__evaluar(datazona)
            datazona['zona']=registro
            filtroarbol=pd.concat([filtroarbol,datazona])
        filtroarbol['ESPECIALIDAD']=self.especialidad
        filtroarbol['ACCIONES']=self.acciones
        self.data=filtroarbol
        return filtroarbol
    def reordenar(self,listaorden):
        return self.data[listaorden]
    def blacklist(self,data,nombrecoldata,blacklist):
        blacklistdata=self.leerarchivo(blacklist)
        return data[ ~data[nombrecoldata].isin(blacklistdata.iloc[:, 0])]
        
    def __evaluar(self,x):
        newdata=pd.DataFrame()
        tenfirst = x.sort_values(by=self.listsort, ascending=self.ordenlista).head(self.cantidadfirsttop)
        registros=tenfirst[self.nombrecodunico].unique()
        for ss,cod in enumerate(registros):
            row ={'ID_UNICO':cod,'PROBLEMA':'*PROACTIVO CALIDAD MOVIL |'}
            unirdup=tenfirst[tenfirst[self.nombrecodunico]==cod]
            for index, unir in unirdup.iterrows():
                row['PROBLEMA']+='*'
                for a in self.concatenardetalle:
                    row['PROBLEMA']+='{} : '.format(a)+'{} -'.format(unir[a])                
            row["PROBLEMA"]=[row['PROBLEMA']]
            temp=pd.DataFrame(row,index=[ss])
            newdata=pd.concat([newdata,temp],sort=False)
        return newdata.head(self.cantidadtop)
         
   