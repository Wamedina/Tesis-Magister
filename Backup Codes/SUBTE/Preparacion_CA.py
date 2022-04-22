#!/usr/bin/env python
# coding: utf-8

# In[ ]:


## Primera parte, separando las variables por año y almacenando la lista de listas en blocks_year

def Separador_Variable_CA (LISTA_VARIABLE_X, bloques_CA):
    j = 0
    blocks_year =[]
    aux_year = []
    for i in LISTA_VARIABLE_X:
        if i == 1:
            a = j//len(bloques_CA)+1
            b = j%len(bloques_CA)
            aux_year.append(int(b))
        if (j+1)%len(bloques_CA) == 0:
            aux_year.sort(reverse = True)
            blocks_year.append(aux_year)
            aux_year=[]
        j += 1
    return blocks_year

def posicionar_bloque_CA(bloque,limites_x_C,limites_y_C,limites_z_C):
    
    # Bloque corresponde al número de este, ejemplo bloque 0 -> x: 0 | y: 0 | z: 0
    # Es importante notar la importancia de la cantidad de bloques en los ejes; bloques_x = 10 | bloques_y = 10 | bloques_z = 10
    # Bloque 56 -> z: Bloque//(bloques_x*bloques_y)                                    -> z: 0  -> aux_z = 0
    #           -> y: (Bloque - (aux_z*(bloques_x*bloques_y)  ))//(bloques_x)          -> y: 5  -> aux_y = 5
    #           -> x: (Bloque - (aux_z*(bloques_x*bloques_y)  ) - (aux_y*bloques_x))   -> x: 6  -> aux_x = 6
    # Ejemplo 2:
    # Bloque 108 -> z: Bloque//(bloques_x*bloques_y)                                    -> z: 1  -> aux_z = 1
    #            -> y: (Bloque - (aux_z*(bloques_x*bloques_y)  ))//(bloques_x)          -> y: 0  -> aux_y = 0
    #            -> x: (Bloque - (aux_z*(bloques_x*bloques_y)  ) - (aux_y*bloques_x))   -> x: 8  -> aux_x = 8
    
    aux_z = bloque//(limites_x_C[3]*limites_y_C[3])
    aux_y = (bloque - aux_z * (limites_x_C[3]*limites_y_C[3]))//limites_x_C[3]
    aux_x = (bloque - aux_z * (limites_x_C[3]*limites_y_C[3])- aux_y * limites_x_C[3])
    
    # Aquí no se escala
    posicion = [aux_x ,aux_y ,aux_z]
    # Se va a escalar
    #posicion = [aux_x - distancia_rebloq[0],aux_y - distancia_rebloq[1],aux_z - (distancia_rebloq[2]/limites_z[0])]
    
    return posicion

def posicion_lista_CA(lista_variable_X_separada,limites_x_C,limites_y_C,limites_z_C,limites_x,limites_y,limites_z,distancia_rebloq,rebloqueo_x,rebloqueo_y,rebloqueo_z):
    lista_final = list()
    for t in lista_variable_X_separada:
        lista_aux = list()
        for bloque in t:
            posicion = posicionar_bloque_CA(bloque,limites_x_C,limites_y_C,limites_z_C)
            
            # posición es de la forma [x,y,z], por lo mismo se aprovechará de des_Rebloquear acá
            for x in range(rebloqueo_x):
                for y in range(rebloqueo_y):
                    for z in range(rebloqueo_z):
                        
                        # Tambien se aprovechará de escalar
                        valor_x = posicion[0]*rebloqueo_x + x - (distancia_rebloq[0]//limites_x[0])
                        valor_y = posicion[1]*rebloqueo_y + y - (distancia_rebloq[1]//limites_y[0])
                        valor_z = posicion[2]*rebloqueo_z + z - (distancia_rebloq[2]//limites_z[0])
                        
                        coordenada_final = [valor_x,valor_y,valor_z]
                        
                        lista_aux.append(coordenada_final)
        lista_final.append(lista_aux)
    return lista_final

def matriz_ca_x (bloques_final, lista_final):
    matriz = []
    for x in range(bloques_final[0] + 1):
        filas_matriz = []
        for y in range(bloques_final[1] + 1):
            columna_matriz = []
            for z in range(bloques_final[2] + 1):
                try:
                    x = 0
                    columna_matriz.append(x)
                except:
                    print(x)
                    print(y)
                    print(z)
            filas_matriz.append(columna_matriz)
        matriz.append(filas_matriz)
        
    for bloque in lista_final:
        matriz[bloque[0]][bloque[1]][bloque[2]] = 1
        
    return matriz
        
        
        

