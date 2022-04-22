import pandas as pd
from OpenPitModel import openPitModel
from BlockFunctions import *

class Main:
    def __init__(self, path, databaseName):
        self.path = path
        self.databaseName = databaseName
        self.mineDatabase = None
        self.model = None

    def execute(self):
        self.setMineDatabase(path, databaseName)
        self.setVariables()
        self.getBlockInfo()

    def setMineDatabase(self, path, databaseName):
        self.mineDataFrame = pd.read_excel(path+databaseName, engine="openpyxl")

    def setVariables(self):
        self.blocksLenght = self.mineDataFrame['X'].to_dict() 
        self.blocksWidth = self.mineDataFrame['Y'].to_dict() 
        self.blocksHeight = self.mineDataFrame['Z'].to_dict() 
        self.blockTonnage = self.mineDataFrame['Ton'].to_dict() 
        self.blockMineral = self.mineDataFrame['Mineral'].to_dict()
        self.blockRecovery = self.mineDataFrame['Recuperación'].to_dict() 
        self.copperLaw = self.mineDataFrame['%Cu'].to_dict()
        self.extractionFixedCosts = self.mineDataFrame['CPlanta CA'].to_dict()
        self.variableExtractionCosts = self.mineDataFrame['CMina CA'].to_dict()

    def getBlockInfo(self):
        a = getNumberOfDifferentBlocksInADimension(self.blocksLenght)

    def setModel(self, ):
        self.model = integratedModel(bloques_CA,drawpoint,cord_z_C,dif_centroide,pos_z,col_height,cota_seg,predecessor_block,predecessor,
                             TON_C,MIN_C,REC_C,LEY_C,CM_CA_C,CP_CA_C,
                             TON_d,MIN_D,REC,LEY_D,C_P_D,C_M_D,
                             t_C,RMu_t,RMl_t,RPu_t,RPl_t,qu_t,ql_t,time_max_C,
                             t_S,MU_mt,ML_mt,MU_pt,ML_pt,qU_dt,qL_dt,A_d,NU_nt,NL_nt,N_t,RL_dt,RU_dt,time_max_S,
                             GAP,precio,costo_mina_ponderador,costo_planta_ponderador)


path = "C:/Users/willi/OneDrive/Escritorio/Magister/Database/"
databaseName = "Modelo.xlsx"
main = Main(path, databaseName)
main.execute()