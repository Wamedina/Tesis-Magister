import pandas as pd
from openPitModel import *
from openPitFunctions import predecessorBlocks
from drawpointFunction  import drawpointFunction
from integratedModel   import setIntegratedModel
from globalFunctions import getNumberOfBlocksInADimension
from plotResults   import plotResults


class Main:
    def __init__(self, path, undergroundDatabaseName, openPitDatabaseName):
        self.path = path
        self.openPitDatabaseName = openPitDatabaseName
        self.undergroundDatabaseName = undergroundDatabaseName
        self.runIntegratedModel = False
        self.runOpenPitModel = True
        self.runUndergroundModel = False
        self.numberOfPeriods = 3
        
    def execute(self):
        print("Setting MineDatabases")
        self.setMineDatabases(path, self.openPitDatabaseName, self.undergroundDatabaseName)

        if self.runIntegratedModel:
            pass
        
        elif self.runOpenPitModel and self.runUndergroundModel:
            pass

        elif self.runOpenPitModel:
            self.executeOpenPitModel()
        
        elif self.runUndergroundModel:
            self.executeUndergroundModel()


        
        print("Getting Block Information")
        self.getBlockInfo()
        print("Setting Parameters to evaluate")
        self.setParametersToEvaluate()
        print("Setting Global Parameters")
        self.setGlobalParameters()
        print("Getting underground variables")
        self.getUndergroundVariables()
        print("Setting Model")
        self.setModelAndGetResults()
        print("Plotting results")
        plotResults(self.variableValues, self.CA_blocks, self.openPitBlocksLenghtLimits, self.openPitBlocksWidthLimits,
        self.openPitBlocksHeightLimits, self.undergroundBlocksWidthLimits, self.undergroundBlocksHeightLimits)
        print(self.variableValues)
        #self.getResults(self.model)


    def executeOpenPitModel(self):
        print("Setting Open Pit Variables")
        self.setOpenPitVariables()

    def executeUndergroundModel(self):
        print("Setting Underground Variables")
        self.setUndergroundVariables()


    def setMineDatabases(self, path, openPitDatabaseName,undergroundDatabaseName ):
        self.openMineDataframe = pd.read_excel(path+openPitDatabaseName, engine="openpyxl")
        self.undergroundMineDataframe = pd.read_excel(path+undergroundDatabaseName, engine="openpyxl")
    
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
        superiorBlock = predecessorBlocks(self.CA_blocks, self.openPitBlocksLenghtLimits,self.openPitBlocksWidthLimits, self.openPitBlocksHeightLimits)
        for i in range(len(self.CA_blocks)):
            for j in superiorBlock[i]:
                aux_1 = []
                aux_1.append(self.CA_blocks[i])
                aux_1.append(j)
                predecessorBlock.append(aux_1)
        return predecessorBlock

    def setMineLimits(self):
        self.undergroundBlocksLenghtLimits = getNumberOfBlocksInADimension(self.undergroundBlocksLenght)
        self.undergroundBlocksWidthLimits = getNumberOfBlocksInADimension(self.undergroundBlocksWidth)
        self.undergroundBlocksHeightLimits = getNumberOfBlocksInADimension(self.undergroundBlocksHeight)

        self.openPitBlocksLenghtLimits = getNumberOfBlocksInADimension(self.openPitBlocksLenght)
        self.openPitBlocksWidthLimits = getNumberOfBlocksInADimension(self.openPitBlocksWidth)
        self.openPitBlocksHeightLimits = getNumberOfBlocksInADimension(self.openPitBlocksHeight)

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

    def getBlockInfo(self):
        self.CA_blocks = [i for i in range(len(self.openPitBlocksLenght.values()))]
        self.S_blocks = [i for i in range(len(self.undergroundBlocksLenght.values()))]

    def setParametersToEvaluate(self):
        #OpenPit Parameters
        self.t_C   = {period : period + 1 for period in range(self.numberOfPeriods+1)}
        self.RMu_t = {period : 132192000000000000000000.0 for period in range(self.numberOfPeriods+1)}#Superior infinita, 0 por abajo Originales: 13219200
        self.RMl_t = {period : 0 for period in range(self.numberOfPeriods+1)}#Valor original 8812800.0
        self.RPu_t = {period : 1093338000000000000000000.0 for period in range(self.numberOfPeriods+1)}#Valor original 10933380.0
        self.RPl_t = {period : 0 for period in range(self.numberOfPeriods+1)}#Valor original 7288920.0 
        self.qu_t  = {period : 1 for period in range(self.numberOfPeriods+1)}#Leyes promedio maxima y minima.
        self.ql_t  = {period : 0 for period in range(self.numberOfPeriods+1)}

        #Underground Parameters
        self.t_S   = {period : period + 1 for period in range(self.numberOfPeriods+1)}
        self.MU_mt = {period : 25806600.0  for period in range(self.numberOfPeriods+1)}
        self.ML_mt = {period : 17204400.0  for period in range(self.numberOfPeriods+1)}
        self.MU_pt = {period : 17777880.0  for period in range(self.numberOfPeriods+1)}
        self.ML_pt = {period : 11851920.0  for period in range(self.numberOfPeriods+1)}
        self.qU_dt = {period : 1 for period in range(self.numberOfPeriods+1)}
        self.qL_dt = {period : 0 for period in range(self.numberOfPeriods+1)}
        self.A_d   = {period : 2 for period in range(self.numberOfPeriods+1)}
        self.NU_nt = {period : 59 for period in range(self.numberOfPeriods+1)}# 
        self.NL_nt = {period : 32 for period in range(self.numberOfPeriods+1)}
        self.N_t   = {period : 57 * (1 + period) for period in range(self.numberOfPeriods+1)}
        self.RL_dt = {period : 0.3 for period in range(self.numberOfPeriods+1)}
        self.RU_dt = {period : 0.7 for period in range(self.numberOfPeriods+1)}
            
        self.maxTimeOpenPit = self.t_C[max(self.t_C)]
        self.maxTimeUnderground = self.t_S[max(self.t_S)]
    
    def getUndergroundVariables(self):
        DP_init = 0       #### Tipo de extracción
        pos_x_f = 730     
        pos_y_f = 910     
        orientationToExtractTheDrawpoints = 0
        
        self.drawpoint, self.TON_d, self.MIN_D,self.LEY_D, self.C_P_D, self.C_M_D, self.predecessor, self.x_draw,self.y_draw, self.z_draw = drawpointFunction(
        self.pos_x, self.pos_y, self.pos_z, self.colHeight, DP_init, self.undergroundBlocksLenghtLimits, self.undergroundBlocksWidthLimits, self.undergroundBlocksHeightLimits, self.undergroundBlockTonnage, self.undergroundCP_S, self.undergroundCM_S, self.undergroundBlockMineral,
        self.undergroundCopperLaw, pos_x_f, pos_y_f,orientationToExtractTheDrawpoints)

    def setModelAndGetResults(self):
        self.objValue, self.variableValues, self.runtime, self.gap = setIntegratedModel(self.CA_blocks,self.drawpoint,self.openPitBlocksHeight,self.dif_centroide,self.pos_z,self.colHeight,self.securityLevel,self.predecessorBlock,self.predecessor,
                         self.openPitBlockTonnage,self.openPitBlockMineral,self.openPitBlockRecovery,self.openPitCopperLaw,self.openPitVariableExtractionCosts,self.openPitExtractionFixedCosts,
                         self.TON_d,self.MIN_D,self.undergroundBlockRecovery,self.LEY_D,self.C_P_D,self.C_M_D,
                         self.t_C ,self.RMu_t,self.RMl_t,self.RPu_t,self.RPl_t,self.qu_t ,self.ql_t,self.maxTimeOpenPit,
                         self.t_S ,self.MU_mt,self.ML_mt,self.MU_pt,self.ML_pt,self.qU_dt,self.qL_dt,self.A_d,self.NU_nt,self.NL_nt,self.N_t ,self.RL_dt ,self.RU_dt ,self.maxTimeUnderground,
                         0.01,self.basePrice,self.mineCostPonderator,self.basePlantCostPonderator)



path = "C:/Users/Williams/Desktop/Tesis Magister/Magister/ThesisCode/MainCode/Databases/integratedModel/"
undergroundDatabaseName = 'Modelo_F_OG.xlsx'
openPitDatabaseName = 'Modelo_F_OG_4_4_4.xlsx'
main = Main(path, undergroundDatabaseName, openPitDatabaseName)
main.execute()


