import numpy as np
import utm
from sklearn.svm import SVR

import YpacaraiMap

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

env = YpacaraiMap.Environment()

mapa = env.map

# Se cargan las coordenadas de latitud y longitud obtenidas manualmente
# En este caso para 15 celdas del gridmap con celdas de 100mx100m

p0 = [-25.346476113643277, -57.28133913439803]
p1 = [-25.363539923964645, -57.28254076409904]
p2 = [-25.36881370533408, -57.29017969576969]
p3 = [-25.300037593310133, -57.3735570475954]
p4 = [-25.260975667187203, -57.32038225220115]
p5 = [-25.292176099134856, -57.32261385052005]
p6 = [-25.29760818972855, -57.30656351079545]
p7 = [-25.26493437489381, -57.356860295979025]
p8 = [-25.29465937091989, -57.37651552351105]
p9 = [-25.35611105817815, -57.285251810002826]
p10 = [-25.366852927272355, -57.28613157436048]
p11 = [-25.301823353381646, -57.37362317249816]
p12 = [-25.316370468388683, -57.29098419815847]
p13 = [-25.285797119341243, -57.32162575467919]
p14 = [-25.259718325613484, -57.34849076154806]


coords = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14]

p0c = [85,96]
p1c = [84,112]
p2c = [77,117]
p3c = [2,51]
p4c = [50,14]
p5c = [48,44]
p6c = [63,49]
p7c = [19,17]
p8c = [1,48]
p9c = [81,103]
p10c = [80,115]
p11c= [3,53]
p12c= [77,69]
p13c= [49,37]
p14c= [25,13]


pixels = [p0c, p1c, p2c, p3c, p4c, p5c, p6c, p7c, p8c, p9c, p10c, p11c, p12c, p13c, p14c]

x = []
y = []

# Se pasa a utm y se obtienen las coordenadas x e y

for i in range(len(pixels)):
    r = utm.from_latlon(coords[i][0], coords[i][1])
    x.append(r[0])
    y.append(r[1])

# Se separan los indices x e y de los puntos de muestra
xp = []    
yp = []

for p in pixels:
    xp.append(p[0])
    yp.append(p[1])
    
# Se crean dos regresores, uno para x y otro para y

clf_x = SVR(kernel='poly', C=1e3, degree=1)
clf_y = SVR(kernel='poly', C=1e3, degree=1)

# Se entrena cada regresor
clf_x.fit(np.array(xp).reshape(-1, 1), x)
clf_y.fit(np.array(yp).reshape(-1, 1), y)


# Se obtienen las coordenadas utm para todos los indices del gridmap
xtest = range(mapa.shape[1])
ytest = range(mapa.shape[0])

resx = clf_x.predict(np.array(xtest).reshape(-1, 1))
resy = clf_y.predict(np.array(ytest).reshape(-1, 1))

        
# Se guardan las coordenadas para utilziarlas en el conversor        
np.save("resx_100.npy",resx)
np.save("resy_100.npy",resy)


# Se almacenan las coordenadas de latitud y longitud de la superficie del lago
# en formato csv para su visualizacion en el mapa
res_coords = []

for i in range(len(resx)):
    for j in range(len(resy)):
        if mapa[j][i] == 0:
            continue
        u = [resx[i], resy[j], 21, 'J']
        r = utm.to_latlon(*u)
        res_coords.append(r)

coord_lago = open("lago_100.csv", 'w')
for c in res_coords:
    coord_lago.writelines(str(c[0]) + "," + str(c[1]) +"\n")
coord_lago.close()