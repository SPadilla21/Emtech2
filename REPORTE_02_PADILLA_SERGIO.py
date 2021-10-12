import csv
lista_datos = []
with open("synergy_logistics_database.csv", "r") as archivo:
    datos = csv.DictReader (archivo)
    for linea in datos:
        lista_datos.append(linea)

def nueva_seccion(titulo, n):  #Función para crear un título personalizado para cada sección
    print(titulo.center(n))
    print(str(  str("-")*(len(titulo)*2)).center(n))

def rutas(direccion, k=2):  #sorting key: 2 ordena segun total de movimientos, 3 ordena segun valor total $
    c, v = 0,0  #Contadores para total de movimeintos y valor total $
    ruta_actual, ruta_cont, ruta_final = [], [], []  #listas para almacenar valores y llevar conteos
    for i in lista_datos:    #por cada diccionario en la lista de datos que contiene la información de los movimientos
        if i["direction"] == direccion:    #Si la dirección es "imports" o "exports" según sea el aso
            ruta_actual = [i["origin"], i["destination"]]   #adjunta a ruta_actual el origen y el destino
            if ruta_actual not in ruta_cont:    #Si la ruta no ha sido contada anteriormente
                for j in lista_datos:   #vuelve a leer el archivo original linea por linea
                    if ruta_actual == [j["origin"], j["destination"]]:   #si encuentra un match de origen y destino
                        c+=1   #suma 1 al contador de movimientos para la ruta específica
                        v+= int(j["total_value"])   #sumael valor del movimiento al contador del valor total
                ruta_cont.append(ruta_actual)    #agrega la ruta contada al contador de rutas
                ruta_final.append([i["origin"], i["destination"], c, v])  #a otra lista final, adjunta la ruta y el total de movimentos e ingresos
                c, v = 0, 0  #resetea los contadores a cero para volver a analizar otra ruta
    ruta_final.sort(reverse=True, key= lambda x: x[k])  #Ordena la lista de rutas de mayor a menor de acuerdo al elemento K de esa lista
    return ruta_final

print('''Opción 1) Rutas de importación y exportación. Synergy logistics está 
considerando la posibilidad de enfocar sus esfuerzos en las 10 rutas más 
demandadas. Acorde a los flujos de importación y exportación, ¿cuáles son esas 
10 rutas? ¿le conviene implementar esa estrategia? ¿porqué? 
''')

nueva_seccion("OPCION 1: FLUJOS DE IMPORTACIONES Y EXPORTACIONES", 100)
nueva_seccion("EXPORTACIONES", 50)
print("ORIGEN\t\tDESTINO\t\tTOTAL DE MOVIMIENTOS")
c=1
tot = 0
for i in rutas("Exports"):  #Para exportaciones, calcula el total de movimientos
    tot += i[2]

for i in rutas("Exports"): #Imprime cada elemento de la lista de rutas para Exportaciones
    if c <= 10:
        print(f"{i[0]} \t {i[1]} \t {i[2]} ({round( i[2]*100/tot,1)}%)")  #A la impresión también se agrega el cálculo del % relativo
    c+=1
print(f"\nEn total se han contratado {tot} servicios de exportaciones.\n")

nueva_seccion("IMPORTACIONES", 50)
print("ORIGEN\t\tDESTINO\t\tTOTAL DE MOVIMIENTOS")
c=1
tot = 0
for i in rutas("Imports"):
    tot += i[2]
for i in rutas("Imports"):
    if c <= 10:
        print(f"{i[0]} \t {i[1]} \t {i[2]} ({round( i[2]*100/tot,1)}%)")
    c+=1
print(f"\nEn total se han contratado {tot} servicios de importaciones.\n\n")

print(
'''Opción 2) Medio de transporte utilizado. ¿Cuáles son los 3 medios de transporte
más importantes para Synergy logistics considerando el valor de las
importaciones y exportaciones? ¿Cuál es medio de transporte que podrían
reducir?
''')

tipo_transporte, c_transp = [], {}  #lista para almacenar el tipo de transporte y un diccionario que facilite el conteo
for i in lista_datos:  #por cada linea en mi archivo de datos
    tipo_transporte.append( [i["transport_mode"], int(i["total_value"])] ) #adjunta a la lista el tipo de transporte y el valor total

for i in tipo_transporte:  #por cada ingreso en la lista de tipo de transporte
    if i[0] not in c_transp:  #Si el tipo de transporte no ha sido agregado al diccionario
        c_transp[i[0] ] = i[1]  #agrega el tipo de transporte y su valor total al diccionario
    else:  #si ya estaba dado de alta en el diccionario
        c_transp[i[0]] += i[1]   #Busca el medio de transporte en el diccionario, y al valor anterior súmale el valor $ actual

nueva_seccion("OPCION 2: MEDIOS DE TRANSPORTE MÁS USADOS", 70)
print("\nMEDIO\t\tINGRESOS TOTALES")
tot = sum(c_transp.values())   #Calcula la suma total del valor $ para todos los tipos de transporte

for i in c_transp: #Para cada elemento del diccionario de conteo de transporte
    print(f"{i}\t\t${c_transp[i]} ({round(c_transp[i]*100/tot,1)}%)")  #Imprime cada medio de transporte, el valor total $ y el % relativo

print('''Opción 3) Valor total de importaciones y exportaciones. Si Synergy Logistics 
quisiera enfocarse en los países que le generan el 80% del valor de las 
exportaciones e importaciones ¿en qué grupo de países debería enfocar sus 
esfuerzos?
''')

def rutas_pais(direccion):  #Función similar al conteo de rutas, pero ahora será solo considerando el país de origen
    c,v = 0,0
    paises, pais_ordenado = {}, []
    for linea in lista_datos:
        #print(linea)
        if linea["direction"] == direccion:
            if linea["origin"] not in paises:
                paises[linea["origin"]] = int(linea["total_value"])
            else:
                paises[linea["origin"]] += int(linea["total_value"])
    for p in paises:
        pais_ordenado.append([p, paises[p]])
    pais_ordenado.sort(reverse=True, key= lambda x: x [1])
    return pais_ordenado

print("\n\n")
nueva_seccion("OPCION 3: VALOR TOTAL DE IMPORTACIONES Y EXPORTACIONES.", 100)
nueva_seccion("EXPORTACIONES", 50)
print("ORIGEN\t\tVALOR TOTAL\t\t% ACUMULADO")
p=0  #Controla el porcentaje acumulado del valor total
tot_exp = 0
for i in rutas_pais("Exports"):
    tot_exp += i[1] #Suma solo el valor total

for i in rutas_pais("Exports"):
    if p < 80:
        print(f"{i[0]} \t {i[1]} ({round( i[1]*100/tot_exp,1)}%)\t\t{round(p,1)}%")
    p += round( i[1]*100/tot_exp,1)
print(f"\nValor total de las exportaciones: ${tot_exp}\n")

nueva_seccion("IMPORTACIONES", 50)
print("ORIGEN\t\tVALOR TOTAL\t\t% ACUMULADO")
p=0  #Controla el porcentaje acumulado del valor total
tot_imp = 0
for i in rutas_pais("Imports"):
    tot_imp += i[1] #Suma solo el valor total

for i in rutas_pais("Imports"):
    if p < 80:
        print(f"{i[0]} \t {i[1]} ({round( i[1]*100/tot_imp,1)}%)\t\t{round(p,1)}%")
    p += round( i[1]*100/tot_imp,1)
print(f"\nValor total de las importaciones: ${tot_imp}\n")

