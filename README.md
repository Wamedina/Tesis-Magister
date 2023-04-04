# Magister


# Para 1 periodo

## OpenPit Parameters
self.t_C   = {period : period + 1 for period in range(self.numberOfPeriods)}
self.RMu_t = {period : 132192000000000000000.0 for period in range(self.numberOfPeriods)}#Superior infinita, 0 por abajo Originales: 13219200
self.RMl_t = {period : 0 for period in range(self.numberOfPeriods)}#Valor original 8812800.0
self.RPu_t = {period : 109300000000000000000000000003380.0 for period in range(self.numberOfPeriods)}#Valor original 10933380.0
self.RPl_t = {period : 0 for period in range(self.numberOfPeriods)}#Valor original 7288920.0 
self.qu_t  = {period : 3 for period in range(self.numberOfPeriods)}#Leyes promedio maxima y minima.
self.ql_t  = {period : 0 for period in range(self.numberOfPeriods)}
self.maxTimeOpenPit = self.t_C[max(self.t_C)]

## Underground Parameters
self.t_S   = {period : period + 1 for period in range(self.numberOfPeriods)}
self.MU_mt = {period : 2580660000000000000000.0  for period in range(self.numberOfPeriods)}
self.ML_mt = {period : 0 for period in range(self.numberOfPeriods)}
self.MU_pt = {period : 177700000000000000000000007880.0  for period in range(self.numberOfPeriods)}
self.ML_pt = {period : 0  for period in range(self.numberOfPeriods)}
self.qU_dt = {period : 1 for period in range(self.numberOfPeriods)}
self.qL_dt = {period : 0 for period in range(self.numberOfPeriods)}
self.A_d   = {period : 2 for period in range(self.numberOfPeriods)}
self.NU_nt = {period : 59000000000000 for period in range(self.numberOfPeriods)}# 
self.NL_nt = {period : 0 for period in range(self.numberOfPeriods)}
self.N_t   = {period : 570000000000000 * (1 + period) for period in range(self.numberOfPeriods)}
self.RL_dt = {period : 0.3 for period in range(self.numberOfPeriods)}
self.RU_dt = {period : 0.7 for period in range(self.numberOfPeriods)}


# Para 5 periodos

## OpenPit Parameters
self.t_C   = {period : period + 1 for period in range(self.numberOfPeriods)}
self.RMu_t = {period : 13219200.0 for period in range(self.numberOfPeriods)}#Superior infinita, 0 por abajo Originales: 13219200
self.RMl_t = {period : 8812800.0 for period in range(self.numberOfPeriods)}#Valor original 8812800.0
self.RPu_t = {period : 10933380.0 for period in range(self.numberOfPeriods)}#Valor original 10933380.0
self.RPl_t = {period : 0 for period in range(self.numberOfPeriods)}#Valor original 7288920.0 
self.qu_t  = {period : 1 for period in range(self.numberOfPeriods)}#Leyes promedio maxima y minima.
self.ql_t  = {period : 0 for period in range(self.numberOfPeriods)}

## Underground Parameters
self.t_S   = {period : period + 1 for period in range(self.numberOfPeriods)}
self.MU_mt = {period : 25806600.0  for period in range(self.numberOfPeriods)} #Tonleage es mina
self.ML_mt = {period : 17204400.0  for period in range(self.numberOfPeriods)}
self.MU_pt = {period : 17777880.0   for period in range(self.numberOfPeriods)}#Mineral es planta
self.ML_pt = {period : 17204400.0 for period in range(self.numberOfPeriods)}
self.qU_dt = {period : 1 for period in range(self.numberOfPeriods)}
self.qL_dt = {period : 0 for period in range(self.numberOfPeriods)}
self.A_d   = {period : 2 for period in range(self.numberOfPeriods)}
self.NU_nt = {period : 59 for period in range(self.numberOfPeriods)} 
self.NL_nt = {period : 32 for period in range(self.numberOfPeriods)}
self.N_t   = {period : 57* (1 + period) for period in range(self.numberOfPeriods)}
self.RL_dt = {period : 0.3 for period in range(self.numberOfPeriods)}
self.RU_dt = {period : 0.7 for period in range(self.numberOfPeriods)}



# Para 10 periodos

## OpenPit Parameters
self.t_C   = {period : period + 1 for period in range(self.numberOfPeriods)}
self.RMu_t = {period : 13219200.0/2 for period in range(self.numberOfPeriods)}#Superior infinita, 0 por abajo Originales: 13219200
self.RMl_t = {period : 0.0 for period in range(self.numberOfPeriods)}#Valor original 8812800.0
self.RPu_t = {period : 10933380.0/2 for period in range(self.numberOfPeriods)}#Valor original 10933380.0
self.RPl_t = {period : 0 for period in range(self.numberOfPeriods)}#Valor original 7288920.0 
self.qu_t  = {period : 1 for period in range(self.numberOfPeriods)}#Leyes promedio maxima y minima.
self.ql_t  = {period : 0.0001 for period in range(self.numberOfPeriods)}
self.maxTimeOpenPit = self.t_C[max(self.t_C)]

