import gurobipy   as     gp
from   gurobipy   import GRB
from globalFunctions import getNumberOfBlocksInADimension
from openPitFunctions import finalBlock


class Subproblem:
   def __init__(self, database, numberOfPeriods):
      self.database = database
      self.numberOfPeriods = numberOfPeriods
      self.basePrice = 3791.912
      self.desc = 0.1

   def execute(self):
      self.setOpenPitVariables()
      self.getOpenPitInfo()
      self.setOpenPitParameters()
      self.setOpenPitMineLimits()
      #self.setFinalParameters()
      self.setModelAndGetResults()
      return self.objValue, self.variableValues, self.runtime, self.gap

   def setOpenPitVariables(self):
      self.openPitBlocksLenght = self.database['X'].to_dict() 
      self.openPitBlocksWidth = self.database['Y'].to_dict() 
      self.openPitBlocksHeight = self.database['Z'].to_dict() 
      self.L_b = self.database['Ton'].to_dict() #openPitBlockTonnage
      self.o_b = self.database['Mineral'].to_dict() #openPitBlockMineral
      self.openPitBlockRecovery = self.database['Recuperación'].to_dict() #openPitBlockRecovery
      self.openPitCopperLaw = self.database['%Cu'].to_dict() #openPitCopperLaw
      self.c_pbt = self.database['CPlanta CA'].to_dict() #openPitPlantCapacity
      self.c_mbt = self.database['CMina CA'].to_dict() #openPitMineCapacity

   def getOpenPitInfo(self):
      self.openPitBlocks = [i for i in range(len(self.openPitBlocksLenght.values()))]

   def setOpenPitParameters(self):
      #OpenPit Parameters
      self.t_C   = {period : period + 1 for period in range(self.numberOfPeriods)}
      self.RMu_t = {period : 13219200.0 for period in range(self.numberOfPeriods)}#Superior infinita, 0 por abajo Originales: 13219200
      self.RMl_t = {period : 8812800.0 for period in range(self.numberOfPeriods)}#Valor original 8812800.0
      self.RPu_t = {period : 10933380.0 for period in range(self.numberOfPeriods)}#Valor original 10933380.0
      self.RPl_t = {period : 0 for period in range(self.numberOfPeriods)}#Valor original 7288920.0 
      self.qu_t  = {period : 1 for period in range(self.numberOfPeriods)}#Leyes promedio maxima y minima.
      self.ql_t  = {period : 0 for period in range(self.numberOfPeriods)}
      self.ql_t  = {period : 0 for period in range(self.numberOfPeriods)}
      self.maxTimeOpenPit = self.t_C[max(self.t_C)]

   def setOpenPitMineLimits(self):
      self.openPitBlocksLenghtLimits = getNumberOfBlocksInADimension(self.openPitBlocksLenght)
      self.openPitBlocksWidthLimits = getNumberOfBlocksInADimension(self.openPitBlocksWidth)
      self.openPitBlocksHeightLimits = getNumberOfBlocksInADimension(self.openPitBlocksHeight)
      self.predecessorBlock = self.setPredecessorBlock()


   def setModelAndGetResults(self):
      self.objValue, self.variableValues, self.runtime, self.gap = self.openPitModel()

   def setPredecessorBlock(self):
        predecessorBlock = []
        superiorBlock = finalBlock(self.openPitBlocks, self.openPitBlocksLenghtLimits,self.openPitBlocksWidthLimits, self.openPitBlocksHeightLimits)
        for i in range(len(self.openPitBlocks)):
            for j in superiorBlock[i]:
                aux_1 = []
                aux_1.append(self.openPitBlocks[i])
                aux_1.append(j)
                predecessorBlock.append(aux_1)
        return predecessorBlock


   def openPitModel(self):#,w_opt):
    
      openPitModel = gp.Model(name = 'Open Pit Model')

      #6. Naturaleza de variables
      x_bt = openPitModel.addVars(self.t_C, self.openPitBlocks, vtype=GRB.CONTINUOUS, name="x")

      #1. Restricci ́on sobre la cantidad de tonelaje m ́axima y m ́ınima a extraer en cada periodo.
      Ton_Up  = openPitModel.addConstrs((gp.quicksum(x_bt[ti, b]*self.L_b[b] for b in self.openPitBlocks) 
                              <= self.RMu_t[ti] for ti in self.t_C), "Ton_max")
      Ton_low = openPitModel.addConstrs((gp.quicksum(x_bt[ti, b]*self.L_b[b] for b in self.openPitBlocks) 
                              >= self.RMl_t[ti] for ti in self.t_C), "Ton_min")

      #2. Restricci ́on sobre la cantidad de material m ́axima y m ́ınima a extraer en cada periodo.
      Mat_Up_OP = openPitModel.addConstrs((gp.quicksum(x_bt[ti, b]*self.o_b[b] for b in self.openPitBlocks) <= 
                              self.RPu_t[ti] for ti in self.t_C), "Mat_max")
      Mat_low_OP = openPitModel.addConstrs((gp.quicksum(x_bt[ti, b]*self.o_b[b] for b in self.openPitBlocks) >= 
                              self.RPl_t[ti] for ti in self.t_C), "Mat_min")

      #3. Restricci ́on de precedencia de los bloques a extraer, debemos extraer los 5 bloques superiores al bloque objetivo para sacar a este
      BLOCK_SUP_OP = openPitModel.addConstrs((gp.quicksum(x_bt[s, self.predecessorBlock[l][0]]*(self.maxTimeOpenPit-s+1) for s in self.t_C) <= 
                                       gp.quicksum(x_bt[s, self.predecessorBlock[l][1]]*(self.maxTimeOpenPit-s+1) for s in self.t_C)  
                                    for l in range(len(self.predecessorBlock))), "Superior_Block")

      #4. Restricci ́on sobre la ley m ́axima y m ́ınima por periodo.
      GQC_Up_OP = openPitModel.addConstrs((gp.quicksum(x_bt[ti, b]*self.L_b[b]*self.openPitCopperLaw[b] for b in self.openPitBlocks) <=
                           self.qu_t[ti] * gp.quicksum(x_bt[ti, b]*self.L_b[b] for b in self.openPitBlocks) for ti in self.t_C), 
                              "GQC_Up")

      GQC_low_OP = openPitModel.addConstrs((gp.quicksum(x_bt[ti, b]*self.L_b[b]*self.openPitCopperLaw[b] for b in self.openPitBlocks) >=
                           self.ql_t[ti] * gp.quicksum(x_bt[ti, b]*self.L_b[b] for b in self.openPitBlocks) for ti in self.t_C), 
                              "GQC_LOW")

      #5. Podemos extraer el bloque en un solo periodo.
      Reserve_cons_OP = openPitModel.addConstrs((gp.quicksum(x_bt[ti, b] for ti in self.t_C) <= 1 for b in self.openPitBlocks), 
                              "Reserve_cons")

      #Función objetivo
      FO_OP = gp.quicksum(x_bt[ti, b]*((((self.basePrice*self.openPitCopperLaw[b]-self.c_pbt[b])*self.o_b[b])-(self.c_mbt[b]*self.L_b[b]))/((1+self.desc)**self.t_C[ti]))
                  for ti in self.t_C for b in self.openPitBlocks)

      ##FALTA DEFINIR LOS CONJUNTOS B_v, V 

      #Variable 1 si y solo si el crown pillar esta ubicado en la elevaci ́on v, 0 en otro caso.
      #w_v = openPitModel.addVars(self.t_C, self.openPitBlocks, vtype=GRB.CONTINUOUS, name="w")

      #Restricciones del crown pillar
      #pillar_2 = openPitModel.addConstrs(gp.quicksum(x_bt[ti, b] for b in self.B_v)<=1- w_v[v] for v in V for ti in self.t_C)

      #fixed_position = openPitModel.addConstrs(w_v == w_opt)
      
      openPitModel.setObjective(FO_OP, GRB.MAXIMIZE)
      openPitModel.Params.MIPGap = 0.01
      openPitModel.optimize()
      lista_variable_Integrado = (openPitModel.getAttr(GRB.Attr.X, openPitModel.getVars()))
      solucion = openPitModel.objVal
      runtime = openPitModel.Runtime
      gap_f = 1#openPitModel.MIPGap
      
      return solucion, lista_variable_Integrado, runtime, gap_f