
from src.limpieza import Limpieza
limpiar=Limpieza('CODIGO UNICO','DELTA RTWP (dB) > 2 dB','# drops 4g','SECTOR',['CEI','DELTA RTWP (dB) > 2 dB', '# drops 4g'],[True,False,False],'Zona')
limadata=limpiar.leerarchivo('./inputvariable/LimaMovil.xlsx')
limadata=limpiar.blacklist(limadata,'CODIGO UNICO','./datastatic/blacklist.xlsx')
zonadata=limpiar.leerarchivo('./datastatic/codigounico-sector.xlsx','Base')
marge=limpiar.unirdataframe(limadata,zonadata,'CODIGO UNICO','Codigo Unico')
newdata=limpiar.procesar(marge)
newdata=limpiar.unirdataframe(newdata,zonadata,'ID_UNICO','Codigo Unico')
newdata=limpiar.reordenar(['Departamento','Nombre Sitio','Tipo de Sitio HISPAM','zona','ID_UNICO','ESPECIALIDAD','PROBLEMA','ACCIONES'])
newdata.to_excel("prueba.xlsx",index=False)
