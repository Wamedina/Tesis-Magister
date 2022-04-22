from   gurobipy   import GRB
import gurobipy   as     gp
    

def openPitModel(bloques_CA,predecessor_block,
                             TON_C,MIN_C,LEY_C,CM_CA_C,CP_CA_C,
                             t_C,RMu_t,RMl_t,RPu_t,RPl_t,qu_t,ql_t,time_max_C,
                             GAP,precio):
    
    openPitModel = gp.Model(name = 'Open Pit Model')
    x_bt_OP = openPitModel.addVars(t_C, bloques_CA, vtype=GRB.BINARY, name="x")
    Ton_Up  = openPitModel.addConstrs((gp.quicksum(x_bt_OP[ti, b]*TON_C[b] for b in bloques_CA) 
                            <= RMu_t[ti] for ti in t_C), "Ton_max")
    Ton_low = openPitModel.addConstrs((gp.quicksum(x_bt_OP[ti, b]*TON_C[b] for b in bloques_CA) 
                            >= RMl_t[ti] for ti in t_C), "Ton_min")
    Mat_Up_OP = openPitModel.addConstrs((gp.quicksum(x_bt_OP[ti, b]*MIN_C[b] for b in bloques_CA) <= 
                           RPu_t[ti] for ti in t_C), "Mat_max")
    Mat_low_OP = openPitModel.addConstrs((gp.quicksum(x_bt_OP[ti, b]*MIN_C[b] for b in bloques_CA) >= 
                            RPl_t[ti] for ti in t_C), "Mat_min")
    BLOCK_SUP_OP = openPitModel.addConstrs((gp.quicksum(x_bt_OP[m, predecessor_block[l][0]]*(time_max_C-m+1) for m in t_C) <= 
                                 gp.quicksum(x_bt_OP[m, predecessor_block[l][1]]*(time_max_C-m+1) for m in t_C)  
                              for l in range(len(predecessor_block))), "Superior_Block")
    Reserve_cons_OP = openPitModel.addConstrs((gp.quicksum(x_bt_OP[ti, b] for ti in t_C) <= 1 for b in bloques_CA), 
                           "Reserve_cons")
    GQC_Up_OP = openPitModel.addConstrs((gp.quicksum(x_bt_OP[ti, b]*TON_C[b]*LEY_C[b] for b in bloques_CA) <=
                          qu_t[ti] * gp.quicksum(x_bt_OP[ti, b]*TON_C[b] for b in bloques_CA) for ti in t_C), 
                           "GQC_Up")

    GQC_low_OP = openPitModel.addConstrs((gp.quicksum(x_bt_OP[ti, b]*TON_C[b]*LEY_C[b] for b in bloques_CA) >=
                          ql_t[ti] * gp.quicksum(x_bt_OP[ti, b]*TON_C[b] for b in bloques_CA) for ti in t_C), 
                           "GQC_LOW")
    
    FO_OP = gp.quicksum(x_bt_OP[ti, b]*((((0.7*precio*LEY_C[b]-CP_CA_C[b])*MIN_C[b])-(CM_CA_C[b]*TON_C[b]))/((1+0.1)**t_C[ti]))
                 for ti in t_C for b in bloques_CA)
    
    openPitModel.setObjective(FO_OP, GRB.MAXIMIZE)
    openPitModel.Params.TimeLimit = 1000
    #openPitModel.Params.MIPGap = 0.20
    openPitModel.Params.MIPGap = GAP    
    openPitModel.optimize()
    lista_variable_CA = openPitModel.getAttr(GRB.Attr.X)

    solucion = openPitModel.objVal    
    return solucion, lista_variable_CA