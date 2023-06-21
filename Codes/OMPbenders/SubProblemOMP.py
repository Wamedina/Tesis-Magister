import sys  
sys.path.insert(0, '../AuxiliarCodes/')

from   gurobipy   import GRB
from globalFunctions import getNumberOfBlocksInADimension
from openPitFunctions import finalBlock
from itertools import chain
import re
import subprocess as sp


class SubProblem:
   def __init__(self, database, minHeightUnderground, maxHeightUnderground,numberOfPeriods, safetyLevel):
      self.database = database
      self.numberOfPeriods = numberOfPeriods
      self.minHeightUnderground = minHeightUnderground
      self.maxHeightUnderground = maxHeightUnderground
      self.safetyLevel = safetyLevel
      self.numberOfDestinations = 1
      self.basePrice = 3791.912
      self.desc = 0.1

   def setParameters(self):
      self.setOpenPitVariables()
      self.getOpenPitInfo()
      self.setOpenPitParameters()
      self.setOpenPitMineLimits()
      self.setPossibleHeights()
      self.setHeightSets()

   def execute(self, B_v, isFinalIteration = False):
      self.createOmpInput(B_v)
      return (self.executeOmp(isFinalIteration))

   def setOpenPitVariables(self):
      self.openPitBlocksLength = self.database['X'].to_dict() 
      self.openPitBlocksWidth = self.database['Y'].to_dict() 
      self.openPitBlocksHeight = self.database['Z'].to_dict() #Los bloques se orientan de abajo hacia arriba, el bloque 0 es el que esta más abajo, 784 bloques
      self.L_b = self.database['Ton'].to_dict() #openPitBlockTonnage
      self.o_b = self.database['Mineral'].to_dict() #openPitBlockMineral
      self.openPitBlockRecovery = self.database['Recuperación'].to_dict() #openPitBlockRecovery
      self.openPitCopperLaw = self.database['%Cu'].to_dict() #openPitCopperLaw
      self.c_pbt = self.database['CPlanta CA'].to_dict() #openPitPlantCapacity
      self.c_mbt = self.database['CMina CA'].to_dict() #openPitMineCapacity

   def getOpenPitInfo(self):
      self.openPitBlocks = [i for i in range(len(self.openPitBlocksLength.values()))]

   def setOpenPitParameters(self):
      #OpenPit Parameters
      self.t_C   = {period : period + 1 for period in range(self.numberOfPeriods)}
      self.RMu_t = {period : 25806600.0 for period in range(self.numberOfPeriods)}#Superior infinita, 0 por abajo Originales: 13219200
      self.RMl_t = {period : 0.0/3 for period in range(self.numberOfPeriods)}#Valor original 8812800.0
      self.RPu_t = {period : 17777880.0 for period in range(self.numberOfPeriods)}#Valor original 10933380.0
      self.RPl_t = {period : 0/3 for period in range(self.numberOfPeriods)}#Valor original 7288920.0 
      self.qu_t  = {period : 1 for period in range(self.numberOfPeriods)}#Leyes promedio maxima y minima.
      self.ql_t  = {period : 0.0001 for period in range(self.numberOfPeriods)}
      self.delta = {period: 0 for period in range(self.numberOfPeriods)}
      self.maxTimeOpenPit = self.t_C[max(self.t_C)]


   def setOpenPitMineLimits(self):
      self.openPitBlocksLengthLimits = getNumberOfBlocksInADimension(self.openPitBlocksLength)
      self.openPitBlocksWidthLimits = getNumberOfBlocksInADimension(self.openPitBlocksWidth)
      self.openPitBlocksHeightLimits = getNumberOfBlocksInADimension(self.openPitBlocksHeight)
      self.predecessorBlock = self.setPredecessorBlocks()

   def setPredecessorBlocks(self):
      self.predecessorBlocks = finalBlock(self.openPitBlocks, self.openPitBlocksLengthLimits,self.openPitBlocksWidthLimits, self.openPitBlocksHeightLimits)
  
   def setPossibleHeights(self):
      self.blockHeight, self.maxHeight, self.minHeight, self.numOfDifferentsBlocks = self.openPitBlocksHeightLimits
   
   def setHeightSets(self):
      #Acá hay que redifinir self.B_v para que tenga las alturas de maxheight al sumarle el safetylvl

      self.V = [height for height in chain(range(self.minHeight,self.maxHeight,self.blockHeight), [self.maxHeight])]
      self.B_v = {}
      self.rho_v = {v:( ((v- self.safetyLevel - self.minHeightUnderground)/(self.maxHeightUnderground - self.minHeightUnderground)) if v - self.minHeightUnderground > 0 else 0 ) for v in self.V}

      for v in self.V:
         numberOfBlocksBelowV = (self.openPitBlocksLengthLimits[3]*self.openPitBlocksWidthLimits[3])*((v-self.minHeight)/self.openPitBlocksHeightLimits[0])
         blocksBelowV = [block for block in range(int(numberOfBlocksBelowV)) if not numberOfBlocksBelowV == 0]
         self.B_v[v] = blocksBelowV
         
   def createOmpInput(self, infeasibleBlocks):
      self.writeProblemFile()
      self.writeBlocksFile(infeasibleBlocks)
      self.writePrecFile()
      self.writeParamsFile()
   
   def writeProblemFile(self):
         with open('../FilesToExecuteOmpOpenPit/files/openPit.prob', 'w') as f:
            numberOfDestinations = 'NDESTINATIONS: ' + str(self.numberOfDestinations)
            numberOfPeriods = 'NPERIODS: ' + str(self.numberOfPeriods)
            objective = 'OBJECTIVE: 0 1'
            duration = 'DURATION: 2'
            discountRate = 'DISCOUNT_RATE: '+ str(self.desc)#/self.numberOfPeriods)
            
            tonUpConstraint = 'CONSTRAINT: 0 3 P * L '
            for rmu in self.RMu_t.values():
               tonUpConstraint +=str(rmu) + " "

            tonLowContraint = 'CONSTRAINT: 1 3 P * G '
            for rml in self.RMl_t.values():
               tonLowContraint +=str(rml) + " "
            
            matUpConstraint = 'CONSTRAINT: 2 4 P * L '
            for rpu in self.RPu_t.values():
               matUpConstraint +=str(rpu) + " "

            matLowConstraint = 'CONSTRAINT: 3 4 P * G '
            for rpl in self.RPl_t.values():
               matLowConstraint +=str(rpl) + " "
            
            #las siguientes dos restricciones tienen 0 en vez de qut y qlt ya que pasamos la desigualdad hacia la derecha en las lineas 144 y 145
            copperLawUpConstraint = 'CONSTRAINT: 4 5 B * L ' 
            for qut in self.qu_t.values():
               copperLawUpConstraint += "0 "

            copperLawLowConstraint = 'CONSTRAINT: 5 6 B * G '
            for qlt in self.ql_t.values():
               copperLawLowConstraint +="0 "

            infeasibleBlocks = 'CONSTRAINT: 6 7 P * L '
            for delta in self.delta.values():
               infeasibleBlocks +=str(delta) + " "
            
            constraints = [tonUpConstraint, tonLowContraint, matUpConstraint, matLowConstraint, copperLawUpConstraint,copperLawLowConstraint,infeasibleBlocks]
            self.numberOfConstraints = len(constraints)
            self.nConstraints = 'NCONSTRAINTS: ' + str(self.numberOfConstraints)
            f.write('{}\n{}\n{}\n{}\n{}\n{}\n'.format(numberOfDestinations,numberOfPeriods, objective,duration,discountRate,self.nConstraints))
            f.write('{}\n{}\n{}\n{}\n{}\n{}\n{}\n'.format(*constraints))

   def writeBlocksFile(self, numberOfInvaiableBlocks):
      #print(f'Se optimizó el subproblema con {numberOfInvaiableBlocks} bloques infactibles')
      with open('../FilesToExecuteOmpOpenPit/files/openPit.blocks', 'w') as f:
         for block in self.openPitBlocks:
            index = block
            value = ((self.basePrice*self.openPitCopperLaw[block]-self.c_pbt[block])*self.o_b[block])-(self.c_mbt[block]*self.L_b[block])
            duration = 1 #Cuanto se demora en extraer el bloque
            ton = self.L_b[block]
            mineral = self.o_b[block]
            copperLawUpper = self.openPitCopperLaw[block] * self.L_b[block] - self.qu_t[0] * self.L_b[block]
            copperLawLower = self.openPitCopperLaw[block] * self.L_b[block] - self.ql_t[0] * self.L_b[block]

            #1 si no se puede extraer, 10977 última capa, los bloques van de abajo hacia arriba, 0 primer bloque de abajo, 10977 última capa hacia arriba, con 10975 la sol es vacia
            if block < numberOfInvaiableBlocks:
               f.write(('{} {} {} {} {} {} {} {}\n').format(index, value, duration, ton, mineral,copperLawUpper, copperLawLower, 1))
            else:
               f.write(('{} {} {} {} {} {} {} {}\n').format(index, value, duration, ton, mineral,copperLawUpper, copperLawLower, 0))
                 
   def writePrecFile(self):
      with open('../FilesToExecuteOmpOpenPit/files/openPit.prec', 'w') as f:
         for index,blockList in enumerate(self.predecessorBlocks):
            predecessorLine = str(len(blockList))
            for block in blockList:
               if block == index:
                  predecessorLine = " 0"
                  break
               else:
                  predecessorLine +=" " + str(block)
            f.write("{} {}\n".format(index, predecessorLine))
            
   def writeParamsFile(self):
      with open('../FilesToExecuteOmpOpenPit/params/openPit.params', 'w') as f:
         f.write("""USE_DISPLAY: 1
WRITE.LP.SOLUTION: 1
WRITE.IP.SOLUTION: 1
CPIT: 1
PP.ULTIMATE_PIT: 1
PP.FORCE_UPIT: 1
PP.EARLY_START: 1
PP.WASTE_OPTION: 1
PP.ELIM_NULL: 0
PP.TRANSITIVE_REDUCTION: 0
AG.USE_BLOCK_AGGREGATION: 0
AG.BLOCK_AGGREGATION: 0
OPTMETHOD: 0
CG.ONE_DESTINATION: 1
CG.IMPLICIT: 0
CG.USE_DISPLAY: 1
CG.MAX_ITER: -1
CG.TARGET_GAP: 0.0001
CG.MAX_TIME: -1
CG.USE_KSTEP: 0
CG.KSTEP_K: 10
CG.MASTER_NTHREADS: 4
CG.DISPLAY_DUALS: 1
HE.TOPOSORT: 1
HE.FTOPOSORT: 0
HE.NALPHA_POINTS: 50
HE.OPT_DESTINATIONS: 1
HE.NAIVE: 0
HE.NAIVE_INTSOLLIM: 1000
HE.NAIVE_EPGAP: 0.01
HE.NAIVE_TILIM: 14400
CP.DYNAMIC_CUTS: 0
CP.CLIQUES: 0
CP.MINW: 0
CP.DELAYED_PRECEDENCES: 0
CONSTRAINT_PROGRAMMING: 0
CPROG.GAP_LIMIT: 0.01
CPROG.CP_TIME_LIMIT: 28800
CPROG.EX_TIME_LIMIT: 28800
CPROG.HOT_START: 1
CPROG.NTHREADS: 8""")

   def executeOmp(self, isFinalIteration):
      output = sp.getoutput("./omp.sh ../FilesToExecuteOmpOpenPit/files/openPit.* ../FilesToExecuteOmpOpenPit/params/dbs_duals.params")
      #print(output)
      return self.getPiAndObjectiveValue(output, isFinalIteration)
   
   def getPiAndObjectiveValue(self, output, isFinalIteration):
      objective_value_to_use = 0
      if isFinalIteration:
         objective_value_to_use = 1
      pi_positions = [positions.start() for positions in re.finditer("rhs= 0.000000", output)]
      pi_t = dict.fromkeys(self.t_C,0)
      for pos in pi_positions:
         pi_value = float(output[pos-48: pos].split()[-3])
         pi_index = float(output[pos-48: pos].split()[-5])
         period_index = pi_index - self.numberOfPeriods * (self.numberOfConstraints - 1)
         pi_t[period_index] = pi_value

      objective_value_positions = [positions.start() for positions in re.finditer("Objective Value ", output)]
      objective_value = float(output[objective_value_positions[objective_value_to_use]: objective_value_positions[objective_value_to_use]+100].split()[-3])
      return objective_value, pi_t 
