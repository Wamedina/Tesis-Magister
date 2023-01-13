import gurobipy   as     gp
from   gurobipy   import GRB
from globalFunctions import getNumberOfBlocksInADimension
from openPitFunctions import finalBlock


class OpenPitModel:
   def __init__(self, database, numberOfPeriods):
      self.database = database
      self.numberOfPeriods = numberOfPeriods
      self.basePrice = 3791.912

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
      self.openPitBlockTonnage = self.database['Ton'].to_dict() 
      self.openPitBlockMineral = self.database['Mineral'].to_dict()
      self.openPitBlockRecovery = self.database['Recuperación'].to_dict() 
      self.openPitCopperLaw = self.database['%Cu'].to_dict()
      self.openPitPlantCapacity = self.database['CPlanta CA'].to_dict()
      self.openPitMineCapacity = self.database['CMina CA'].to_dict()

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
      self.objValue, self.variableValues, self.runtime, self.gap = self.openPitModel(self.openPitBlocks, self.predecessorBlock,
                                                                  self.openPitBlockTonnage, self.openPitBlockMineral, self.openPitCopperLaw, self.openPitMineCapacity,self.openPitPlantCapacity,
                                                                  self.t_C,self.RMu_t,self.RMl_t,self.RPu_t,self.RPl_t,self.qu_t,self.ql_t,self.maxTimeOpenPit,
                                                                  self.basePrice)

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


   def openPitModel(self, bloques_CA,predecessor_block,
                             TON_C,MIN_C,LEY_C,CM_CA_C,CP_CA_C,
                             t_C,RMu_t,RMl_t,RPu_t,RPl_t,qu_t,ql_t,time_max_C,
                             basePrice):
    
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
      
      FO_OP = gp.quicksum(x_bt_OP[ti, b]*((((0.7*basePrice*LEY_C[b]-CP_CA_C[b])*MIN_C[b])-(CM_CA_C[b]*TON_C[b]))/((1+0.1)**t_C[ti]))
                  for ti in t_C for b in bloques_CA)
      
      openPitModel.setObjective(FO_OP, GRB.MAXIMIZE)
      openPitModel.Params.MIPGap = 0.01
      openPitModel.optimize()
      #openPitModel.Params.MIPGap = 0.20
      lista_variable_Integrado = (openPitModel.getAttr(GRB.Attr.X, openPitModel.getVars()))
      solucion = openPitModel.objVal
      runtime = openPitModel.Runtime
      gap_f = openPitModel.MIPGap
      
      return solucion, lista_variable_Integrado, runtime, gap_f