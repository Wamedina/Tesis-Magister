import pandas as pd
import gurobipy   as     gp
from   gurobipy   import GRB
from globalFunctions import getNumberOfBlocksInADimension
from openPitModel import *
from openPitFunctions import finalBlock
from globalFunctions import getNumberOfBlocksInADimension
from plotResults   import plotResults
from drawpointFunction  import drawpointFunction


class IntegratedModel:
    def __init__(self, undergroundMineDataframe, openMineDataframe, numberOfPeriods):
        self.openMineDataframe = openMineDataframe
        self.undergroundMineDataframe = undergroundMineDataframe
        self.numberOfPeriods = numberOfPeriods

    def execute(self):
        self.setOpenPitVariables()
        self.setUndergroundVariables()
        self.setMineLimits()
        self.getBlockInfo()
        self.setParametersToEvaluate()
        self.setGlobalParameters()
        self.getUndergroundVariables()
        self.setModelAndGetResults()  
        return self.objValue, self.variableValues, self.runtime, self.gap  

    def setOpenPitVariables(self):
        self.openPitBlocksLenght = self.openMineDataframe['X'].to_dict() 
        self.openPitBlocksWidth = self.openMineDataframe['Y'].to_dict() 
        self.openPitBlocksHeight = self.openMineDataframe['Z'].to_dict() 
        self.openPitBlockTonnage = self.openMineDataframe['Ton'].to_dict() 
        self.openPitBlockMineral = self.openMineDataframe['Mineral'].to_dict()
        self.openPitBlockRecovery = self.openMineDataframe['Recuperación'].to_dict() 
        self.openPitCopperLaw = self.openMineDataframe['%Cu'].to_dict()
        self.openPitExtractionFixedCosts = self.openMineDataframe['CPlanta CA'].to_dict()
        self.openPitVariableExtractionCosts = self.openMineDataframe['CMina CA'].to_dict()
      
    def setUndergroundVariables(self):
        self.undergroundBlocksLenght = self.undergroundMineDataframe['X'].to_dict()             
        self.undergroundBlocksWidth  = self.undergroundMineDataframe['Y'].to_dict()             
        self.undergroundBlocksHeight = self.undergroundMineDataframe['Z'].to_dict()             
        self.undergroundBlockTonnage = self.undergroundMineDataframe['Ton'].to_dict()              
        self.undergroundBlockMineral  = self.undergroundMineDataframe['Mineral'].to_dict()          
        self.undergroundBlockRecovery  = self.undergroundMineDataframe['Recuperación'].to_dict()     
        self.undergroundCopperLaw  = self.undergroundMineDataframe['%Cu'].to_dict()
        self.undergroundExtractionFixedCosts = self.undergroundMineDataframe['CPlanta CA'].to_dict()
        self.undergroundVariableExtractionCosts = self.undergroundMineDataframe['CMina CA'].to_dict()
        self.undergroundCP_S = self.undergroundMineDataframe['CPlanta S'].to_dict()
        self.undergroundCM_S = self.undergroundMineDataframe['CMINA S'].to_dict() 

    def setMineLimits(self):
        self.undergroundBlocksLenghtLimits = getNumberOfBlocksInADimension(self.undergroundBlocksLenght)
        self.undergroundBlocksWidthLimits = getNumberOfBlocksInADimension(self.undergroundBlocksWidth)
        self.undergroundBlocksHeightLimits = getNumberOfBlocksInADimension(self.undergroundBlocksHeight)

        self.openPitBlocksLenghtLimits = getNumberOfBlocksInADimension(self.openPitBlocksLenght)
        self.openPitBlocksWidthLimits = getNumberOfBlocksInADimension(self.openPitBlocksWidth)
        self.openPitBlocksHeightLimits = getNumberOfBlocksInADimension(self.openPitBlocksHeight)

    def getBlockInfo(self):
        self.CA_blocks = [i for i in range(len(self.openPitBlocksLenght.values()))]
        self.S_blocks = [i for i in range(len(self.undergroundBlocksLenght.values()))]

    def setParametersToEvaluate(self):
        #OpenPit Parameters
        self.t_C   = {period : period + 1 for period in range(self.numberOfPeriods)}
        self.RMu_t = {period : 8683200.0 for period in range(self.numberOfPeriods)}#Superior infinita, 0 por abajo Originales: 13219200
        self.RMl_t = {period : 5788800.0 for period in range(self.numberOfPeriods)}#Valor original 8812800.0
        self.RPu_t = {period : 4601205.0 for period in range(self.numberOfPeriods)}#Valor original 10933380.0
        self.RPl_t = {period : 4162995.0 for period in range(self.numberOfPeriods)}#Valor original 7288920.0 
        self.qu_t  = {period : 1 for period in range(self.numberOfPeriods)}#Leyes promedio maxima y minima.
        self.ql_t  = {period : 0 for period in range(self.numberOfPeriods)}


        #Underground Parameters
        self.t_S   = {period : period + 1 for period in range(self.numberOfPeriods)}
        self.MU_mt = {period : 6975072.0  for period in range(self.numberOfPeriods)} #Tonleage es mina
        self.ML_mt = {period : 4650048.0 for period in range(self.numberOfPeriods)}
        self.MU_pt = {period : 6460300.8  for period in range(self.numberOfPeriods)}#Mineral es planta
        self.ML_pt = {period : 4306867.2 for period in range(self.numberOfPeriods)}
        self.qU_dt = {period : 1 for period in range(self.numberOfPeriods)}
        self.qL_dt = {period : 0 for period in range(self.numberOfPeriods)}
        self.A_d   = {period : 2 for period in range(self.numberOfPeriods)}
        self.NU_nt = {period : 42 for period in range(self.numberOfPeriods)} 
        self.NL_nt = {period : 30 for period in range(self.numberOfPeriods)}
        self.N_t   = {period : int((0.75*self.NU_nt[0] + 0.25*self.NL_nt[0])/2) * (1 + period) for period in range(self.numberOfPeriods)}
        self.RL_dt = {period : 0.3 for period in range(self.numberOfPeriods)}
        self.RU_dt = {period : 0.7 for period in range(self.numberOfPeriods)}
            
        self.maxTimeOpenPit = self.t_C[max(self.t_C)]
        self.maxTimeUnderground = self.t_S[max(self.t_S)]

    def setGlobalParameters(self):
        self.colHeight = 300
        self.securityLevel = 30
        pricePonderator = 1
        mineCostPonderator = 1
        plantCostPonderator = 1
        self.basePrice = 3791.912 * pricePonderator
        self.mineCostPonderator = 1 * mineCostPonderator
        self.basePlantCostPonderator = 1 * plantCostPonderator
        self.setMineLimits()
        self.predecessorBlock = self.setPredecessorBlock()

        self.dif_centroide = self.openPitBlocksLenghtLimits[0]//2 - self.undergroundBlocksLenghtLimits[0]//2
        ZZ = 780
        self.pos_x = 430         
        self.pos_y = 550         
        self.pos_z = ZZ   

    def setPredecessorBlock(self):
        predecessorBlock = []
        superiorBlock = finalBlock(self.CA_blocks, self.openPitBlocksLenghtLimits,self.openPitBlocksWidthLimits, self.openPitBlocksHeightLimits)
        for i in range(len(self.CA_blocks)):
            for j in superiorBlock[i]:
                aux_1 = []
                aux_1.append(self.CA_blocks[i])
                aux_1.append(j)
                predecessorBlock.append(aux_1)
        return predecessorBlock

    def getUndergroundVariables(self):
        DP_init = 0       #### Tipo de extracción
        pos_x_f = 730     
        pos_y_f = 910     
        orientationToExtractTheDrawpoints = 0
        
        self.drawpoint, self.TON_d, self.MIN_D,self.LEY_D, self.C_P_D, self.C_M_D, self.predecessor, self.x_draw,self.y_draw, self.z_draw = drawpointFunction(
        self.pos_x, self.pos_y, self.pos_z, self.colHeight, DP_init, self.undergroundBlocksLenghtLimits, self.undergroundBlocksWidthLimits, self.undergroundBlocksHeightLimits, self.undergroundBlockTonnage, self.undergroundCP_S, self.undergroundCM_S, self.undergroundBlockMineral,
        self.undergroundCopperLaw, pos_x_f, pos_y_f,orientationToExtractTheDrawpoints)

    def setModelAndGetResults(self):
        self.objValue, self.variableValues, self.runtime, self.gap = self.setIntegratedModel(self.CA_blocks,self.drawpoint,self.openPitBlocksHeight,self.dif_centroide,self.pos_z,self.colHeight,self.securityLevel,self.predecessorBlock,self.predecessor,
                         self.openPitBlockTonnage,self.openPitBlockMineral,self.openPitBlockRecovery,self.openPitCopperLaw,self.openPitVariableExtractionCosts,self.openPitExtractionFixedCosts,
                         self.TON_d,self.MIN_D,self.undergroundBlockRecovery,self.LEY_D,self.C_P_D,self.C_M_D,
                         self.t_C ,self.RMu_t,self.RMl_t,self.RPu_t,self.RPl_t,self.qu_t ,self.ql_t,self.maxTimeOpenPit,
                         self.t_S ,self.MU_mt,self.ML_mt,self.MU_pt,self.ML_pt,self.qU_dt,self.qL_dt,self.A_d,self.NU_nt,self.NL_nt,self.N_t ,self.RL_dt ,self.RU_dt ,self.maxTimeUnderground,
                         0.01,self.basePrice,self.mineCostPonderator,self.basePlantCostPonderator)

    def setIntegratedModel(self, bloques_CA,drawpoint,cord_z_C,dif_centroide,pos_z,col_height,cota_seg,predecessor_block,predecessor,
                                TON_C,MIN_C,REC_C,LEY_C,CM_CA_C,CP_CA_C,
                                TON_d,MIN_D,REC,LEY_D,C_P_D,C_M_D,
                                t_C,RMu_t,RMl_t,RPu_t,RPl_t,qu_t,ql_t,time_max_C,
                                t_S,MU_mt,ML_mt,MU_pt,ML_pt,qU_dt,qL_dt,A_d,NU_nt,NL_nt,N_t,RL_dt,RU_dt,time_max_S,
                                GAP,precio,costo_mina_ponderador,costo_planta_ponderador):
        
        integratedModel = gp.Model(name = 'Modelo Integrado')

        # Open Pit
        x_bt_OP_I = integratedModel.addVars(t_C, bloques_CA, vtype=GRB.BINARY, name="x")



        # Underground  Model
        x_dt_S_I = integratedModel.addVars(drawpoint, t_S, vtype=GRB.BINARY, name="x")
        y_dt_S_I = integratedModel.addVars(drawpoint, t_S, vtype=GRB.CONTINUOUS, name="y")
        z_dt_S_I = integratedModel.addVars(drawpoint, t_S, vtype=GRB.BINARY, name="z")
        
        rest_cota = integratedModel.addConstrs((x_bt_OP_I[ti, b]*(cord_z_C[b] - dif_centroide - pos_z - col_height - cota_seg) 
                                                >= 0 for b in bloques_CA for ti in t_C), "Cota")
        
        Ton_Up  = integratedModel.addConstrs((gp.quicksum(x_bt_OP_I[ti, b]*TON_C[b] for b in bloques_CA) 
                                <= RMu_t[ti] for ti in t_C), "Ton_max")
        Ton_low = integratedModel.addConstrs((gp.quicksum(x_bt_OP_I[ti, b]*TON_C[b] for b in bloques_CA) 
                                    >= RMl_t[ti] for ti in t_C), "Ton_min")
        Mat_Up_OP = integratedModel.addConstrs((gp.quicksum(x_bt_OP_I[ti, b]*MIN_C[b] for b in bloques_CA) <= 
                                RPu_t[ti] for ti in t_C), "Mat_max")
        Mat_low_OP = integratedModel.addConstrs((gp.quicksum(x_bt_OP_I[ti, b]*MIN_C[b] for b in bloques_CA) >= 
                                    RPl_t[ti] for ti in t_C), "Mat_min")
        BLOCK_SUP_OP = integratedModel.addConstrs((gp.quicksum(x_bt_OP_I[m, predecessor_block[l][0]]*(time_max_C-m+1) for m in t_C)
                                                    <=  gp.quicksum(x_bt_OP_I[m, predecessor_block[l][1]]*(time_max_C-m+1)
                                                                    for m in t_C)  for l in range(len(predecessor_block))),
                                                "Superior_Block")
        
        Reserve_cons_OP = integratedModel.addConstrs((gp.quicksum(x_bt_OP_I[ti, b] for ti in t_C) <= 1 for b in bloques_CA), 
                                "Reserve_cons")
        GQC_Up_OP = integratedModel.addConstrs((gp.quicksum(x_bt_OP_I[ti, b]*TON_C[b]*LEY_C[b] for b in bloques_CA) <=
                                qu_t[ti] * gp.quicksum(x_bt_OP_I[ti, b]*TON_C[b] for b in bloques_CA) for ti in t_C), 
                                "GQC_Up")

        GQC_low_OP = integratedModel.addConstrs((gp.quicksum(x_bt_OP_I[ti, b]*TON_C[b]*LEY_C[b] for b in bloques_CA) >=
                                ql_t[ti] * gp.quicksum(x_bt_OP_I[ti, b]*TON_C[b] for b in bloques_CA) for ti in t_C), 
                                "GQC_Up")


        #Restricciones underground
        Ton_Up = integratedModel.addConstrs((gp.quicksum(y_dt_S_I[d, ti]*TON_d[d] for d in drawpoint) <= MU_mt[ti] for ti in t_S),
                                            "Min_max")
        
        Ton_low = integratedModel.addConstrs((gp.quicksum(y_dt_S_I[d, ti]*TON_d[d] for d in drawpoint) >= ML_mt[ti] for ti in t_S),
                                            "Min_min")

        Mat_Up = integratedModel.addConstrs((gp.quicksum(y_dt_S_I[d, ti]* MIN_D[d] for d in drawpoint) <= MU_pt[ti] for ti in t_S),
                                            "Mat_max")

        Mat_low = integratedModel.addConstrs((gp.quicksum(y_dt_S_I[d, ti]* MIN_D[d] for d in drawpoint) >= ML_pt[ti] for ti in t_S)
                                            , "Mat_min")

        GQC_Up = integratedModel.addConstrs((gp.quicksum(y_dt_S_I[d, ti]*LEY_D[d]*TON_d[d] for d in drawpoint) <=
                                qU_dt[ti] * gp.quicksum(TON_d[d]*y_dt_S_I[d, ti] for d in drawpoint) for ti in t_S), "GQC_Up")

        GQC_low = integratedModel.addConstrs((gp.quicksum(y_dt_S_I[d, ti]*LEY_D[d]*TON_d[d] for d in drawpoint) >=
                                qL_dt[ti] * gp.quicksum(TON_d[d]*y_dt_S_I[d, ti] for d in drawpoint) for ti in t_S), "GQC_low")

        DP_Sup = integratedModel.addConstrs((gp.quicksum(x_dt_S_I[predecessor[l][0], m]*(max(t_S)-m+1) for m in t_S) <=
                                    gp.quicksum(x_dt_S_I[predecessor[l][1], m]*(max(t_S)-m+1) for m in t_S)  
                                    for l in range(len(predecessor))), "DP_Sup")

        Drawp_init = integratedModel.addConstrs((gp.quicksum(x_dt_S_I[d, ti] for ti in t_S) <= 1 for d in drawpoint), "Drawp_init")

        ## Lo que hace Drawpextract_61, es forzar a que solamente se puede extraer un drawpoint una vez que se activo
        Drawpextract_61 = integratedModel.addConstrs((gp.quicksum(x_dt_S_I[d, tau] for tau in range(ti+1)) >= z_dt_S_I[d, ti]  
                                            for d in drawpoint for ti in t_S), "Drawpextract_61")

        ## Un drawpoint solamente puede ser extraido por un preiodo pre determinado (A_d)
        Drawpextract_62 = integratedModel.addConstrs((gp.quicksum(z_dt_S_I[d, ti] for ti in t_S)  <= A_d[ti]  for d in drawpoint
                                                    for ti in t_S), "Drawp_62")

        ## Una vez se inicia extrayendo de un drawpoint, se continua extrayendo sin interrupción
        Drawpextract_63 = integratedModel.addConstrs((A_d[ti] *(z_dt_S_I[d, ti] - z_dt_S_I[d, ti+1]) 
                                            - gp.quicksum(z_dt_S_I[d, tau] for tau in range(ti+1)) <= 0 
                                            for d in drawpoint for ti in range(0,max(t_S))), "Drawpextract_63")

        ## El número de nuevos drawpoints debe tener un limite superior
        Drawpextract_64_1 = integratedModel.addConstrs((gp.quicksum(x_dt_S_I[d, ti] for d in drawpoint) <= NU_nt[ti] for ti 
                                                        in t_S)
                                                        ,"Drawpextract_64_1")

        ## El número de nuevos drawpoints debe tener un limite inferior
        Drawpextract_64_2 = integratedModel.addConstrs((gp.quicksum(x_dt_S_I[d, ti] for d in drawpoint) >= NL_nt[ti] for ti 
                                                        in t_S)
                                                        , "Drawpextract_64_2")

        ## El número de nuevos drawpoints debe tener un limite inferior respecto al origen
        Drawpextract_64_3 = integratedModel.addConstrs((gp.quicksum(x_dt_S_I[d, ti] for d in drawpoint) <= NU_nt[0] for ti 
                                                        in t_S)
                                                        ,"Drawpextract_64_3")

        ## El número máximo de drawpoints siendo extraidos simultáneamente en un periodo debe tener un límite
        Drawpextract_65 = integratedModel.addConstrs((gp.quicksum(z_dt_S_I[d, ti] for d in drawpoint) <= N_t[ti] for ti in t_S)
                                                    , "Drawpextract_65")

        ## El porcentaje de tonelaje extraido es cero si el drawpoint no es extraido en el periodo
        Drawpextract_66 = integratedModel.addConstrs((y_dt_S_I[d, ti] <= z_dt_S_I[d, ti] for d in drawpoint for ti in t_S),
                                                    "Drawpextract_66")

        ## Extracción mínima constante a extraer (RL_dt es el ratio mínimo de extracción en el periodo t)
        Drawpextract_67_1 = integratedModel.addConstrs((RL_dt[ti] * z_dt_S_I[d, ti]  <= y_dt_S_I[d, ti] for d in drawpoint
                                                        for ti in t_S), "Drawpextract_67_1")

        Reserver_cnst = integratedModel.addConstrs((gp.quicksum(y_dt_S_I[d, ti] for ti in t_S) <= 1 for d in drawpoint),
                                                    "Reserver_cnst")

        restricion_partida_1 = integratedModel.addConstr(x_dt_S_I[predecessor[0][0],0] == 1, "restriccion_partida 1")

        ## Lo mínimo a extraer en el primer drawpoint es de 0.3 
        restricion_partida_2 = integratedModel.addConstr(y_dt_S_I[predecessor[0][0],0] >= 0.3, "restriccion_partida 2")

        ## Se debe extraer un mínimo de un 90% de cada drawpoint
        restricion_partida_E =integratedModel.addConstrs((gp.quicksum(y_dt_S_I[d, ti]*z_dt_S_I[d, ti] for ti in t_S) >= 0.8
                                                        for d in drawpoint), "Reserver_cnst")

        ## Los drawpoints se extraen en orden (es decir que el z anterior debe estar activo para que el siguiente lo esté)
        restricion_z_dt = integratedModel.addConstrs((gp.quicksum(z_dt_S_I[predecessor[l][0], m]*(max(t_S)-m+1) for m in t_S) <=
                                    gp.quicksum(z_dt_S_I[predecessor[l][1], m]*(max(t_S)-m+1) for m in t_S)  
                                    for l in range(len(predecessor))), "DP_Sup")

        
        openPitObjectiveFunction = gp.quicksum(x_bt_OP_I[ti, b]*((((0.7*precio*LEY_C[b]-CP_CA_C[b]*costo_planta_ponderador)*MIN_C[b])-(CM_CA_C[b]*costo_mina_ponderador*TON_C[b]))/
                                                ((1+0.1)**t_C[ti])) for ti in t_C for b in bloques_CA)

        undergroundObjectiveFunction = gp.quicksum(y_dt_S_I[d, ti]*((((0.7*precio*LEY_D[d]-C_P_D[d]*costo_planta_ponderador)*MIN_D[d])-(C_M_D[d]*costo_mina_ponderador*TON_d[d]))/
                                                ((1+0.1)**(t_S[ti]+time_max_C))) for ti in t_S for d in drawpoint)

        FO_Int = openPitObjectiveFunction + undergroundObjectiveFunction
        
        integratedModel.setObjective(FO_Int, GRB.MAXIMIZE)
        integratedModel.Params.MIPGap = GAP
        integratedModel.Params.TimeLimit = 3600
        
        integratedModel.optimize()
        
        # Saca los valores de la solución
        lista_variable_Integrado = (integratedModel.getAttr(GRB.Attr.X, integratedModel.getVars()))
        solucion = integratedModel.objVal
        runtime = integratedModel.Runtime
        gap_f = integratedModel.MIPGap
        
        return solucion, lista_variable_Integrado, runtime, gap_f