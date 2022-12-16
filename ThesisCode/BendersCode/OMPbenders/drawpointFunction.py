def drawpointFunction(pos_x, pos_y, pos_z, col_height, DP_init, limites_x, limites_y, limites_z, TON, CP_S, CM_S, MIN, LEY, 
                      pos_x_f, pos_y_f, orientacion):
    init_block = int((pos_z-limites_z[2])/10 * limites_x[3] * limites_y[3] + (pos_y-limites_y[2])/10 * limites_x[3] +  
                     (pos_x-limites_x[2])/10)

    x_draw = []
    A = pos_x_f - pos_x

    if int((A)/10+1)%2 == 0:
        for i in range(0,int((A)/10+1)//2):
            x_draw.append(i)
    else:
        for i in range(0,int((A)/10)//2):
            x_draw.append(i)

    y_draw = []
    A = pos_y_f - pos_y

    if int((A)/10+1)%3 == 0:
        for i in range(0,int((A)/10+1)//3):
            y_draw.append(i)
    else:
        for i in range(0,int((A)/10)//3):
            y_draw.append(i)

    z_draw = []
    for i in range(0,int((col_height)/10)):
        z_draw.append(i)

    b1_l = []
    for k in z_draw:
        for j in y_draw:
            for i in x_draw:
                b1_aux = init_block  + (k) * (limites_x[3] * limites_y[3]) + (j) * 3 * limites_x[3] + (i) * 2 
                b1_l.append(b1_aux)
    

    DP = []
    aux = 0
    for j in y_draw:
        list_aux = []
        for i in x_draw:
            list_aux.append(aux)
            aux += 1
        DP.append(list_aux)

    ## DP es de la forma = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 
    #                      [20, 21, 22, 23, 24, 25, 26, 27, 28, 29], [30, 31, 32, 33, 34, 35, 36, 37, 38, 39], 
    #                      [40, 41, 42, 43, 44, 45, 46, 47, 48, 49], [50, 51, 52, 53, 54, 55, 56, 57, 58, 59]]
    
    
    
    #########################################################
    ###                                                  ####
    ### Donde los drawpoints están presentados asi       ####
    ###                                                  ####
    #########################################################
    ###                                                  ####
    ###  0   1   2   3   4   5   6   7   8   9           ####
    ###  10  11  12  13  14  15  16  17  18  19          ####
    ###  20  21  22  23  24  25  26  27  28  29          ####
    ###  30  31  32  33  34  35  36  37  38  39          ####
    ###  40  41  42  43  44  45  46  47  48  49          ####
    ###  50  51  52  53  54  55  56  57  58  59          ####
    ###  60  61  62  63  64  65  66  67  68  69          ####
    ###                                                  ####
    #########################################################
    
    list_aux = []
    drawpoint = []
    aux = 0
    for j in y_draw:
        for i in x_draw:
            drawpoint.append(aux)
            aux += 1
    
    T_d_1 = []
    Q_d_1 = []#Tonnelage of mineral
    q_d_1 = []
    c_pd_1 = []
    c_md_1 = []
    for i in b1_l:
        Td_aux = 0
        Qd_aux = 0
        qd_aux = 0
        cpd_aux = 0
        cmd_aux = 0
        b1 = int(i)
        b2 = int(b1 + 1)
        b3 = int(i + limites_y[3] + 1)
        b4 = int(b3 + 1)
        b5 = int(b3 + limites_y[3] + 1)
        b6 = int(b5 + 1)
        Td_aux += (TON[b1] + TON[b2] + TON[b3] + TON[b4] + TON[b5] + TON[b6])
        cpd_aux += (CP_S[b1] + CP_S[b2] + CP_S[b3] + CP_S[b4] + CP_S[b5] + CP_S[b6])/6
        cmd_aux += (CM_S[b1] + CM_S[b2] + CM_S[b3] + CM_S[b4] + CM_S[b5] + CM_S[b6])/6
        Qd_aux += (MIN[b1] + MIN[b2] + MIN[b3] + MIN[b4] + MIN[b5] + MIN[b6])
        if Td_aux == 0:
            qd_aux = 0
        else:
            qd_aux += (TON[b1] * LEY[b1] + TON[b2] * LEY[b2] + TON[b3] * LEY[b3] +
                      TON[b4] * LEY[b4] + TON[b5] * LEY[b5] + TON[b6] * LEY[b6]) / Td_aux
        T_d_1.append(Td_aux)
        Q_d_1.append(Qd_aux)
        q_d_1.append(qd_aux)
        c_pd_1.append(cpd_aux)
        c_md_1.append(cmd_aux)

    aux = int(len(T_d_1)/len(drawpoint))
    b_drawpoint = []
    for i in range(len(drawpoint)):
        aux_list = []
        for k in range(aux):
            aux_list.append(len(drawpoint)*k+i)
        b_drawpoint.append(aux_list)

    T_d = []
    Q_d = []
    q_d = [] #
    c_pd = []
    c_md = []

    for i in b_drawpoint:
        Td_aux = 0
        Qd_aux = 0
        qd_aux = 0
        cpd_aux = 0
        cmd_aux = 0
        for j in i:
            Td_aux += T_d_1[j]
            Qd_aux += Q_d_1[j]
            qd_aux += q_d_1[j]*T_d_1[j]
            cpd_aux += c_pd_1[j]
            cmd_aux += c_md_1[j]
        T_d.append(Td_aux)
        Q_d.append(Qd_aux)
        q_d.append(qd_aux/Td_aux)
        c_pd.append(cpd_aux/len(b_drawpoint[0]))
        c_md.append(cmd_aux/len(b_drawpoint[0]))
        
    #########################################################
    ###                                                  ####
    ### Acá se empieza a calcular el drawpoint predecesor####
    ###                                                  ####
    #########################################################
    
    
    DP_pred = []
    


    
    #########################################################
    ###                                                  ####
    ### Orientación 1:                                   ####
    ###   De la derecha superior a la izquierda inferior ####
    ###       #####    ######     ######    ######       ####
    ###                                                  ####
    ###   Orden:                                         ####
    ###      9 - 8 - 19 - 7 - 18 - 29 - 6 - 17 - 28- 39  ####
    ###                                                  ####
    ###        Y así continuar con eso                   ####
    ###                                                  ####
    #########################################################       
    ###                                                  ####
    ### Para conseguir esto se debe cambiar el orden     ####
    ### Como se hará a continuación (opción 1)           ####
    ###                                                  ####
    #########################################################
    
    
    if orientacion == 1:
        print('Los drawpoints saldrán orientados de derecha superior a la izquierda inferior')
        for i in range(len(DP)):
            DP[i].sort(reverse = True)
        
    #########################################################
    ###                                                  ####
    ### Orientación 2:                                   ####
    ###   De la izquierda inferior a la derecha superior ####
    ###       #####    ######     ######    ######       ####
    ###                                                  ####
    ###   Orden:                                         ####
    ###      60 - 61 - 50 - 62 - 51 - 40 - 63 - 52       ####
    ###                                                  ####
    ###        Y así continuar con eso                   ####
    ###                                                  ####
    #########################################################
    ###                                                  ####
    ### Para conseguir esto se debe cambiar el orden     ####
    ### Como se hará a continuación (opción 2)           ####
    ###                                                  ####
    #########################################################
    
    elif orientacion == 2:
        print('Los drawpoints saldrán orientados de izquierda inferior a la derecha superior')
        DP.sort(reverse = True)
        
    #########################################################
    ###                                                  ####
    ### Orientación 3:                                   ####
    ###   De la derecha inferior a la izquierda superior ####
    ###       #####    ######     ######    ######       ####
    ###                                                  ####
    ###   Orden:                                         ####
    ###      69 - 68 - 59 - 67 - 58 - 49 - 66 - 57       ####
    ###                                                  ####
    ###        Y así continuar con eso                   #### 
    ###                                                  ####
    #########################################################
    ###                                                  ####
    ### Para conseguir esto se debe cambiar el orden     ####
    ### Como se hará a continuación (opción 3)           ####
    ###                                                  ####
    #########################################################

    elif orientacion == 3:
        print('Los drawpoints saldrán orientados de derecha inferior a la izquierda superior')
        DP.sort(reverse = True)
        
        for i in range(len(DP)):
            DP[i].sort(reverse = True)
    
    
    #########################################################
    ###                                                  ####
    ### Orientación 0:                                   ####
    ###   De la izquierda superior a la derecha inferior ####
    ###       #####    ######     ######    ######       ####
    ###                                                  ####
    ###   Orden:                                         ####
    ###      0 - 1 - 10 - 2 - 11 - 20 - 3 - 12 - 21- 30  ####
    ###                                                  ####
    ###        Y así continuar con eso                   ####
    ###                                                  ####
    #########################################################
    ###                                                  ####
    ### Acá no hay cambio de nada     (opción 0)         ####
    ###                                                  ####
    #########################################################

    elif orientacion == 0:
        pass
    
    elif orientacion != (1 or 2 or 3):
        print('Debe seleccionar la opción 0, 1, 2 o 3, los resultados saldrán como la opción 0')    
        print('Los drawpoints saldrán orientados de izquierda superior a la derecha inferior')
        
    lista_a_eliminar = DP.copy()
    columnas_dp = len(lista_a_eliminar[0]) ## En este caso sería de 10 en el ejemplo (drawpoints eje X)
    filas_dp = len(lista_a_eliminar) ## En este caso sería de 7 en el ejemplo (drawpoints eje Y)
    aux_fil = 1
    
    
    
    ### Lo que se hará es ordenar en el eje X todas los drawpoints al revés
    for i in range(columnas_dp + filas_dp):
        for j in range(aux_fil):
            if lista_a_eliminar[j] != []:
                DP_pred.append(lista_a_eliminar[j].pop(0))
        if aux_fil != filas_dp:
            aux_fil += 1
              
    predecessor =list()
    for i in range(len(DP_pred)-1):
        lista_aux = list()
        lista_aux.append(DP_pred[i+1])
        lista_aux.append(DP_pred[i])
        predecessor.append(lista_aux)

    return (drawpoint, T_d, Q_d, q_d, c_pd, c_md, predecessor, x_draw, y_draw, z_draw)
