import sys  
sys.path.insert(0, '../AuxiliarCodes/')
import gurobipy   as     gp
from   gurobipy   import GRB
from drawpointFunction  import drawpointFunction
from globalFunctions import getNumberOfBlocksInADimension
from itertools import chain


class MasterProblem:
    #Underground Model + Crown Pillar Restrictions.
    def __init__(self, database, numberOfPeriods):
        self.database = database
        self.numberOfPeriods = numberOfPeriods
        self.DP_init = 0       #### Tipo de extracción
        self.desc = 0.1
        self.colHeight = 300
        self.pos_x = 430     
        self.pos_y = 550     
        self.pos_z = 780
        self.pos_x_f = 730     
        self.pos_y_f = 910     
        self.p_t = 3791.912
        self.epsilon = 1
        self.orientationToExtractTheDrawpoints = 0

    def setParameters(self):
        self.getUndergroundVariablesFromCSV()
        self.getUndergroundInfo()
        self.setUndergroundParameters()
        self.setUndergroundMineLimits()
        self.setUndergroundVariables()

    
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
        self.MU_mt = {period : 25806600.0/4  for period in range(self.numberOfPeriods)} #Tonleage es mina
        self.ML_mt = {period : 0.0  for period in range(self.numberOfPeriods)}
        self.MU_pt = {period : 17777880.0/4  for period in range(self.numberOfPeriods)}#Mineral es planta
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
        self.drawpoint, self.G_d, self.Q_d,self.LEY_D, self.C_pdt, self.C_mdt, self.predecessor, self.x_draw,self.y_draw, self.z_draw = drawpointFunction(
                        self.pos_x, self.pos_y, self.pos_z, self.colHeight, self.DP_init, self.undergroundBlocksLenghtLimits, self.undergroundBlocksWidthLimits, self.undergroundBlocksHeightLimits, self.undergroundBlockTonnage, self.undergroundCP_S, self.undergroundCM_S, self.undergroundBlockMineral,
                        self.undergroundCopperLaw, self.pos_x_f, self.pos_y_f,self.orientationToExtractTheDrawpoints)
    
    def setUndergroundMineLimits(self):
        self.undergroundBlocksLenghtLimits = getNumberOfBlocksInADimension(self.undergroundBlocksLenght)
        self.undergroundBlocksWidthLimits = getNumberOfBlocksInADimension(self.undergroundBlocksWidth)
        self.undergroundBlocksHeightLimits = getNumberOfBlocksInADimension(self.undergroundBlocksHeight)

    def setModelandGetResults(self):
        self.objValue, self.variableValues, self.runtime, self.gap = self.setUndergroundModel()

    def addThetaRestriction(self, subProblemObjValue, estimatedW_v, pi_vb):
        self.undergroundModel.addConstr(self.theta <= subProblemObjValue + gp.quicksum(gp.quicksum((self.w_v[v]-estimatedW_v[v]) * pi_vb[b] for b in self.B_v) for v in self.V))

    def setModel(self):#,v_p, theta_opt, w_opt):
                                
        self.undergroundModel = gp.Model(name = 'Modelo Integrado')
        self.undergroundModel.Params.TimeLimit = 3600
        self.undergroundModel.Params.OutputFlag = 0

        # Underground  Model

        #14. Naturaleza de las variables
        self.x_dt = self.undergroundModel.addVars(self.drawpoint, self.t_S, vtype=GRB.BINARY, name="x")
        y_dt = self.undergroundModel.addVars(self.drawpoint, self.t_S, vtype=GRB.CONTINUOUS, name="y")
        self.z_dt = self.undergroundModel.addVars(self.drawpoint, self.t_S, vtype=GRB.BINARY, name="z")
        

        #1. Restricción sobre la cantidad de tonelaje máxima y mínima a extraer en cada periodo.
        Ton_Up = self.undergroundModel.addConstrs((gp.quicksum(y_dt[d, ti]*self.G_d[d] for d in self.drawpoint) <= self.MU_mt[ti] for ti in self.t_S),
                                         "Min_max")
        
        Ton_low = self.undergroundModel.addConstrs((gp.quicksum(y_dt[d, ti]*self.G_d[d] for d in self.drawpoint) >= self.ML_mt[ti] for ti in self.t_S),
                                            "Min_min")
        #2. Restricción sobre la cantidad de material máxima y mínima a procesar en cada periodo.
        Mat_Up = self.undergroundModel.addConstrs((gp.quicksum(y_dt[d, ti]* self.Q_d[d] for d in self.drawpoint) <= self.MU_pt[ti] for ti in self.t_S),
                                            "Mat_max")

        Mat_low = self.undergroundModel.addConstrs((gp.quicksum(y_dt[d, ti]* self.Q_d[d] for d in self.drawpoint) >= self.ML_pt[ti] for ti in self.t_S)
                                            , "Mat_min")
        #3. Rango de leyes máximas y mínimas a procesar
        GQC_Up = self.undergroundModel.addConstrs((gp.quicksum(y_dt[d, ti]*self.LEY_D[d]*self.G_d[d] for d in self.drawpoint) <=
                                self.qU_dt[ti] * gp.quicksum(self.Q_d[d] * y_dt[d, ti] for d in self.drawpoint) for ti in self.t_S), "GQC_Up")

        GQC_low = self.undergroundModel.addConstrs((gp.quicksum(y_dt[d, ti]*self.LEY_D[d]*self.G_d[d] for d in self.drawpoint) >=
                                self.qL_dt[ti] * gp.quicksum(self.Q_d[d] * y_dt[d, ti] for d in self.drawpoint) for ti in self.t_S), "GQC_low")

        #4. Todos los puntos de extracci ́on deben ser iniciados en el largo de la extracción
        Drawp_init = self.undergroundModel.addConstrs((gp.quicksum(self.x_dt[d, ti] for ti in self.t_S) <= 1 for d in self.drawpoint), "Drawp_init")

        #5. Los puntos de extracción deben ser activados al menos en el mismo periodo para que se inicie la extracción 
        Drawpextract_61 = self.undergroundModel.addConstrs((gp.quicksum(self.x_dt[d, tau] for tau in range(ti+1)) >= self.z_dt[d, ti]  
                                            for d in self.drawpoint for ti in self.t_S), "Drawpextract_61")


        #6. Existe una cantidad máxima y mínima de drawpoints a abrir en cada periodo.
        Drawpextract_64_1 = self.undergroundModel.addConstrs((gp.quicksum(self.x_dt[d, ti] for d in self.drawpoint) <= self.NU_nt[ti] for ti 
                                                        in self.t_S)
                                                        ,"Drawpextract_64_1")

        Drawpextract_64_2 = self.undergroundModel.addConstrs((gp.quicksum(self.x_dt[d, ti] for d in self.drawpoint) >= self.NL_nt[ti] for ti 
                                                        in self.t_S)
                                                        , "Drawpextract_64_2")

        #7. Existe una m ́axima cantidad de drawpoints a extraer por periodo.
        Drawpextract_65 = self.undergroundModel.addConstrs((gp.quicksum(self.z_dt[d, ti] for d in self.drawpoint) <= self.N_t[ti] for ti in self.t_S)
                                                    , "Drawpextract_65")


        #8. Si iniciamos la extracción de un drawpoint esta debe durar por su duraci ́on determinada.
        ## Un drawpoint solamente puede ser extraido por un preiodo pre determinado (A_d)
        Drawpextract_62 = self.undergroundModel.addConstrs((gp.quicksum(self.z_dt[d, ti] for ti in self.t_S)  <= self.A_d[ti]  for d in self.drawpoint
                                                    for ti in self.t_S), "Drawp_62")

        ## Una vez se inicia extrayendo de un drawpoint, se continua extrayendo sin interrupción
        Drawpextract_63 = self.undergroundModel.addConstrs((self.A_d[ti] *(self.z_dt[d, ti] - self.z_dt[d, ti+1]) 
                                            - gp.quicksum(self.z_dt[d, tau] for tau in range(ti+1)) <= 0 
                                            for d in self.drawpoint for ti in range(0,max(self.t_S))), "Drawpextract_63")

        #9. Relación de variables, el porcentaje a extraer es 0 si no se extra un drawpoint.
        Drawpextract_66 = self.undergroundModel.addConstrs((y_dt[d, ti] <= self.z_dt[d, ti] for d in self.drawpoint for ti in self.t_S),
                                                    "Drawpextract_66")

        #10. Existe una tasa m ́ınima de extracci ́on para cada drawpoint a extraer.
        Drawpextract_67_1 = self.undergroundModel.addConstrs((self.RL_dt[ti] * self.z_dt[d, ti]  <=  y_dt[d, ti] for d in self.drawpoint
                                                        for ti in self.t_S), "Drawpextract_67_1")

        #11. La altura a extraer debe ser mayor a una cantidad m ́ınima.
        #rest_11 = self.undergroundModel.addConstrs((gp.quicksum(y_dt[d,ti] for ti in self.t_S)>= self.colHeight for d in self.drawpoint))

        #12. No podemos extraer más del 100 % de un drawpoint.
        Reserver_cnst = self.undergroundModel.addConstrs((gp.quicksum(y_dt[d, ti] for ti in self.t_S) <= 1 for d in self.drawpoint),
                                                    "Reserver_cnst")

        #13. Si se activa un drawpoint, se extrae en ese periodo
        rest_13 = self.undergroundModel.addConstrs(self.x_dt[d,ti] <= self.z_dt[d, ti] for d in self.drawpoint for ti in self.t_S)

        #14. Naturaleza de variables.

        #15. Existe una m ́axima cantidad de drawpoints a extraer por periodo.
        rest_15= self.undergroundModel.addConstrs((gp.quicksum(self.x_dt[d, ti] for d in self.drawpoint) <= self.N_t[ti] for ti in self.t_S)
                                                    , "Drawpextract_65")

        
        #16. Restricción sobre el inicio de la extracci ́on de los drawpoints.
        DP_Sup = self.undergroundModel.addConstrs((gp.quicksum(self.x_dt[self.predecessor[l][0], s]*(max(self.t_S)-s+1) for s in self.t_S) <=
                                    gp.quicksum(self.x_dt[self.predecessor[l][1], s]*(max(self.t_S)-s+1) for s in self.t_S)  
                                    for l in range(len(self.predecessor))), "DP_Sup")

        #17. Restricci ́on sobre la extracci ́on de los drawpoints.
        restricion_17 = self.undergroundModel.addConstrs((gp.quicksum(self.z_dt[self.predecessor[l][0], s]*(max(self.t_S)-s+1) for s in self.t_S) <=
                                    gp.quicksum(self.z_dt[self.predecessor[l][1], s]*(max(self.t_S)-s+1) for s in self.t_S)  
                                    for l in range(len(self.predecessor))), "DP_Sup")
        
        
       
        
        #Conjuntos para el crown pillar

        #Restricciones del crown pillar
        #Variable 1 si y solo si el crown pillar esta ubicado en la elevaci ́on v, 0 en otro caso.
        self.w_v = self.undergroundModel.addVars(self.V, vtype=GRB.BINARY, name="w")
        self.theta = self.undergroundModel.addVar(vtype=GRB.CONTINUOUS,name="theta")


        pillar_2 = self.undergroundModel.addConstrs(gp.quicksum(y_dt[d, ti] for d in self.drawpoint
                                                        for ti in self.t_S) <= self.rho_v[v] * self.w_v[v] + (1 - self.w_v[v]) for v in self.V)
       
        pillar_3 = self.undergroundModel.addConstr(gp.quicksum(self.w_v[v] for v in self.V) == 1)

        theta_restriction_1 = self.undergroundModel.addConstr(-gp.GRB.INFINITY <= self.theta)
        theta_restriction_2 = self.undergroundModel.addConstr(self.theta <= 800000000)

         #Función objetivo
        undergroundObjectiveFunction = self.theta + gp.quicksum( y_dt[d, ti]*((((self.p_t * self.LEY_D[d] -self.C_pdt[d] ) * self.Q_d[d])-(self.C_mdt[d]*self.G_d[d]))/
                                        ((1+self.desc)**(self.t_S[ti]))) for ti in self.t_S for d in self.drawpoint) 

        self.undergroundModel.setObjective(undergroundObjectiveFunction, GRB.MAXIMIZE)
        self.undergroundModel.Params.MIPGap = 0.01

    def optimize(self):
        self.undergroundModel.optimize()
        lista_variable_Integrado = (self.undergroundModel.getAttr(GRB.Attr.X, self.undergroundModel.getVars()))
        solucion = self.undergroundModel.objVal
        runtime = self.undergroundModel.Runtime
        gap_f = self.undergroundModel.MIPGap
        
        return {key:value.X for key,value in zip(self.w_v, self.w_v.values())}, self.theta