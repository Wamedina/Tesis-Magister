def integratedModel(bloques_CA,drawpoint,cord_z_C,dif_centroide,pos_z,col_height,cota_seg,predecessor_block,predecessor,
                             TON_C,MIN_C,REC_C,LEY_C,CM_CA_C,CP_CA_C,
                             TON_d,MIN_D,REC,LEY_D,C_P_D,C_M_D,
                             t_C,RMu_t,RMl_t,RPu_t,RPl_t,qu_t,ql_t,time_max_C,
                             t_S,MU_mt,ML_mt,MU_pt,ML_pt,qU_dt,qL_dt,A_d,NU_nt,NL_nt,N_t,RL_dt,RU_dt,time_max_S,
                             GAP,precio,costo_mina_ponderador,costo_planta_ponderador):
    
    import gurobipy   as     gp
    from   gurobipy   import GRB
    
    modelo_integrado = gp.Model(name = 'Modelo Integrado')
    
    # Open Pit
    x_bt_OP_I = modelo_integrado.addVars(t_C, bloques_CA, vtype=GRB.BINARY, name="x")

    # Underground  Model
    x_dt_S_I = modelo_integrado.addVars(drawpoint, t_S, vtype=GRB.BINARY, name="x")
    y_dt_S_I = modelo_integrado.addVars(drawpoint, t_S, vtype=GRB.CONTINUOUS, name="y")
    z_dt_S_I = modelo_integrado.addVars(drawpoint, t_S, vtype=GRB.BINARY, name="z")
    
    rest_cota = modelo_integrado.addConstrs((x_bt_OP_I[ti, b]*(cord_z_C[b] - dif_centroide - pos_z - col_height - cota_seg) 
                                             >= 0 for b in bloques_CA for ti in t_C), "Cota")
    
    Ton_Up  = modelo_integrado.addConstrs((gp.quicksum(x_bt_OP_I[ti, b]*TON_C[b] for b in bloques_CA) 
                            <= RMu_t[ti] for ti in t_C), "Ton_max")
    Ton_low = modelo_integrado.addConstrs((gp.quicksum(x_bt_OP_I[ti, b]*TON_C[b] for b in bloques_CA) 
                                >= RMl_t[ti] for ti in t_C), "Ton_min")
    Mat_Up_OP = modelo_integrado.addConstrs((gp.quicksum(x_bt_OP_I[ti, b]*MIN_C[b] for b in bloques_CA) <= 
                               RPu_t[ti] for ti in t_C), "Mat_max")
    Mat_low_OP = modelo_integrado.addConstrs((gp.quicksum(x_bt_OP_I[ti, b]*MIN_C[b] for b in bloques_CA) >= 
                                RPl_t[ti] for ti in t_C), "Mat_min")
    BLOCK_SUP_OP = modelo_integrado.addConstrs((gp.quicksum(x_bt_OP_I[m, predecessor_block[l][0]]*(time_max_C-m+1) for m in t_C)
                                                <=  gp.quicksum(x_bt_OP_I[m, predecessor_block[l][1]]*(time_max_C-m+1)
                                                                for m in t_C)  for l in range(len(predecessor_block))),
                                               "Superior_Block")
    
    Reserve_cons_OP = modelo_integrado.addConstrs((gp.quicksum(x_bt_OP_I[ti, b] for ti in t_C) <= 1 for b in bloques_CA), 
                               "Reserve_cons")
    GQC_Up_OP = modelo_integrado.addConstrs((gp.quicksum(x_bt_OP_I[ti, b]*TON_C[b]*LEY_C[b] for b in bloques_CA) <=
                              qu_t[ti] * gp.quicksum(x_bt_OP_I[ti, b]*TON_C[b] for b in bloques_CA) for ti in t_C), 
                               "GQC_Up")

    GQC_low_OP = modelo_integrado.addConstrs((gp.quicksum(x_bt_OP_I[ti, b]*TON_C[b]*LEY_C[b] for b in bloques_CA) >=
                              ql_t[ti] * gp.quicksum(x_bt_OP_I[ti, b]*TON_C[b] for b in bloques_CA) for ti in t_C), 
                               "GQC_Up")
    Ton_Up = modelo_integrado.addConstrs((gp.quicksum(y_dt_S_I[d, ti]*TON_d[d] for d in drawpoint) <= MU_mt[ti] for ti in t_S),
                                         "Min_max")
    
    Ton_low = modelo_integrado.addConstrs((gp.quicksum(y_dt_S_I[d, ti]*TON_d[d] for d in drawpoint) >= ML_mt[ti] for ti in t_S),
                                          "Min_min")

    Mat_Up = modelo_integrado.addConstrs((gp.quicksum(y_dt_S_I[d, ti]* MIN_D[d] for d in drawpoint) <= MU_pt[ti] for ti in t_S),
                                         "Mat_max")

    Mat_low = modelo_integrado.addConstrs((gp.quicksum(y_dt_S_I[d, ti]* MIN_D[d] for d in drawpoint) >= ML_pt[ti] for ti in t_S)
                                          , "Mat_min")

    GQC_Up = modelo_integrado.addConstrs((gp.quicksum(y_dt_S_I[d, ti]*LEY_D[d]*TON_d[d] for d in drawpoint) <=
                               qU_dt[ti] * gp.quicksum(TON_d[d]*y_dt_S_I[d, ti] for d in drawpoint) for ti in t_S), "GQC_Up")

    GQC_low = modelo_integrado.addConstrs((gp.quicksum(y_dt_S_I[d, ti]*LEY_D[d]*TON_d[d] for d in drawpoint) >=
                               qL_dt[ti] * gp.quicksum(TON_d[d]*y_dt_S_I[d, ti] for d in drawpoint) for ti in t_S), "GQC_low")

    DP_Sup = modelo_integrado.addConstrs((gp.quicksum(x_dt_S_I[predecessor[l][0], m]*(max(t_S)-m+1) for m in t_S) <=
                                  gp.quicksum(x_dt_S_I[predecessor[l][1], m]*(max(t_S)-m+1) for m in t_S)  
                                  for l in range(len(predecessor))), "DP_Sup")

    Drawp_init = modelo_integrado.addConstrs((gp.quicksum(x_dt_S_I[d, ti] for ti in t_S) <= 1 for d in drawpoint), "Drawp_init")

    ## Lo que hace Drawpextract_61, es forzar a que solamente se puede extraer un drawpoint una vez que se activo
    Drawpextract_61 = modelo_integrado.addConstrs((gp.quicksum(x_dt_S_I[d, tau] for tau in range(ti+1)) >= z_dt_S_I[d, ti]  
                                        for d in drawpoint for ti in t_S), "Drawpextract_61")

    ## Un drawpoint solamente puede ser extraido por un preiodo pre determinado (A_d)
    Drawpextract_62 = modelo_integrado.addConstrs((gp.quicksum(z_dt_S_I[d, ti] for ti in t_S)  <= A_d[ti]  for d in drawpoint
                                                   for ti in t_S), "Drawp_62")

    ## Una vez se inicia extrayendo de un drawpoint, se continua extrayendo sin interrupción
    Drawpextract_63 = modelo_integrado.addConstrs((A_d[ti] *(z_dt_S_I[d, ti] - z_dt_S_I[d, ti+1]) 
                                        - gp.quicksum(z_dt_S_I[d, tau] for tau in range(ti+1)) <= 0 
                                        for d in drawpoint for ti in range(0,max(t_S))), "Drawpextract_63")

    ## El número de nuevos drawpoints debe tener un limite superior
    Drawpextract_64_1 = modelo_integrado.addConstrs((gp.quicksum(x_dt_S_I[d, ti] for d in drawpoint) <= NU_nt[ti] for ti 
                                                     in t_S)
                                                    ,"Drawpextract_64_1")

    ## El número de nuevos drawpoints debe tener un limite inferior
    Drawpextract_64_2 = modelo_integrado.addConstrs((gp.quicksum(x_dt_S_I[d, ti] for d in drawpoint) >= NL_nt[ti] for ti 
                                                     in t_S)
                                                    , "Drawpextract_64_2")

    ## El número de nuevos drawpoints debe tener un limite inferior respecto al origen
    Drawpextract_64_3 = modelo_integrado.addConstrs((gp.quicksum(x_dt_S_I[d, ti] for d in drawpoint) <= NU_nt[0] for ti 
                                                     in t_S)
                                                    ,"Drawpextract_64_3")

    ## El número máximo de drawpoints siendo extraidos simultáneamente en un periodo debe tener un límite
    Drawpextract_65 = modelo_integrado.addConstrs((gp.quicksum(z_dt_S_I[d, ti] for d in drawpoint) <= N_t[ti] for ti in t_S)
                                                  , "Drawpextract_65")

    ## El porcentaje de tonelaje extraido es cero si el drawpoint no es extraido en el periodo
    Drawpextract_66 = modelo_integrado.addConstrs((y_dt_S_I[d, ti] <= z_dt_S_I[d, ti] for d in drawpoint for ti in t_S),
                                                  "Drawpextract_66")

    ## Extracción mínima constante a extraer (RL_dt es el ratio mínimo de extracción en el periodo t)
    Drawpextract_67_1 = modelo_integrado.addConstrs((RL_dt[ti] * z_dt_S_I[d, ti]  <= y_dt_S_I[d, ti] for d in drawpoint
                                                     for ti in t_S), "Drawpextract_67_1")

    Reserver_cnst = modelo_integrado.addConstrs((gp.quicksum(y_dt_S_I[d, ti] for ti in t_S) <= 1 for d in drawpoint),
                                                "Reserver_cnst")

    restricion_partida_1 = modelo_integrado.addConstr(x_dt_S_I[predecessor[0][0],0] == 1, "restriccion_partida 1")

    ## Lo mínimo a extraer en el primer drawpoint es de 0.3 
    restricion_partida_2 = modelo_integrado.addConstr(y_dt_S_I[predecessor[0][0],0] >= 0.3, "restriccion_partida 2")

    ## Se debe extraer un mínimo de un 90% de cada drawpoint
    restricion_partida_E =modelo_integrado.addConstrs((gp.quicksum(y_dt_S_I[d, ti]*z_dt_S_I[d, ti] for ti in t_S) >= 0.8
                                                       for d in drawpoint), "Reserver_cnst")

    ## Los drawpoints se extraen en orden (es decir que el z anterior debe estar activo para que el siguiente lo esté)
    restricion_z_dt = modelo_integrado.addConstrs((gp.quicksum(z_dt_S_I[predecessor[l][0], m]*(max(t_S)-m+1) for m in t_S) <=
                                  gp.quicksum(z_dt_S_I[predecessor[l][1], m]*(max(t_S)-m+1) for m in t_S)  
                                  for l in range(len(predecessor))), "DP_Sup")

    
    FO_OP_Int = gp.quicksum(x_bt_OP_I[ti, b]*((((0.7*precio*LEY_C[b]-CP_CA_C[b]*costo_planta_ponderador)*MIN_C[b])-(CM_CA_C[b]*costo_mina_ponderador*TON_C[b]))/
                                              ((1+0.1)**t_C[ti])) for ti in t_C for b in bloques_CA)

    FO_S_Int = gp.quicksum(y_dt_S_I[d, ti]*((((0.7*precio*LEY_D[d]-C_P_D[d]*costo_planta_ponderador)*MIN_D[d])-(C_M_D[d]*costo_mina_ponderador*TON_d[d]))/
                                            ((1+0.1)**(t_S[ti]+time_max_C))) for ti in t_S for d in drawpoint)

    FO_Int = FO_OP_Int + FO_S_Int
    
    modelo_integrado.setObjective(FO_Int, GRB.MAXIMIZE)
    modelo_integrado.Params.MIPGap = GAP
    
    modelo_integrado.optimize()
    
    # Saca los valores de la solución
    lista_variable_Integrado = (modelo_integrado.getAttr(GRB.Attr.X, modelo_integrado.getVars()))
    solucion = modelo_integrado.objVal
    runtime = modelo_integrado.Runtime
    gap_f = modelo_integrado.MIPGap
    
    return solucion, lista_variable_Integrado, runtime, gap_f

