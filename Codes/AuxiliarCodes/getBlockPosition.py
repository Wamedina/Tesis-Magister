def getBlockPosition(bloque,limites_x_C,limites_y_C, limites_z):
    
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
    #distancia_rebloq = [10,10,10]
    # Aquí no se escala
    posicion = [aux_x ,aux_y ,aux_z]
    # Se va a escalar
    
    #posicion = [aux_x - distancia_rebloq[0],aux_y - distancia_rebloq[1],aux_z - (distancia_rebloq[2]/limites_z[0])]
    
    return posicion