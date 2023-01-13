from   gurobipy   import GRB

def getResults(model):
    model.optimize()
    # Saca los valores de la solución
    lista_variable_Integrado = (model.getAttr(GRB.Attr.X, model.getVars()))
    solucion = model.objVal
    runtime = model.Runtime
    gap_f = model.MIPGap
    
    return solucion, lista_variable_Integrado, runtime, gap_f
