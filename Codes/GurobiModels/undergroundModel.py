import sys  
sys.path.insert(0, '../AuxiliarCodes/')

import gurobipy   as     gp
from   gurobipy   import GRB
from drawpointFunction  import drawpointFunction
from globalFunctions import getNumberOfBlocksInADimension
import pandas as pd

class UndergroundModel:
    def __init__(self, database, numberOfPeriods):
        self.database = database
        self.numberOfPeriods = numberOfPeriods
        self.DP_init = 0       #### Tipo de extracción
        self.colHeight = 300
        self.pos_x = 430     
        self.pos_y = 550     
        self.pos_z = 780
        self.pos_x_f = 730     
        self.pos_y_f = 910     
        self.basePrice = 3791.912
        self.orientationToExtractTheDrawpoints = 0

    def execute(self):
        self.getUndergroundVariablesFromCSV()
        self.getUndergroundInfo()
        self.setUndergroundParameters()
        self.setUndergroundMineLimits()
        self.setUndergroundVariables()
        self.setModelandGetResults()
        return self.objValue, self.variableValues, self.runtime, self.gap
    
    def getUndergroundVariablesFromCSV(self):
        self.undergroundBlocksLenght = self.database['X'].to_dict()             
        self.undergroundBlocksWidth  = self.database['Y'].to_dict()             
        self.undergroundBlocksHeight = self.database['Z'].to_dict()             
        self.undergroundBlockTonnage = self.database['Ton'].to_dict()              
        self.undergroundBlockMineral  = self.database['Mineral'].to_dict()          
        self.undergroundBlockRecovery  = self.database['Recuperación'].to_dict()     
        self.undergroundCopperLaw  = self.database['%Cu'].to_dict()
        self.undergroundExtractionFixedCosts = self.database['CPlanta CA'].to_dict()
        self.undergroundVariableExtractionCosts = self.database['CMina CA'].to_dict()
        self.undergroundCP_S = self.database['CPlanta S'].to_dict()
        self.undergroundCM_S = self.database['CMINA S'].to_dict() 
    
    def getUndergroundInfo(self):
        self.undergroundBlocks = [i for i in range(len(self.undergroundBlocksLenght.values()))]

    def setUndergroundParameters(self):
        #Underground Parameters
        self.t_S   = {period : period + 1 for period in range(self.numberOfPeriods)}
        self.MU_mt = {period : 25806600.0  for period in range(self.numberOfPeriods)} #Tonleage es mina
        self.ML_mt = {period : 0.0  for period in range(self.numberOfPeriods)}
        self.MU_pt = {period : 17777880.0   for period in range(self.numberOfPeriods)}#Mineral es planta
        self.ML_pt = {period : 0.0 for period in range(self.numberOfPeriods)}
        self.qU_dt = {period : 1 for period in range(self.numberOfPeriods)}
        self.qL_dt = {period : 0.15 for period in range(self.numberOfPeriods)}
        self.A_d   = {period : 2 for period in range(self.numberOfPeriods)}
        self.NU_nt = {period : 59 for period in range(self.numberOfPeriods)} 
        self.NL_nt = {period : 0 for period in range(self.numberOfPeriods)}
        self.N_t   = {period : 57* (1 + period) for period in range(self.numberOfPeriods)}
        self.RL_dt = {period : 0.3 for period in range(self.numberOfPeriods)}
        self.RU_dt = {period : 0.7 for period in range(self.numberOfPeriods)}

    def setUndergroundVariables(self):
        self.drawpoint, self.G_d, self.Q_d,self.q_d, self.C_P_D, self.C_M_D, self.predecessor, self.x_draw,self.y_draw, self.z_draw = drawpointFunction(
                        self.pos_x, self.pos_y, self.pos_z, self.colHeight, self.DP_init, self.undergroundBlocksLenghtLimits, self.undergroundBlocksWidthLimits, self.undergroundBlocksHeightLimits, self.undergroundBlockTonnage, self.undergroundCP_S, self.undergroundCM_S, self.undergroundBlockMineral,
                        self.undergroundCopperLaw, self.pos_x_f, self.pos_y_f,self.orientationToExtractTheDrawpoints)
    
    def setUndergroundMineLimits(self):
        self.undergroundBlocksLenghtLimits = getNumberOfBlocksInADimension(self.undergroundBlocksLenght)
        self.undergroundBlocksWidthLimits = getNumberOfBlocksInADimension(self.undergroundBlocksWidth)
        self.undergroundBlocksHeightLimits = getNumberOfBlocksInADimension(self.undergroundBlocksHeight)

    def setModelandGetResults(self):
        self.objValue, self.variableValues, self.runtime, self.gap = self.setUndergroundModel(self.drawpoint,self.G_d,self.MU_mt, self.ML_mt, self.t_S, self.Q_d, self.q_d, self.qU_dt, self.qL_dt, self.predecessor, self.A_d, self.NU_nt, self.NL_nt,
                                                                     self.MU_pt, self.ML_pt, self.N_t, self.RL_dt, self.basePrice, self.C_M_D, self.C_P_D)

    def setUndergroundModel(self, drawpoint, G_d, MU_mt, ML_mt, t_S, Q_d, q_d, qU_dt, qL_dt, predecessor, A_d, NU_nt, NL_nt, 
                                MU_pt,ML_pt, N_t,RL_dt,basePrice,C_M_D,C_P_D):
                                
        undergroundModel = gp.Model(name = 'Modelo Integrado')
        undergroundModel.Params.TimeLimit = 3600

        x_dt = undergroundModel.addVars(drawpoint, t_S, vtype=GRB.BINARY, name="x")
        y_dt = undergroundModel.addVars(drawpoint, t_S, vtype=GRB.CONTINUOUS, name="y")
        z_dt = undergroundModel.addVars(drawpoint, t_S, vtype=GRB.BINARY, name="z")


        Ton_Up = undergroundModel.addConstrs((gp.quicksum(y_dt[d, ti]*G_d[d] for d in drawpoint) <= MU_mt[ti] for ti in t_S),
                                         "Min_max")
            
        Ton_low = undergroundModel.addConstrs((gp.quicksum(y_dt[d, ti]*G_d[d] for d in drawpoint) >= ML_mt[ti] for ti in t_S),
                                            "Min_min")

        Mat_Up = undergroundModel.addConstrs((gp.quicksum(y_dt[d, ti]* Q_d[d] for d in drawpoint) <= MU_pt[ti] for ti in t_S),
                                            "Mat_max")

        Mat_low = undergroundModel.addConstrs((gp.quicksum(y_dt[d, ti]* Q_d[d] for d in drawpoint) >= ML_pt[ti] for ti in t_S)
                                            , "Mat_min")

        GQC_low = undergroundModel.addConstrs((gp.quicksum(Q_d[d] * q_d[d] * y_dt[d, ti] for d in drawpoint) >=
                                qL_dt[ti] * gp.quicksum(G_d[d] * y_dt[d, ti] for d in drawpoint) for ti in t_S), "GQC_low")
        
        GQC_Up = undergroundModel.addConstrs((gp.quicksum(Q_d[d] * q_d[d] * y_dt[d, ti] for d in drawpoint) <=
                                qU_dt[ti] * gp.quicksum(G_d[d] * y_dt[d, ti] for d in drawpoint) for ti in t_S), "GQC_Up")

  

        Drawp_init = undergroundModel.addConstrs((gp.quicksum(x_dt[d, ti] for ti in t_S) <= 1 for d in drawpoint), "Drawp_init")

        ## Lo que hace Drawpextract_61, es forzar a que solamente se puede extraer un drawpoint una vez que se activo
        Drawpextract_61 = undergroundModel.addConstrs((gp.quicksum(x_dt[d, tau] for tau in range(ti+1)) >= z_dt[d, ti]  
                                            for d in drawpoint for ti in t_S), "Drawpextract_61")
        

        ## El número de nuevos drawpoints debe tener un limite superior
        Drawpextract_64_1 = undergroundModel.addConstrs((gp.quicksum(x_dt[d, ti] for d in drawpoint) <= NU_nt[ti] for ti 
                                                        in t_S)
                                                        ,"Drawpextract_64_1")

        ## El número de nuevos drawpoints debe tener un limite inferior
        Drawpextract_64_2 = undergroundModel.addConstrs((gp.quicksum(x_dt[d, ti] for d in drawpoint) >= NL_nt[ti] for ti 
                                                        in t_S)
                                                        , "Drawpextract_64_2")

        ## El número de nuevos drawpoints debe tener un limite inferior respecto al origen
        #Drawpextract_64_3 = undergroundModel.addConstrs((gp.quicksum(x_dt[d, ti] for d in drawpoint) <= NU_nt[0] for ti in t_S),"Drawpextract_64_3")

        ## El número máximo de drawpoints siendo extraidos simultáneamente en un periodo debe tener un límite
        Drawpextract_65 = undergroundModel.addConstrs((gp.quicksum(z_dt[d, ti] for d in drawpoint) <= N_t[ti] for ti in t_S)
                                                    , "Drawpextract_65")

        ## Un drawpoint solamente puede ser extraido por un preiodo pre determinado (A_d)
        Drawpextract_62 = undergroundModel.addConstrs((gp.quicksum(z_dt[d, ti] for ti in t_S)  <= A_d[ti]  for d in drawpoint
                                                    for ti in t_S), "Drawp_62")

        ## Una vez se inicia extrayendo de un drawpoint, se continua extrayendo sin interrupción
        Drawpextract_63 = undergroundModel.addConstrs((A_d[ti] *(z_dt[d, ti] - z_dt[d, ti+1]) 
                                            - gp.quicksum(z_dt[d, tau] for tau in range(ti+1)) <= 0 
                                            for d in drawpoint for ti in range(0,max(t_S))), "Drawpextract_63")
        
        ## El porcentaje de tonelaje extraido es cero si el drawpoint no es extraido en el periodo
        Drawpextract_66 = undergroundModel.addConstrs((y_dt[d, ti] <= z_dt[d, ti] for d in drawpoint for ti in t_S),
                                                    "Drawpextract_66")

        ## Extracción mínima constante a extraer (RL_dt es el ratio mínimo de extracción en el periodo t)
        Drawpextract_67_1 = undergroundModel.addConstrs((RL_dt[ti] * z_dt[d, ti]  <= y_dt[d, ti] for d in drawpoint
                                                        for ti in t_S), "Drawpextract_67_1")

        Reserver_cnst = undergroundModel.addConstrs((gp.quicksum(y_dt[d, ti] for ti in t_S) <= 1 for d in drawpoint),
                                                    "Reserver_cnst")

        rest_13 = undergroundModel.addConstrs(x_dt[d,ti] <= z_dt[d, ti] for d in self.drawpoint for ti in self.t_S)


        #15. Existe una m ́axima cantidad de drawpoints a extraer por periodo.
        rest_15= undergroundModel.addConstrs((gp.quicksum(x_dt[d, ti] for d in self.drawpoint) <= self.N_t[ti] for ti in self.t_S)
                                                    , "Drawpextract_65")

        #restricion_partida_1 = undergroundModel.addConstr(x_dt[predecessor[0][0],0] == 1, "restriccion_partida 1")

        ## Lo mínimo a extraer en el primer drawpoint es de 0.3 
        #restricion_partida_2 = undergroundModel.addConstr(y_dt[predecessor[0][0],0] >= 0.3, "restriccion_partida 2")

        ## Se debe extraer un mínimo de un 90% de cada drawpoint
        #restricion_partida_E =undergroundModel.addConstrs((gp.quicksum(y_dt[d, ti]*z_dt[d, ti] for ti in t_S) >= 0.8
         #                                               for d in drawpoint), "Reserver_cnst")
        DP_Sup = undergroundModel.addConstrs((gp.quicksum(x_dt[predecessor[l][0], m]*(max(t_S)-m+1) for m in t_S) <=
                            gp.quicksum(x_dt[predecessor[l][1], m]*(max(t_S)-m+1) for m in t_S)  
                            for l in range(len(predecessor))), "DP_Sup")

        ## Los drawpoints se extraen en orden (es decir que el z anterior debe estar activo para que el siguiente lo esté)
        restricion_z_dt = undergroundModel.addConstrs((gp.quicksum(z_dt[predecessor[l][0], m]*(max(t_S)-m+1) for m in t_S) <=
                                    gp.quicksum(z_dt[predecessor[l][1], m]*(max(t_S)-m+1) for m in t_S)  
                                    for l in range(len(predecessor))), "DP_Sup")
        



        
        undergroundObjectiveFunction = gp.quicksum(y_dt[d, ti]*((((basePrice*q_d[d]-C_P_D[d])*Q_d[d])-(C_M_D[d]*G_d[d]))/
                                        ((1+0.1)**(t_S[ti]))) for ti in t_S for d in drawpoint)
       
        undergroundModel.setObjective(undergroundObjectiveFunction, GRB.MAXIMIZE)
        undergroundModel.Params.MIPGap = 0.01
        
        undergroundModel.optimize()
        lista_variable_Integrado = (undergroundModel.getAttr(GRB.Attr.X, undergroundModel.getVars()))
        solucion = undergroundModel.objVal
        runtime = undergroundModel.Runtime
        gap_f = undergroundModel.MIPGap
        
        return solucion, lista_variable_Integrado, runtime, gap_f
        
path = "/home/williams/Tesis-Magister/Databases/"
undergroundDatabaseName = 'Modelo_F_OG.xlsx'
undergroundMineDataframe = pd.read_excel(path + undergroundDatabaseName, engine="openpyxl") #Notebook


numberOfPeriods = 5
undergroundModel = UndergroundModel(undergroundMineDataframe,numberOfPeriods)
undergroundObjValue, undergroundVariableValues, undergroundRuntime, undergroundGap = undergroundModel.execute()

for i in range(0, len(undergroundVariableValues[:900]),5):
    chunck = undergroundVariableValues[i:i+5]
    print(chunck)

