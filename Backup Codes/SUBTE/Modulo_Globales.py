def t_cord(cord_):
    correct_ = []
    for i in cord_.values():
        if i not in correct_:
            correct_.append(i)
    size = correct_[1] - correct_[0]
    max_ = max(correct_)
    min_ = min(correct_)
    return (size, max_, min_, len(correct_))

def cantidad_bloques(alguna_variable, lista_exportar):
    for i in range(len(alguna_variable)):
        lista_exportar.append(i)

