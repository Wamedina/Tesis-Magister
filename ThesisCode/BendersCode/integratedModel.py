import pandas as pd
import gurobipy   as     gp
from   gurobipy   import GRB
from globalFunctions import getNumberOfBlocksInADimension
from integratedModel import *
from openPitFunctions import predecessorBlocks
from globalFunctions import getNumberOfBlocksInADimension
from drawpointFunction  import drawpointFunction
from itertools import chain


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
        self.setPossibleHeights()
        self.setModelAndGetResults()  
        return self.objValue, self.variableValues, self.runtime, self.gap  

    def setOpenPitVariables(self):
        self.openPitBlocksLength = self.openMineDataframe['X'].to_dict() 
        self.openPitBlocksWidth = self.openMineDataframe['Y'].to_dict() 
        self.openPitBlocksHeight = self.openMineDataframe['Z'].to_dict() 
        self.L_b = self.openMineDataframe['Ton'].to_dict() #openPitBlockTonnage
        self.o_b = self.openMineDataframe['Mineral'].to_dict() #openPitBlockMineral
        self.openPitBlockRecovery = self.openMineDataframe['Recuperación'].to_dict() #openPitBlockRecovery
        self.openPitCopperLaw = self.openMineDataframe['%Cu'].to_dict() #openPitCopperLaw
        self.c_pbt = self.openMineDataframe['CPlanta CA'].to_dict() #openPitPlantCapacity
        self.c_mbt = self.openMineDataframe['CMina CA'].to_dict() #openPitMineCapacity
      
    def setUndergroundVariables(self):
        self.undergroundBlocksLength = self.undergroundMineDataframe['X'].to_dict()             
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
        self.undergroundBlocksLengthLimits = getNumberOfBlocksInADimension(self.undergroundBlocksLength)
        self.undergroundBlocksWidthLimits = getNumberOfBlocksInADimension(self.undergroundBlocksWidth)
        self.undergroundBlocksHeightLimits = getNumberOfBlocksInADimension(self.undergroundBlocksHeight)

        self.openPitBlocksLengthLimits = getNumberOfBlocksInADimension(self.openPitBlocksLength)
        self.openPitBlocksWidthLimits = getNumberOfBlocksInADimension(self.openPitBlocksWidth)
        self.openPitBlocksHeightLimits = getNumberOfBlocksInADimension(self.openPitBlocksHeight)

    def getBlockInfo(self):
        self.openPitBlocks = [i for i in range(len(self.openPitBlocksLength.values()))]
        self.S_blocks = [i for i in range(len(self.undergroundBlocksLength.values()))]

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
        self.p_t = 3791.912 
        self.desc = 0.1
        self.setMineLimits()
        self.predecessorBlock = self.setPredecessorBlock()

        self.dif_centroide = self.openPitBlocksLengthLimits[0]//2 - self.undergroundBlocksLengthLimits[0]//2
        ZZ = 780
        self.pos_x = 430         
        self.pos_y = 550         
        self.pos_z = ZZ   

    def setPredecessorBlock(self):
        predecessorBlock = []
        superiorBlock = predecessorBlocks(self.openPitBlocks, self.openPitBlocksLengthLimits,self.openPitBlocksWidthLimits, self.openPitBlocksHeightLimits)
        for i in range(len(self.openPitBlocks)):
            for j in superiorBlock[i]:
                aux_1 = []
                aux_1.append(self.openPitBlocks[i])
                aux_1.append(j)
                predecessorBlock.append(aux_1)
        return predecessorBlock

    def getUndergroundVariables(self):
        DP_init = 0       #### Tipo de extracción
        pos_x_f = 730     
        pos_y_f = 910     
        orientationToExtractTheDrawpoints = 0
        
        self.drawpoint, self.G_d, self.Q_d,self.LEY_D, self.C_pdt, self.C_mdt, self.predecessor, self.x_draw,self.y_draw, self.z_draw = drawpointFunction(
                        self.pos_x, self.pos_y, self.pos_z, self.colHeight, DP_init, self.undergroundBlocksLengthLimits, self.undergroundBlocksWidthLimits, self.undergroundBlocksHeightLimits, self.undergroundBlockTonnage, self.undergroundCP_S, self.undergroundCM_S, self.undergroundBlockMineral,
                        self.undergroundCopperLaw, pos_x_f, pos_y_f, orientationToExtractTheDrawpoints)

    def setPossibleHeights(self):
        self.blockHeight, self.maxHeight, self.minHeight, self.numOfDifferentsBlocks = self.undergroundBlocksHeightLimits

    def setModelAndGetResults(self):
        self.objValue, self.variableValues, self.runtime, self.gap = self.setIntegratedModel()

    def setIntegratedModel(self):
         
        integratedModel = gp.Model(name = 'Modelo Integrado')

        # Underground  Model

        #14. Naturaleza de las variables
        x_dt = integratedModel.addVars(self.drawpoint, self.t_S, vtype=GRB.BINARY, name="x")
        y_dt = integratedModel.addVars(self.drawpoint, self.t_S, vtype=GRB.CONTINUOUS, name="y")
        z_dt = integratedModel.addVars(self.drawpoint, self.t_S, vtype=GRB.BINARY, name="z")

        #1. Restricción sobre la cantidad de tonelaje máxima y mínima a extraer en cada periodo.
        Ton_Up = integratedModel.addConstrs((gp.quicksum(y_dt[d, ti]*self.G_d[d] for d in self.drawpoint) <= self.MU_mt[ti] for ti in self.t_S),
                                         "Min_max")
        
        Ton_low = integratedModel.addConstrs((gp.quicksum(y_dt[d, ti]*self.G_d[d] for d in self.drawpoint) >= self.ML_mt[ti] for ti in self.t_S),
                                            "Min_min")
        #2. Restricción sobre la cantidad de material máxima y mínima a procesar en cada periodo.
        Mat_Up = integratedModel.addConstrs((gp.quicksum(y_dt[d, ti]* self.Q_d[d] for d in self.drawpoint) <= self.MU_pt[ti] for ti in self.t_S),
                                            "Mat_max")

        Mat_low = integratedModel.addConstrs((gp.quicksum(y_dt[d, ti]* self.Q_d[d] for d in self.drawpoint) >= self.ML_pt[ti] for ti in self.t_S)
                                            , "Mat_min")
        #3. Rango de leyes máximas y mínimas a procesar
        GQC_Up = integratedModel.addConstrs((gp.quicksum(y_dt[d, ti]*self.LEY_D[d]*self.G_d[d] for d in self.drawpoint) <=
                                self.qU_dt[ti] * gp.quicksum(self.Q_d[d] * y_dt[d, ti] for d in self.drawpoint) for ti in self.t_S), "GQC_Up")

        GQC_low = integratedModel.addConstrs((gp.quicksum(y_dt[d, ti]*self.LEY_D[d]*self.G_d[d] for d in self.drawpoint) >=
                                self.qL_dt[ti] * gp.quicksum(self.Q_d[d] * y_dt[d, ti] for d in self.drawpoint) for ti in self.t_S), "GQC_low")

        #4. Todos los puntos de extracci ́on deben ser iniciados en el largo de la extracción
        Drawp_init = integratedModel.addConstrs((gp.quicksum(x_dt[d, ti] for ti in self.t_S) <= 1 for d in self.drawpoint), "Drawp_init")

        #5. Los puntos de extracción deben ser activados al menos en el mismo periodo para que se inicie la extracción 
        Drawpextract_61 = integratedModel.addConstrs((gp.quicksum(x_dt[d, tau] for tau in range(ti+1)) >= z_dt[d, ti]  
                                            for d in self.drawpoint for ti in self.t_S), "Drawpextract_61")


        #6. Existe una cantidad máxima y mínima de drawpoints a abrir en cada periodo.
        Drawpextract_64_1 = integratedModel.addConstrs((gp.quicksum(x_dt[d, ti] for d in self.drawpoint) <= self.NU_nt[ti] for ti 
                                                        in self.t_S)
                                                        ,"Drawpextract_64_1")

        Drawpextract_64_2 = integratedModel.addConstrs((gp.quicksum(x_dt[d, ti] for d in self.drawpoint) >= self.NL_nt[ti] for ti 
                                                        in self.t_S)
                                                        , "Drawpextract_64_2")

        #7. Existe una m ́axima cantidad de drawpoints a extraer por periodo.
        Drawpextract_65 = integratedModel.addConstrs((gp.quicksum(z_dt[d, ti] for d in self.drawpoint) <= self.N_t[ti] for ti in self.t_S)
                                                    , "Drawpextract_65")


        #8. Si iniciamos la extracción de un drawpoint esta debe durar por su duraci ́on determinada.
        ## Un drawpoint solamente puede ser extraido por un preiodo pre determinado (A_d)
        Drawpextract_62 = integratedModel.addConstrs((gp.quicksum(z_dt[d, ti] for ti in self.t_S)  <= self.A_d[ti]  for d in self.drawpoint
                                                    for ti in self.t_S), "Drawp_62")

        ## Una vez se inicia extrayendo de un drawpoint, se continua extrayendo sin interrupción
        Drawpextract_63 = integratedModel.addConstrs((self.A_d[ti] *(z_dt[d, ti] - z_dt[d, ti+1]) 
                                            - gp.quicksum(z_dt[d, tau] for tau in range(ti+1)) <= 0 
                                            for d in self.drawpoint for ti in range(0,max(self.t_S))), "Drawpextract_63")

        #9. Relación de variables, el porcentaje a extraer es 0 si no se extra un drawpoint.
        Drawpextract_66 = integratedModel.addConstrs((y_dt[d, ti] <= z_dt[d, ti] for d in self.drawpoint for ti in self.t_S),
                                                    "Drawpextract_66")

        #10. Existe una tasa m ́ınima de extracci ́on para cada drawpoint a extraer.
        Drawpextract_67_1 = integratedModel.addConstrs((self.RL_dt[ti] * z_dt[d, ti]  <=  y_dt[d, ti] for d in self.drawpoint
                                                        for ti in self.t_S), "Drawpextract_67_1")

        #11. La altura a extraer debe ser mayor a una cantidad m ́ınima.
        #rest_11 = integratedModel.addConstrs((gp.quicksum(y_dt[d,ti] for ti in self.t_S)>= self.colHeight for d in self.drawpoint))

        #12. No podemos extraer más del 100 % de un drawpoint.
        Reserver_cnst = integratedModel.addConstrs((gp.quicksum(y_dt[d, ti] for ti in self.t_S) <= 1 for d in self.drawpoint),
                                                    "Reserver_cnst")

        #13. Si se activa un drawpoint, se extrae en ese periodo
        rest_13 = integratedModel.addConstrs(x_dt[d,ti] <= z_dt[d, ti] for d in self.drawpoint for ti in self.t_S)

        #14. Naturaleza de variables.

        #15. Existe una m ́axima cantidad de drawpoints a extraer por periodo.
        rest_15= integratedModel.addConstrs((gp.quicksum(x_dt[d, ti] for d in self.drawpoint) <= self.N_t[ti] for ti in self.t_S)
                                                    , "Drawpextract_65")

        
        #16. Restricción sobre el inicio de la extracci ́on de los drawpoints.
        DP_Sup = integratedModel.addConstrs((gp.quicksum(x_dt[self.predecessor[l][0], s]*(max(self.t_S)-s+1) for s in self.t_S) <=
                                    gp.quicksum(x_dt[self.predecessor[l][1], s]*(max(self.t_S)-s+1) for s in self.t_S)  
                                    for l in range(len(self.predecessor))), "DP_Sup")

        #17. Restricci ́on sobre la extracci ́on de los drawpoints.
        restricion_z_dt = integratedModel.addConstrs((gp.quicksum(z_dt[self.predecessor[l][0], s]*(max(self.t_S)-s+1) for s in self.t_S) <=
                                    gp.quicksum(z_dt[self.predecessor[l][1], s]*(max(self.t_S)-s+1) for s in self.t_S)  
                                    for l in range(len(self.predecessor))), "DP_Sup")

        # Open Pit
        x_bt = integratedModel.addVars(self.t_C, self.openPitBlocks, vtype=GRB.BINARY, name="x")


        #Función objetivo
        
        undergroundObjectiveFunction = gp.quicksum(y_dt[d, ti]*((((self.p_t * self.LEY_D[d] -self.C_pdt[d] ) * self.Q_d[d])-(self.C_mdt[d]*self.G_d[d]))/
                                        ((1+self.desc)**(self.t_S[ti]))) for ti in self.t_S for d in self.drawpoint)
        
        
        #1. Restricci ́on sobre la cantidad de tonelaje m ́axima y m ́ınima a extraer en cada periodo.
        Ton_Up  = integratedModel.addConstrs((gp.quicksum(x_bt[ti, b]*self.L_b[b] for b in self.openPitBlocks) 
                                <= self.RMu_t[ti] for ti in self.t_C), "Ton_max")
        Ton_low = integratedModel.addConstrs((gp.quicksum(x_bt[ti, b]*self.L_b[b] for b in self.openPitBlocks) 
                                >= self.RMl_t[ti] for ti in self.t_C), "Ton_min")

        #2. Restricci ́on sobre la cantidad de material m ́axima y m ́ınima a extraer en cada periodo.
        Mat_Up_OP = integratedModel.addConstrs((gp.quicksum(x_bt[ti, b]*self.o_b[b] for b in self.openPitBlocks) <= 
                                self.RPu_t[ti] for ti in self.t_C), "Mat_max")
        Mat_low_OP = integratedModel.addConstrs((gp.quicksum(x_bt[ti, b]*self.o_b[b] for b in self.openPitBlocks) >= 
                                self.RPl_t[ti] for ti in self.t_C), "Mat_min")

        #3. Restricci ́on de precedencia de los bloques a extraer, debemos extraer los 5 bloques superiores al bloque objetivo para sacar a este
        BLOCK_SUP_OP = integratedModel.addConstrs((gp.quicksum(x_bt[s, self.predecessorBlock[l][0]]*(self.maxTimeOpenPit-s+1) for s in self.t_C) <= 
                                        gp.quicksum(x_bt[s, self.predecessorBlock[l][1]]*(self.maxTimeOpenPit-s+1) for s in self.t_C)  
                                    for l in range(len(self.predecessorBlock))), "Superior_Block")

        #4. Restricci ́on sobre la ley m ́axima y m ́ınima por periodo.
        GQC_Up_OP = integratedModel.addConstrs((gp.quicksum(x_bt[ti, b]*self.L_b[b]*self.openPitCopperLaw[b] for b in self.openPitBlocks) <=
                            self.qu_t[ti] * gp.quicksum(x_bt[ti, b]*self.L_b[b] for b in self.openPitBlocks) for ti in self.t_C), 
                                "GQC_Up")

        GQC_low_OP = integratedModel.addConstrs((gp.quicksum(x_bt[ti, b]*self.L_b[b]*self.openPitCopperLaw[b] for b in self.openPitBlocks) >=
                            self.ql_t[ti] * gp.quicksum(x_bt[ti, b]*self.L_b[b] for b in self.openPitBlocks) for ti in self.t_C), 
                                "GQC_LOW")

        #5. Podemos extraer el bloque en un solo periodo.
        Reserve_cons_OP = integratedModel.addConstrs((gp.quicksum(x_bt[ti, b] for ti in self.t_C) <= 1 for b in self.openPitBlocks), 
                                "Reserve_cons")

        #Función objetivo
        openPitObjectiveFunction = gp.quicksum(x_bt[ti, b]*((((self.p_t*self.openPitCopperLaw[b]-self.c_pbt[b])*self.o_b[b])-(self.c_mbt[b]*self.L_b[b]))/((1+self.desc)**self.t_C[ti]))
                    for ti in self.t_C for b in self.openPitBlocks)

        #FALTA DEFINIR LOS CONJUNTOS B_v

        V = [height for height in chain(range(self.minHeight,self.maxHeight,self.blockHeight), [self.maxHeight])]
        rho_v = [1 - (v - self.minHeight)/(self.maxHeight - self.minHeight) for v in V]
        B_v = []
        for v in V:
            numberOfBlocksBelowV = (self.openPitBlocksLengthLimits[3]*self.openPitBlocksWidthLimits[3])*((v-self.minHeight)/self.openPitBlocksHeightLimits[0])
            blocksBelowV = [block for block in range(int(numberOfBlocksBelowV)) if not numberOfBlocksBelowV == 0]
            B_v.append(blocksBelowV)

        #Restricciones del crown pillar

        #Variable 1 si y solo si el crown pillar esta ubicado en la elevaci ́on v, 0 en otro caso.
        w_v = integratedModel.addVars(V, vtype=GRB.BINARY, name="w")

        #Restricciones del crown pillar
        pillar_1 = integratedModel.addConstrs(gp.quicksum(x_bt[ti, b] for ti in self.t_C) <= 1 - w_v[v] for b in B_v[v] for v in range(len(V)))

        pillar_2 = integratedModel.addConstrs(gp.quicksum(y_dt[d, ti] for d in self.drawpoint
                                                        for ti in self.t_S) <= rho_v[v] * w_v[v] + (1 - w_v[v]) for v in range(len(V)))

        ##FALTA DEFINIR LOS CONJUNTOS B_v, V

        #Variable 1 si y solo si el crown pillar esta ubicado en la elevaci ́on v, 0 en otro caso.
        #w_v = integratedModel.addVars(self.t_C, self.openPitBlocks, vtype=GRB.CONTINUOUS, name="w")

        #Restricciones del crown pillar
        #pillar_2 = integratedModel.addConstrs(gp.quicksum(x_bt[ti, b] for b in self.B_v)<=1- w_v[v] for v in V for ti in self.t_C)

        #fixed_position = integratedModel.addConstrs(w_v == w_opt)
        integratedObjectiveFunction = integratedObjectiveFunction + openPitObjectiveFunction

        
        integratedModel.setObjective(integratedObjectiveFunction, GRB.MAXIMIZE)
        integratedModel.Params.MIPGap = 0.01
        integratedModel.Params.TimeLimit = 3600
        
        integratedModel.optimize()
        
        # Saca los valores de la solución
        lista_variable_Integrado = (integratedModel.getAttr(GRB.Attr.X, integratedModel.getVars()))
        solucion = integratedModel.objVal
        runtime = integratedModel.Runtime
        gap_f = integratedModel.MIPGap
        
        return solucion, lista_variable_Integrado, runtime, gap_f