import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from mpl_toolkits.mplot3d import Axes3D
from getBlockPosition import getBlockPosition


def plotIntegratedOmpSolution(limites_x_C,limites_y_C,limites_z_C, drawpoints_blocks,drawpoints_xdt, drawpoints_ydt, periods,openPitDict): 
    colors = ['purple',    #Morado
                'blue',    #Azul
                'skyblue', #Celeste
                'green',   #Verde
                'yellow',  #Amarillo
                '#800000', #maroon
                '#9A6324', #Brown
                '#808000', #Olive
                '#469990', #Teal
                '#000075', #Navy
                '#e6194B', #Red
                '#f58231', #naranjo
                '#bfef45', #lime
                '#42d4f4', #Cyan
                '#f032e6', #magenta  
                '#fabed4', #Pink
                '#ffd8b1', #Apricot
                '#fffac8', #Beige
                '#000000', #negro
                '#dcbeff', #lavanda
            ]  # Define más colores si tienes más periodos.
    purple = mpatches.Patch(color='purple', label = "Period 1")
    blue = mpatches.Patch(color='blue', label = "Period 2")
    blue_sky = mpatches.Patch(color='skyblue', label = "Period 3")
    green = mpatches.Patch(color='green', label = "Period 4")
    yellow = mpatches.Patch(color='yellow', label = "Period 5")
    maroon  = mpatches.Patch(color='#800000', label = "Period 6")
    brown = mpatches.Patch(color='#9A6324', label = "Period 7")
    olive = mpatches.Patch(color='#808000', label = "Period 8")
    Teal = mpatches.Patch(color='#469990', label = "Period 9")
    Navy = mpatches.Patch(color='#000075', label = "Period 10")
    Red = mpatches.Patch(color='#e6194B', label = "Period 11")
    naranjo = mpatches.Patch(color='#f58231', label = "Period 12")
    lime = mpatches.Patch(color='#bfef45', label = "Period 13")
    Cyan = mpatches.Patch(color='#42d4f4', label = "Period 14")
    magenta = mpatches.Patch(color='#f032e6', label = "Period 15")
    Pink = mpatches.Patch(color='#fabed4', label = "Period 16")
    Apricot = mpatches.Patch(color='#ffd8b1', label = "Period 17")
    Beige = mpatches.Patch(color='#fffac8', label = "Period 18")
    negro = mpatches.Patch(color='#000000', label = "Period 19")
    lavanda = mpatches.Patch(color='#dcbeff', label = "Period 20")
    colors_patches = [purple,blue, blue_sky, green, yellow,maroon,brown,olive,Teal,Navy,Red,naranjo,lime,Cyan,magenta,Pink,Apricot,Beige,negro,lavanda]


    # Creamos una matriz 3D de False con las dimensiones de los limites.
    voxels = np.zeros((limites_x_C[3], limites_y_C[3], limites_z_C[3]), dtype=bool)

    # Creamos una matriz 3D para los colores.
    colors_voxels = np.empty(voxels.shape, dtype=object)

    for drawpoint in drawpoints_blocks:
        blocks = drawpoints_blocks[drawpoint].copy()
        for period in range(periods):#len(drawpoints_xdt)):
            if drawpoints_xdt[(drawpoint, period)] == 1:
                extracted_percentage = drawpoints_ydt[(drawpoint, period)]
                num_blocks = int(extracted_percentage * len(blocks))
                for i in range(num_blocks):
                    if blocks:
                        bloque = blocks.pop(0)  # Extraemos los bloques en orden.
                        posicion = getBlockPosition(bloque,limites_x_C,limites_y_C, limites_z_C)#posicionar_dp_CA_S(drawpoint,bloque,x_draw,y_draw,z_draw,limites_x_C, limites_y_C)
                        voxels[posicion[0], posicion[1], posicion[2]] = True
                        colors_voxels[posicion[0], posicion[1], posicion[2]] = colors[period % len(colors)]  # Ciclamos a través de los colores.

    # Creamos una matriz 3D de False con las dimensiones de los limites.

    # Creamos una matriz 3D para los colores.

    for bloque in openPitDict:
        posicion = getBlockPosition(bloque,limites_x_C,limites_y_C, limites_z_C)#posicionar_dp_CA_S(drawpoint,bloque,x_draw,y_draw,z_draw,limites_x_C, limites_y_C)
        voxels[posicion[0], posicion[1], posicion[2]] = True
        period = openPitDict[bloque]
        colors_voxels[posicion[0], posicion[1], posicion[2]] = colors[period % len(colors)]  # Ciclamos a través de los colores.

    fig = plt.figure(figsize=(15,15))
    ax = fig.add_subplot(projection='3d')
    #ax.set_aspect('auto')
    plt.legend(["a"],["b"])
    ax.set_xlabel('Axis X',fontsize= 25)
    ax.set_ylabel('Axis Y',fontsize= 25)
    ax.set_zlabel('Axis Z',fontsize= 25)
    ax.zaxis.set_tick_params(labelsize = 25)
    ax.xaxis.set_tick_params(labelsize = 25)
    ax.yaxis.set_tick_params(labelsize = 25)
    ax.legend(handles=colors_patches[:periods])
    ax.voxels(voxels, facecolors=colors_voxels, edgecolor='none')
    

    plt.show()