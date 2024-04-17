from functions import leerarchivo,unirdataframe,columnaunica,procesar

data_lima=leerarchivo('./data/lista_lima.xlsx',['CODIGO UNICO','NOMBRE_EBC','DELTA RTWP (dB) > 2 dB', '# drops 4g','SECTOR'])
data_sector=leerarchivo('./data/codigounico-sector.xlsx',['Codigo Unico','Zona'],'Base')
data_merge=unirdataframe(data_lima,data_sector,'CODIGO UNICO','Codigo Unico')
zona=columnaunica(data_merge,'Zona')
data_arbol=procesar(data_merge,zona,'Zona',['DELTA RTWP (dB) > 2 dB', '# drops 4g'])
print(data_arbol)

