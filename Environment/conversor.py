import numpy as np
import utm


# Se cargan las coordenadas obtenidas por los regresores entrenados
resx = np.load("resx_100.npy")
resy = np.load("resy_100.npy")


# Funcion para obtener las coordenadas de latitud y longitud de la celda (x,y)
def index_to_latlon(x, y):
    u = [resx[x], resy[y], 21, 'J']
    r = utm.to_latlon(*u)
    return r

# Funcion para obtener los indices de la celda correspondiente a un punto
# mediante las coordenadas de latitud y longitud del mismo
# Si el punto se encuentra fuera del area de cobertura del gridmap
# se devuelve la celda mas cercana al mismo
def latlon_to_index(lat,lon):
    r = utm.from_latlon(lat, lon)
    x = mas_cercano(resx, r[0])
    y = mas_cercano(resy, r[1])
    return [x, y]
    
def mas_cercano(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

