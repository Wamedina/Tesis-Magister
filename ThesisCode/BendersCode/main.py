import pandas as pd
from Subproblem import OpenPitModel
from MasterProblem import UndergroundModel


class Main:
    def __init__(self, path, undergroundDatabaseName, openPitDatabaseName):
        self.path = path
        self.openPitDatabaseName = openPitDatabaseName
        self.undergroundDatabaseName = undergroundDatabaseName
        self.runOpenPitModel = False
        self.runUndergroundModel = True
        self.numberOfPeriods = 4
        self.models = []
        
    def execute(self):
        print("Setting MineDatabases")
        self.setMineDatabases()
        self.createModels()
        self.getResults()

        #plotResults(self.variableValues, self.CA_blocks, self.openPitBlocksLenghtLimits, self.openPitBlocksWidthLimits,
        #self.openPitBlocksHeightLimits, self.undergroundBlocksWidthLimits, self.undergroundBlocksHeightLimits)
        #print(self.variableValues)
        #self.getResults(self.model)

    def setMineDatabases(self):
        if self.runUndergroundModel:
            self.undergroundMineDataframe = pd.read_excel(self.path+self.undergroundDatabaseName, engine="openpyxl")

        if self.runOpenPitModel:
            self.openMineDataframe = pd.read_excel(self.path+self.openPitDatabaseName, engine="openpyxl")
    
    def createModels(self):

        if self.runUndergroundModel:
            self.createUndergroundModel()

        if self.runOpenPitModel:
            self.createOpenPitModel()


    def createUndergroundModel(self):
        self.undergroundModel = UndergroundModel(self.undergroundMineDataframe, self.numberOfPeriods)
        self.models.append(self.undergroundModel)

    def createOpenPitModel(self):
        self.openPitModel = OpenPitModel(self.openMineDataframe, self.numberOfPeriods)
        self.models.append(self.openPitModel)

    def getResults(self):
        for model in self.models:
            if isinstance(model, UndergroundModel):
                self.undergroundObjValue, self.undergroundVariableValues, self.undergroundRuntime, self.undergroundGap = model.execute()
                print("Objective Value: {} RunTime: {} GAP: {}" .format(self.undergroundObjValue, self.undergroundRuntime, self.undergroundGap))
                self.calculateUndergroundCapacitiesPerPeriod()
            if isinstance(model, OpenPitModel):
                self.openPitObjValue, self.openPitVariableValues, self.openPitRuntime, self.openPitGap = model.execute()
                print("Objective Value: {} RunTime: {} GAP: {}" .format(self.openPitObjValue, self.openPitRuntime, self.openPitGap))
                self.calculateOpenPitCapacitiesPerPeriod()

    def calculateOpenPitCapacitiesPerPeriod(self):
        self.openPitTonelagePerPeriod = {}
        self.openPitMineralPerPeriod = {}
        for period in range(self.numberOfPeriods):
            self.openPitTonelagePerPeriod[period] = 0
            self.openPitMineralPerPeriod[period] = 0
            for block in range(len(self.openPitVariableValues)//(self.numberOfPeriods+1)-1):
                self.openPitTonelagePerPeriod[period] += self.openPitVariableValues[period*len(self.openPitVariableValues)//(self.numberOfPeriods+1)+block] * self.openPitModel.openPitBlockTonnage[block]
                self.openPitMineralPerPeriod[period] += self.openPitVariableValues[period*len(self.openPitVariableValues)//(self.numberOfPeriods+1)+block] * self.openPitModel.openPitBlockMineral[block]
        print("Open pit mineral per period", self.openPitMineralPerPeriod)
        print("Open pit tonelage per period", self.openPitTonelagePerPeriod)

    def calculateUndergroundCapacitiesPerPeriod(self):
        variablesAggruped = [self.undergroundVariableValues[x:x+self.numberOfPeriods] for x in range(self.numberOfPeriods*len(self.undergroundModel.drawpoint), 2*self.numberOfPeriods*len(self.undergroundModel.drawpoint), self.numberOfPeriods)]
        self.undergroundTonelagePerPeriod = {}
        self.undergroundMineralPerPeriod = {}
        for period in range(self.numberOfPeriods):
            self.undergroundTonelagePerPeriod[period] = 0
            self.undergroundMineralPerPeriod[period] = 0
            for variable in range(len(variablesAggruped)):
                self.undergroundTonelagePerPeriod[period] += variablesAggruped[variable][period] * self.undergroundModel.TON_d[variable]
                self.undergroundMineralPerPeriod[period] += variablesAggruped[variable][period] * self.undergroundModel.MIN_D[variable]
        print("Underground mineral per period", self.undergroundMineralPerPeriod)
        print("Underground tonelage per period", self.undergroundTonelagePerPeriod)

path = "C:/Users/Williams Medina/Desktop/Tesis Magister/Tesis-Magister/ThesisCode/MainCode/Databases/integratedModel/"
undergroundDatabaseName = 'Modelo_F_OG.xlsx'
#undergroundDatabaseName = 'Modelo_F_OG_4_4_4.xlsx'
#openPitDatabaseName = 'Modelo_F_OG.xlsx'
openPitDatabaseName = 'Modelo_F_OG_4_4_4.xlsx'
main = Main(path, undergroundDatabaseName, openPitDatabaseName)
main.execute()

