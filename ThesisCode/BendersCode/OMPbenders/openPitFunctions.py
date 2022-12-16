def superiorBlock(blockIndex,numberOfBlocksInLenght,numberOfBlocksInWidth):
    topBlockCenter = numberOfBlocksInLenght * numberOfBlocksInWidth + blockIndex
    topBlockLeft = topBlockCenter - 1
    topBlockRight = topBlockCenter + 1
    topBlockDown = topBlockCenter - numberOfBlocksInLenght
    topBlockUp = topBlockCenter + numberOfBlocksInLenght

    return [topBlockCenter,topBlockLeft,topBlockRight,topBlockDown,topBlockUp]


def finalBlock(bloques_usados, limites_x_C, limites_y_C, limites_z_C): #Este es el bloque que conseguimos a través de las restricciones?
    block_sup = []*len(bloques_usados)
    for i in bloques_usados:
        aux = []
        
        if i % (limites_x_C[3] * limites_y_C[3]) == 0:      # Type 1 EL bloque esta en la esquina superior izq
            solution = superiorBlock(i,limites_x_C[3],limites_y_C[3])
            if solution[0]<=(limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[0])
            if solution[2]<=(limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[2])
            if solution[4] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                if solution[4]<=(limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                    aux.append(solution[4])

        elif i % (limites_x_C[3] * limites_y_C[3]) < limites_x_C[3] - 1: # Type 2
            solution = superiorBlock(i,limites_x_C[3],limites_y_C[3])
            if solution[0] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[0])
            if solution[1] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[1])
            if solution[2] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[2])
            if solution[4] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[4])

        elif i % (limites_x_C[3] * limites_y_C[3]) == limites_x_C[3] - 1:      # Type 3
            solution = superiorBlock(i,limites_x_C[3],limites_y_C[3])
            if solution[0] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[0])
            if solution[1] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[1])
            if solution[4] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[4])

        elif i % (limites_x_C[3] * limites_y_C[3]) == (limites_x_C[3] * limites_y_C[3]) - 1:      # Type 9
            solution = superiorBlock(i,limites_x_C[3],limites_y_C[3])
            if solution[0] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[0])
            if solution[1] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[1])
            if solution[3] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[3])

        elif i % (limites_x_C[3] * limites_y_C[3]) == limites_x_C[3] * (limites_y_C[3] - 1):      # Type 7
            solution = superiorBlock(i,limites_x_C[3],limites_y_C[3])
            if solution[0] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[0])
            if solution[2] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[2])
            if solution[3] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[3])

        elif i % (limites_x_C[3] * limites_y_C[3]) > limites_x_C[3] * (limites_y_C[3] - 1) and i % (limites_x_C[3] * limites_y_C[3]) < (limites_y_C[3] * limites_x_C[3]) - 1:       # Type 8
            solution = superiorBlock(i,limites_x_C[3],limites_y_C[3])
            if solution[0] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[0])
            if solution[1] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[1])
            if solution[2] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[2])
            if solution[3] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[3])

        elif (i % (limites_x_C[3]*limites_y_C[3]))%limites_x_C[3] == 0:      # Type 4
            solution = superiorBlock(i,limites_x_C[3],limites_y_C[3])
            if solution[0] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[0])
            if solution[2] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[2])
            if solution[3] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[3])
            if solution[4] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[4])

        elif (i % limites_x_C[3])%limites_x_C[3] == limites_x_C[3]-1:      # Type 6
            solution = superiorBlock(i,limites_x_C[3],limites_y_C[3])
            if solution[0] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1): #Para ver que no estemos en la primera capa de la matriz
                aux.append(solution[0])
            if solution[1] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[1])
            if solution[3] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[3])
            if solution[4] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[4])

        else:       # Type 5
            solution = superiorBlock(i,limites_x_C[3],limites_y_C[3])
            if solution[0] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[0])
            if solution[0] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[1])
            if solution[0] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[2])
            if solution[0] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[3])
            if solution[0] <= (limites_x_C[3] * limites_y_C[3] * limites_z_C[3] - 1):
                aux.append(solution[4])

        aux.sort()
        if aux == []:
            aux.append(i)
        block_sup.append(aux)
    return block_sup
