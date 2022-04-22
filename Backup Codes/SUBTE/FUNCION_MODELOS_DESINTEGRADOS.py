#!/usr/bin/env python
# coding: utf-8

# In[1]:


def FUNCION_MODELO_CIELO(bloques_CA,predecessor_block,
                             TON_C,MIN_C,REC_C,LEY_C,CM_CA_C,CP_CA_C,
                             t_C,RMu_t,RMl_t,RPu_t,RPl_t,qu_t,ql_t,time_max_C,
                             GAP,precio,costo_mina_ponderador,costo_planta_ponderador):
    
    import gurobipy   as     gp
    from   gurobipy   import GRB
    
    model_CA = gp.Model(name = 'Modelo Cielo Abierto')
    x_bt_OP = model_CA.addVars(t_C, bloques_CA, vtype=GRB.BINARY, name="x")
    Ton_Up  = model_CA.addConstrs((gp.quicksum(x_bt_OP[ti, b]*TON_C[b] for b in bloques_CA) 
                            <= RMu_t[ti] for ti in t_C), "Ton_max")
    Ton_low = model_CA.addConstrs((gp.quicksum(x_bt_OP[ti, b]*TON_C[b] for b in bloques_CA) 
                            >= RMl_t[ti] for ti in t_C), "Ton_min")
    Mat_Up_OP = model_CA.addConstrs((gp.quicksum(x_bt_OP[ti, b]*MIN_C[b] for b in bloques_CA) <= 
                           RPu_t[ti] for ti in t_C), "Mat_max")
    Mat_low_OP = model_CA.addConstrs((gp.quicksum(x_bt_OP[ti, b]*MIN_C[b] for b in bloques_CA) >= 
                            RPl_t[ti] for ti in t_C), "Mat_min")
    BLOCK_SUP_OP = model_CA.addConstrs((gp.quicksum(x_bt_OP[m, predecessor_block[l][0]]*(time_max_C-m+1) for m in t_C) <= 
                                 gp.quicksum(x_bt_OP[m, predecessor_block[l][1]]*(time_max_C-m+1) for m in t_C)  
                              for l in range(len(predecessor_block))), "Superior_Block")
    Reserve_cons_OP = model_CA.addConstrs((gp.quicksum(x_bt_OP[ti, b] for ti in t_C) <= 1 for b in bloques_CA), 
                           "Reserve_cons")
    GQC_Up_OP = model_CA.addConstrs((gp.quicksum(x_bt_OP[ti, b]*TON_C[b]*LEY_C[b] for b in bloques_CA) <=
                          qu_t[ti] * gp.quicksum(x_bt_OP[ti, b]*TON_C[b] for b in bloques_CA) for ti in t_C), 
                           "GQC_Up")

    GQC_low_OP = model_CA.addConstrs((gp.quicksum(x_bt_OP[ti, b]*TON_C[b]*LEY_C[b] for b in bloques_CA) >=
                          ql_t[ti] * gp.quicksum(x_bt_OP[ti, b]*TON_C[b] for b in bloques_CA) for ti in t_C), 
                           "GQC_LOW")
    
    FO_OP = gp.quicksum(x_bt_OP[ti, b]*((((0.7*precio*LEY_C[b]-CP_CA_C[b]*costo_planta_ponderador)*MIN_C[b])-(CM_CA_C[b]*costo_mina_ponderador*TON_C[b]))/((1+0.1)**t_C[ti]))
                 for ti in t_C for b in bloques_CA)
    
    model_CA.setObjective(FO_OP, GRB.MAXIMIZE)
    ## Momentaneo
    model_CA.Params.TimeLimit = 36000
    #model_CA.Params.MIPGap = 0.20
    model_CA.Params.MIPGap = GAP    
    model_CA.optimize()
    lista_variable_CA = model_CA.getAttr(GRB.Attr.X)

    solucion = model_CA.objVal
    runtime = model_CA.Runtime
    gap_f = model_CA.MIPGap
    return solucion, lista_variable_CA,runtime,gap_f


# In[ ]:


def FUNCION_SUBTE(drawpoint,col_height,predecessor,
                             TON_d,MIN_D,REC,LEY_D,C_P_D,C_M_D,
                             t_S,MU_mt,ML_mt,MU_pt,ML_pt,qU_dt,qL_dt,A_d,NU_nt,NL_nt,N_t,RL_dt,RU_dt,time_max_S,
                             GAP,precio,costo_mina_ponderador,costo_planta_ponderador):
    
    import gurobipy   as     gp
    from   gurobipy   import GRB
    
    model_S = gp.Model(name = 'Modelo Subterráneo')
    x_dt_S = model_S.addVars(drawpoint, t_S, vtype=GRB.BINARY, name="x")
    y_dt_S = model_S.addVars(drawpoint, t_S, vtype=GRB.CONTINUOUS, name="y")
    z_dt_S = model_S.addVars(drawpoint, t_S, vtype=GRB.BINARY, name="z")
    
    Ton_Up = model_S.addConstrs((gp.quicksum(y_dt_S[d, ti]*TON_d[d] for d in drawpoint) <= MU_mt[ti] for ti in t_S), "Min_max")
    
    Ton_low = model_S.addConstrs((gp.quicksum(y_dt_S[d, ti]*TON_d[d] for d in drawpoint) >= ML_mt[ti] for ti in t_S), "Min_min")
    
    Mat_Up = model_S.addConstrs((gp.quicksum(y_dt_S[d, ti]* MIN_D[d] for d in drawpoint) <= MU_pt[ti] for ti in t_S), "Mat_max")
    
    Mat_low = model_S.addConstrs((gp.quicksum(y_dt_S[d, ti]* MIN_D[d] for d in drawpoint) >= ML_pt[ti] for ti in t_S), "Mat_min")
    
    GQC_Up = model_S.addConstrs((gp.quicksum(y_dt_S[d, ti]*LEY_D[d]*TON_d[d] for d in drawpoint) <=
                           qU_dt[ti] * gp.quicksum(TON_d[d]*y_dt_S[d, ti] for d in drawpoint) for ti in t_S), "GQC_Up")
    
    GQC_low = model_S.addConstrs((gp.quicksum(y_dt_S[d, ti]*LEY_D[d]*TON_d[d] for d in drawpoint) >=
                           qL_dt[ti] * gp.quicksum(TON_d[d]*y_dt_S[d, ti] for d in drawpoint) for ti in t_S), "GQC_low")
    
    DP_Sup = model_S.addConstrs((gp.quicksum(x_dt_S[predecessor[l][0], m]*(max(t_S)-m+1) for m in t_S) <=
                              gp.quicksum(x_dt_S[predecessor[l][1], m]*(max(t_S)-m+1) for m in t_S)  
                              for l in range(len(predecessor))), "DP_Sup")
    
    Drawp_init = model_S.addConstrs((gp.quicksum(x_dt_S[d, ti] for ti in t_S) <= 1 for d in drawpoint), "Drawp_init")
    
    
    

    ## Lo que hace Drawpextract_61, es forzar a que solamente se puede extraer un drawpoint una vez que se activo
    Drawpextract_61 = model_S.addConstrs((gp.quicksum(x_dt_S[d, tau] for tau in range(ti+1)) >= z_dt_S[d, ti]  
                                        for d in drawpoint for ti in t_S), "Drawpextract_61")
    
    ## Un drawpoint solamente puede ser extraido por un periodo pre determinado (A_d)
    Drawpextract_62 = model_S.addConstrs((gp.quicksum(z_dt_S[d, ti] for ti in t_S)  <= A_d[ti]  for d in drawpoint for ti in t_S),                                        "Drawp_62")
    
    ## Una vez se inicia extrayendo de un drawpoint, se continua extrayendo sin interrupción
    Drawpextract_63 = model_S.addConstrs((A_d[ti] *(z_dt_S[d, ti] - z_dt_S[d, ti+1]) 
                                        - gp.quicksum(z_dt_S[d, tau] for tau in range(ti+1)) <= 0 
                                        for d in drawpoint for ti in range(0,max(t_S))), "Drawpextract_63")
  
    
    
    ## El número de nuevos drawpoints debe tener un limite superior
    Drawpextract_64_1 = model_S.addConstrs((gp.quicksum(x_dt_S[d, ti] for d in drawpoint) <= NU_nt[ti] for ti in t_S),                                              "Drawpextract_64_1")

    ## El número de nuevos drawpoints debe tener un limite inferior
    Drawpextract_64_2 = model_S.addConstrs((gp.quicksum(x_dt_S[d, ti] for d in drawpoint) >= NL_nt[ti] for ti in t_S),                                              "Drawpextract_64_2")


    ## El número de nuevos drawpoints debe tener un limite inferior respecto al origen
    Drawpextract_64_3 = model_S.addConstrs((gp.quicksum(x_dt_S[d, ti] for d in drawpoint) <= NU_nt[0] for ti in t_S),                                              "Drawpextract_64_3")

    ## El número máximo de drawpoints siendo extraidos simultáneamente en un periodo debe tener un límite
    Drawpextract_65 = model_S.addConstrs((gp.quicksum(z_dt_S[d, ti] for d in drawpoint) <= N_t[ti] for ti in t_S), "Drawpextract_65")
    '''
    '''
    ## El porcentaje de tonelaje extraido es cero si el drawpoint no es extraido en el periodo
    Drawpextract_66 = model_S.addConstrs((y_dt_S[d, ti] <= z_dt_S[d, ti] for d in drawpoint for ti in t_S),"Drawpextract_66")

    ## Extracción mínima constante a extraer (RL_dt es el ratio mínimo de extracción en el periodo t)
    Drawpextract_67_1 = model_S.addConstrs((RL_dt[ti] * z_dt_S[d, ti]  <= y_dt_S[d, ti] for d in drawpoint for ti in t_S),                                           "Drawpextract_67_1")
        
    Reserver_cnst = model_S.addConstrs((gp.quicksum(y_dt_S[d, ti] for ti in t_S) <= 1 for d in drawpoint), "Reserver_cnst")  
    
    ## Se debe partir si o si por este nodo
    restricion_partida_1 = model_S.addConstr(x_dt_S[predecessor[0][1],0] == 1, "restriccion_partida 1")

    ## Lo mínimo a extraer en el primer drawpoint es de 0.3 
    restricion_partida_2 = model_S.addConstr(y_dt_S[predecessor[0][0],0] >= 0.3, "restriccion_partida 2")
    
    ## Se debe extraer un mínimo de un 90% de cada drawpoint
    restricion_partida_E =model_S.addConstrs((gp.quicksum(y_dt_S[d, ti]*z_dt_S[d, ti] for ti in t_S) >= 0.8 for d in drawpoint), "Reserver_cnst")
    
    
    
    ## Los drawpoints se extraen en orden (es decir que el z anterior debe estar activo para que el siguiente lo esté)
    restricion_z_dt = model_S.addConstrs((gp.quicksum(z_dt_S[predecessor[l][0], m]*(max(t_S)-m+1) for m in t_S) <=
                                  gp.quicksum(z_dt_S[predecessor[l][1], m]*(max(t_S)-m+1) for m in t_S)  
                                  for l in range(len(predecessor))), "DP_Sup")
    
    
    
    FO_S = gp.quicksum(y_dt_S[d, ti]*((((0.7*precio*LEY_D[d]-C_P_D[d]*costo_planta_ponderador)*MIN_D[d])-(C_M_D[d]*costo_mina_ponderador*TON_d[d]))/((1+0.1)**(t_S[ti])))
                 for ti in t_S for d in drawpoint)
    
    model_S.setObjective(FO_S, GRB.MAXIMIZE)
    
    model_S.write('model_m.mps')
    model_S.write('model_r.rew')
    model_S.write('model_l.lp')
    model_S.write('model_rlp.rlp')
    
    model_S.Params.MIPGap = GAP
    model_S.Params.TimeLimit = 36000
    model_S.optimize()
    lista_variable_S = (model_S.getAttr(GRB.Attr.X, model_S.getVars()))  

    solucion = model_S.objVal
    runtime = model_S.Runtime
    gap_f = model_S.MIPGap
    return solucion, lista_variable_S, runtime, gap_f

