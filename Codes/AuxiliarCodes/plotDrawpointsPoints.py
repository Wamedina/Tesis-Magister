import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from getDrawpointPosition import getDrawpointPosition
from mpl_toolkits.mplot3d import Axes3D

def plotDrawpointsPoints(numberOfDrawpoints,drawpoints_xdt_values,periods,x_draw,y_draw,z_draw): 
    colors = ['purple',       # Morado
                'blue',      # Azul
                'skyblue',      # Celeste
                'green',      # Verde
                'yellow',      # Amarillo
                '#ff5b00',      # Naranjo
                '#380282',      # Rojo
                '#000000'       # Negro
            ]  # Define más colores si tienes más periodos.

    purple = mpatches.Patch(color='purple', label = "Period 1")
    blue = mpatches.Patch(color='blue', label = "Period 2")
    blue_sky = mpatches.Patch(color='skyblue', label = "Period 3")
    green = mpatches.Patch(color='green', label = "Period 4")
    yellow = mpatches.Patch(color='yellow', label = "Period 5")

    # Creamos una matriz 3D de False con las dimensiones de los limites.
    voxels = np.zeros((30,30,30), dtype=bool)

    # Creamos una matriz 3D para los colores.
    colors_voxels = np.empty(voxels.shape, dtype=object)
    for drawpoint_index in range(numberOfDrawpoints):
        for period in range(periods):#len(drawpoints_xdt)):
            if drawpoints_xdt_values[(drawpoint_index, period)] == 1:
                posicion = getDrawpointPosition(drawpoint_index,x_draw,y_draw,z_draw)
                voxels[posicion[0], posicion[1], posicion[2]] = True
                colors_voxels[posicion[0], posicion[1], posicion[2]] = colors[period % len(colors)]  # Ciclamos a través de los colores.

    fig = plt.figure(figsize=(15,15))
    ax = fig.add_subplot(projection='3d')
    ax.set_aspect('auto')
    plt.legend(["a"],["b"])
    ax.set_xlabel('Axis X',fontsize= 25)
    ax.set_ylabel('Axis Y',fontsize= 25)
    ax.set_zlabel('Axis Z',fontsize= 25)
    ax.zaxis.set_tick_params(labelsize = 25)
    ax.xaxis.set_tick_params(labelsize = 25)
    ax.yaxis.set_tick_params(labelsize = 25)
    ax.legend(handles=[purple,blue, blue_sky, green, yellow])
    ax.voxels(voxels, facecolors=colors_voxels, edgecolor='none')

    plt.show()