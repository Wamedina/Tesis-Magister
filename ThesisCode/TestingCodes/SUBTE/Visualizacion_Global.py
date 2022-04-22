#!/usr/bin/env python
# coding: utf-8

# In[1]:


def valor_extra (limite1,limite2):
    valor_aux_1 = 0
    valor_aux_2 = 0
    LARGO = limite2[0]//limite1[0]
    for i in range(LARGO):
        valor_aux_1 += valor_aux_2
        valor_aux_2 += limite1[0]
        
    valor_extra = valor_aux_1//(LARGO)
    return valor_extra

def Escalado_conjunto_posicion (limites_x,limites_y,limites_z,limites_x_C,limites_y_C,limites_z_C):
     
    extra_x = valor_extra (limites_x,limites_x_C)
    extra_y = valor_extra (limites_y,limites_y_C)
    extra_z = valor_extra (limites_z,limites_z_C)
        
    x_min = min(limites_x[2],limites_x_C[2] - extra_x)
    y_min = min(limites_y[2],limites_y_C[2] - extra_y)
    z_min = min(limites_z[2],limites_z_C[2] - extra_z)
    
    x_max = max(limites_x[1],limites_x_C[1]+ extra_x)
    y_max = max(limites_y[1],limites_y_C[1]+ extra_y)
    z_max = max(limites_z[1],limites_z_C[1]+ extra_z)
    
    escalado = (x_min,y_min,z_min,x_max,y_max,z_max)
    
    dif_no_rebloq = (-limites_x[2] + x_min, -limites_y[2] + y_min, -limites_z[2] + z_min)
    dif_rebloq = (-limites_x_C[2] + x_min + extra_x, -limites_y_C[2] + y_min + extra_y, -limites_z_C[2] + z_min + extra_z)
    
    ### Escalado es de la forma (x_min, y_min, z_min, x_max, y_max, z_max)
    
    ### dif_no_rebloq es de la forma (distancia del origen del modelo no rebloqueado al global en x,y,z)
    
    ### dif_rebloq es de la forma (distancia del origen del modelo rebloqueado al global en x,y,z)
    
    bloques_x = (x_max-x_min)//limites_x[0]
    bloques_y = (y_max-y_min)//limites_y[0]
    bloques_z = (z_max-z_min)//limites_z[0]
    bloques_final = (bloques_x,bloques_y,bloques_z) 
    
    return escalado , dif_no_rebloq, dif_rebloq , bloques_final

## Generador de la matriz global
def matriz_global (bloques_final):
    matriz = []
    for x in range(bloques_final[0] + 1):
        filas_matriz = []
        for y in range(bloques_final[1] + 1):
            columna_matriz = []
            for z in range(bloques_final[2] + 1):
                x = 0
                columna_matriz.append(x)
            filas_matriz.append(columna_matriz)
        matriz.append(filas_matriz)
    return matriz
                

