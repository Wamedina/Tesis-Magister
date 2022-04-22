#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def separacion_integrado(lista_variable_Integrado,time_max_C,time_max_S,bloques_CA,drawpoint):
    VAR_X_C = list()
    VAR_S = list()
    aux = 0
    for i in range(len(lista_variable_Integrado)):
        if aux < len(bloques_CA)*time_max_C:
            VAR_X_C.append(lista_variable_Integrado[i])
        else:
            VAR_S.append(lista_variable_Integrado[i])
        aux += 1
    return VAR_X_C, VAR_S