## Underground Parameters
self.t_S   = {period : period + 1 for period in range(self.numberOfPeriods)}
self.MU_mt = {period : 25806600.0/2  for period in range(self.numberOfPeriods)} #Tonleage es mina
self.ML_mt = {period : 0.0  for period in range(self.numberOfPeriods)}
self.MU_pt = {period : 17777880.0/2  for period in range(self.numberOfPeriods)}#Mineral es planta
self.ML_pt = {period : 0.0 for period in range(self.numberOfPeriods)}
self.qU_dt = {period : 1 for period in range(self.numberOfPeriods)}
self.qL_dt = {period : 0.15 for period in range(self.numberOfPeriods)}
self.A_d   = {period : 2 for period in range(self.numberOfPeriods)}
self.NU_nt = {period : 59 for period in range(self.numberOfPeriods)} 
self.NL_nt = {period : 0 for period in range(self.numberOfPeriods)}
self.N_t   = {period : 57* (1 + period) for period in range(self.numberOfPeriods)}
self.RL_dt = {period : 0.3 for period in range(self.numberOfPeriods)}
self.RU_dt = {period : 0.7 for period in range(self.numberOfPeriods)}



# Para 15 periodos

## OpenPit Parameters
self.t_C   = {period : period + 1 for period in range(self.numberOfPeriods)}
self.RMu_t = {period : 13219200.0/3 for period in range(self.numberOfPeriods)}#Superior infinita, 0 por abajo Originales: 13219200
self.RMl_t = {period : 0.0 for period in range(self.numberOfPeriods)}#Valor original 8812800.0
self.RPu_t = {period : 10933380.0/3 for period in range(self.numberOfPeriods)}#Valor original 10933380.0
self.RPl_t = {period : 0 for period in range(self.numberOfPeriods)}#Valor original 7288920.0 
self.qu_t  = {period : 1 for period in range(self.numberOfPeriods)}#Leyes promedio maxima y minima.
self.ql_t  = {period : 0.0001 for period in range(self.numberOfPeriods)}
self.maxTimeOpenPit = self.t_C[max(self.t_C)]

## Underground Parameters
self.t_S   = {period : period + 1 for period in range(self.numberOfPeriods)}
self.MU_mt = {period : 25806600.0/3  for period in range(self.numberOfPeriods)} #Tonleage es mina
self.ML_mt = {period : 0.0  for period in range(self.numberOfPeriods)}
self.MU_pt = {period : 17777880.0/3  for period in range(self.numberOfPeriods)}#Mineral es planta
self.ML_pt = {period : 0.0 for period in range(self.numberOfPeriods)}
self.qU_dt = {period : 1 for period in range(self.numberOfPeriods)}
self.qL_dt = {period : 0.15 for period in range(self.numberOfPeriods)}
self.A_d   = {period : 2 for period in range(self.numberOfPeriods)}
self.NU_nt = {period : 59 for period in range(self.numberOfPeriods)} 
self.NL_nt = {period : 0 for period in range(self.numberOfPeriods)}
self.N_t   = {period : 57* (1 + period) for period in range(self.numberOfPeriods)}
self.RL_dt = {period : 0.3 for period in range(self.numberOfPeriods)}
self.RU_dt = {period : 0.7 for period in range(self.numberOfPeriods)}



# Para 20 periodos

## OpenPit Parameters
self.t_C   = {period : period + 1 for period in range(self.numberOfPeriods)}
self.RMu_t = {period : 13219200.0/4 for period in range(self.numberOfPeriods)}#Superior infinita, 0 por abajo Originales: 13219200
self.RMl_t = {period : 0.0 for period in range(self.numberOfPeriods)}#Valor original 8812800.0
self.RPu_t = {period : 10933380.0/4 for period in range(self.numberOfPeriods)}#Valor original 10933380.0
self.RPl_t = {period : 0 for period in range(self.numberOfPeriods)}#Valor original 7288920.0 
self.qu_t  = {period : 1 for period in range(self.numberOfPeriods)}#Leyes promedio maxima y minima.
self.ql_t  = {period : 0.0001 for period in range(self.numberOfPeriods)}
self.maxTimeOpenPit = self.t_C[max(self.t_C)]

## Underground Parameters
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

