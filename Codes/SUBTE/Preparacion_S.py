#!/usr/bin/env python
# coding: utf-8

# In[1]:


def Funcion_Resultados_Variables(lista_variable,t_S): 
    X_1_INT = list()
    Y_1_INT = list()
    Z_1_INT = list()
    lista_aux = list()

    for i in range(len(lista_variable)):
        if i <= len(lista_variable)//3:
            if (i) % t_S[max(t_S)] == 0 and i != 0:
                X_1_INT.append(lista_aux)
                lista_aux = []
                lista_aux.append(lista_variable[i])
            else:
                lista_aux.append(lista_variable[i])
        
                
        elif i <= 2*len(lista_variable)//3:
            if (i) % t_S[max(t_S)] == 0 and i != 0:
                Y_1_INT.append(lista_aux)
                lista_aux = []
                lista_aux.append(lista_variable[i])
            else:
                lista_aux.append(lista_variable[i])
                
        else:
            if (i) % t_S[max(t_S)] == 0 and i != 0:
                Z_1_INT.append(lista_aux)
                lista_aux = []
                lista_aux.append(lista_variable[i])
            else:
                lista_aux.append(lista_variable[i])
    Z_1_INT.append(lista_aux)
    return X_1_INT, Y_1_INT, Z_1_INT

def Trabajando_X_S (X_1_INT):
    
    lista_final = list()
    for columnas in range(len(X_1_INT[0])):
        lista_aux = list()
        for filas in X_1_INT:
            lista_aux.append(filas[columnas])
        lista_final.append(lista_aux)
        
    return lista_final

def A_escalar_S (modelo_general,pos_x,pos_y,pos_z):
    
    distancia_x = modelo_general[0][0] - pos_x
    distancia_y = modelo_general[0][1] - pos_y
    distancia_z = modelo_general[0][2] - pos_z
    
    return(distancia_x,distancia_y,distancia_z)

def Separador_Variable_S(X_1_INT):
    lista_final = list()
    X_1 = Trabajando_X_S (X_1_INT)
    for t in X_1:
        dp = 0
        lista_aux = list()
        for columna in t:
            if columna == 1:
                lista_aux.append(dp)
            dp += 1 
        lista_final.append(lista_aux)
    return lista_final

def posicionar_dp_CA_S(dp,x_draw,y_draw,z_draw):

    aux_z = dp//((max(x_draw) + 1)*(max(y_draw) + 1))
    aux_y = (dp - aux_z * ((max(x_draw) + 1)*(max(y_draw) + 1)))//(max(x_draw) + 1)
    aux_x = (dp - aux_z * ((max(x_draw) + 1)*(max(y_draw) + 1)) - aux_y * (max(x_draw) + 1))
    
    posicion = [aux_x ,aux_y ,aux_z]
    
    return posicion

def posicion_lista_S_X(lista_x_S_separada,x_draw,y_draw,z_draw,distancia_x,distancia_y,distancia_z,limites_x,limites_y,limites_z):
    lista_final = list()
    for t in lista_x_S_separada:
        lista_aux = list()
        for dp in t:
            posicion = posicionar_dp_CA_S(dp,x_draw,y_draw,z_draw)
            
            # posición es de la forma [x,y,z], por lo mismo se aprovechará de des_Rebloquear acá
            for x in range(2):
                for y in range(3):
                    # Tambien se aprovechará de escalar
                    valor_x = posicion[0]*2 + x - (distancia_x//limites_x[0])
                    valor_y = posicion[1]*3 + y - (distancia_y//limites_y[0])
                    valor_z = posicion[2] - (distancia_z//limites_z[0])

                    coordenada_final = [valor_x,valor_y,valor_z]

                    lista_aux.append(coordenada_final)
        lista_final.append(lista_aux)
    return lista_final

##########################################################################################################
############################### VARIABLE Y ###############################################################
##########################################################################################################
def Posicion_X_Y_ALL_DP (x_draw,y_draw,z_draw):
    lista = list()
    for i in range((max(x_draw) + 1)*(max(y_draw) + 1)):
        coordenada = posicionar_dp_CA_S(i,x_draw,y_draw,z_draw)
        lista.append(coordenada)
    return lista

def Separador_Variable_S_Y(Y_1_INT,col_height,limites_z):
    lista_final = list()
    for i in range(len(Y_1_INT[0])):
        lista_aux = list()
        for j in range(len(Y_1_INT)):
            lista_aux.append(int(round(Y_1_INT[j][i]*(col_height//limites_z[0]),0)))
        lista_final.append(lista_aux)
    return lista_final

def Separador_Variable_S_Y_ACU (Y_SIN_ACU):
    lista_final = list()
    for i in range(len(Y_SIN_ACU[0])):
        lista_aux = list()
        valor = 0
        for j in range(len(Y_SIN_ACU)):
            valor +=  Y_SIN_ACU[j][i]
            lista_aux.append(valor)
        lista_final.append(lista_aux)
    return lista_final

def Separador_Variable_S_Y_ACU_F(Y_ACU_PRIMA):
    lista_final = list()
    for i in range(len(Y_ACU_PRIMA[0])):
        lista_aux = list()
        for j in range(len(Y_ACU_PRIMA)):
            lista_aux.append(Y_ACU_PRIMA[j][i])
        lista_final.append(lista_aux)
    return lista_final

def Generador_lista_matriz (Y_VAR,dp_cords,distancia_x,distancia_y,distancia_z,limites_x,limites_y,limites_z):
    lista_final_1 = []
    dp = 0
    for i in Y_VAR:
        if i > 0:
            for j in range(i):
                coordenada = [dp_cords[dp][0],dp_cords[dp][1],dp_cords[dp][2]+j]
                lista_final_1.append(coordenada)
        dp += 1
        
    ## Se escalará la variable a continuación
    lista_final_2 = []
    for i in lista_final_1:
        for x in range(2):
            for y in range(3):
                valor_x = i[0]*2 + x - (distancia_x//limites_x[0])
                valor_y = i[1]*3 + y - (distancia_y//limites_y[0])
                valor_z = i[2] - (distancia_z//limites_z[0])
                
                coordenada_final = [valor_x,valor_y,valor_z]
                lista_final_2.append(coordenada_final)   
    return lista_final_2

def coordenadas_Y_S_GLOBAL(Y_VAR,dp_cords,distancia_x,distancia_y,distancia_z,limites_x,limites_y,limites_z):
    LISTA = []
    for i in Y_VAR:
        lista_aux = Generador_lista_matriz(i,dp_cords,distancia_x,distancia_y,distancia_z,limites_x,limites_y,limites_z)
        LISTA.append(lista_aux)
    return LISTA


# In[ ]:




