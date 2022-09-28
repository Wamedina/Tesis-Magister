def superiorBlock(blockIndex,numberOfBlocksInLenght,numberOfBlocksInWidth):
    topBlockCenter = numberOfBlocksInLenght * numberOfBlocksInWidth + blockIndex
    topBlockLeft = topBlockCenter - 1
    topBlockRight = topBlockCenter + 1
    topBlockDown = topBlockCenter - numberOfBlocksInLenght
    topBlockUp = topBlockCenter + numberOfBlocksInLenght

    return [topBlockCenter,topBlockLeft,topBlockRight,topBlockDown,topBlockUp]


def predecessorBlocks(bloques_usados, limites_x_C, limites_y_C, limites_z_C): #Este es el bloque que conseguimos a través de las restricciones?
    block_sup = []*len(bloques_usados)
    numberOfBlocksInX = limites_x_C[3]
    numberOfBlocksInY = limites_y_C[3]
    numberOfBlocksInZ = limites_z_C[3]
    for i in bloques_usados:
        aux = []
                    
        solution = superiorBlock(i,numberOfBlocksInX,numberOfBlocksInY)
        topBlockCenter,topBlockLeft,topBlockRight,topBlockDown,topBlockUp = solution[0], solution[1], solution[2], solution[3], solution[4]
        totalNumberOfBlocksIndices = (numberOfBlocksInX * numberOfBlocksInY * numberOfBlocksInZ - 1)

        if i % (numberOfBlocksInX * numberOfBlocksInY) == 0:      # Type 1 EL bloque esta en la esquina superior izq
            if topBlockCenter<=totalNumberOfBlocksIndices:
                aux.append(topBlockCenter)
            if topBlockRight<=totalNumberOfBlocksIndices:
                aux.append(topBlockRight)
            if topBlockUp <= totalNumberOfBlocksIndices:
                if topBlockUp<=totalNumberOfBlocksIndices:
                    aux.append(topBlockUp)

        elif i % (numberOfBlocksInX * numberOfBlocksInY) < numberOfBlocksInX - 1: # Type 2
            if topBlockCenter <= totalNumberOfBlocksIndices:
                aux.append(topBlockCenter)
            if topBlockLeft <= totalNumberOfBlocksIndices:
                aux.append(topBlockLeft)
            if topBlockRight <= totalNumberOfBlocksIndices:
                aux.append(topBlockRight)
            if topBlockUp <= totalNumberOfBlocksIndices:
                aux.append(topBlockUp)

        elif i % (numberOfBlocksInX * numberOfBlocksInY) == numberOfBlocksInX - 1:      # Type 3
            if topBlockCenter <= totalNumberOfBlocksIndices:
                aux.append(topBlockCenter)
            if topBlockLeft <= totalNumberOfBlocksIndices:
                aux.append(topBlockLeft)
            if topBlockUp <= totalNumberOfBlocksIndices:
                aux.append(topBlockUp)

        elif i % (numberOfBlocksInX * numberOfBlocksInY) == (numberOfBlocksInX * numberOfBlocksInY) - 1:      # Type 9
            if topBlockCenter <= totalNumberOfBlocksIndices:
                aux.append(topBlockCenter)
            if topBlockLeft <= totalNumberOfBlocksIndices:
                aux.append(topBlockLeft)
            if topBlockDown <= totalNumberOfBlocksIndices:
                aux.append(topBlockDown)

        elif i % (numberOfBlocksInX * numberOfBlocksInY) == numberOfBlocksInX * (numberOfBlocksInY - 1):      # Type 7
            if topBlockCenter <= totalNumberOfBlocksIndices:
                aux.append(topBlockCenter)
            if topBlockRight <= totalNumberOfBlocksIndices:
                aux.append(topBlockRight)
            if topBlockDown <= totalNumberOfBlocksIndices:
                aux.append(topBlockDown)

        elif i % (numberOfBlocksInX * numberOfBlocksInY) > numberOfBlocksInX * (numberOfBlocksInY - 1) and i % (numberOfBlocksInX * numberOfBlocksInY) < (numberOfBlocksInY * numberOfBlocksInX) - 1:       # Type 8
            if topBlockCenter <= totalNumberOfBlocksIndices:
                aux.append(topBlockCenter)
            if topBlockLeft <= totalNumberOfBlocksIndices:
                aux.append(topBlockLeft)
            if topBlockRight <= totalNumberOfBlocksIndices:
                aux.append(topBlockRight)
            if topBlockDown <= totalNumberOfBlocksIndices:
                aux.append(topBlockDown)

        elif (i % (numberOfBlocksInX*numberOfBlocksInY))%numberOfBlocksInX == 0:      # Type 4
            if topBlockCenter <= totalNumberOfBlocksIndices:
                aux.append(topBlockCenter)
            if topBlockRight <= totalNumberOfBlocksIndices:
                aux.append(topBlockRight)
            if topBlockDown <= totalNumberOfBlocksIndices:
                aux.append(topBlockDown)
            if topBlockUp <= totalNumberOfBlocksIndices:
                aux.append(topBlockUp)

        elif (i % numberOfBlocksInX)%numberOfBlocksInX == numberOfBlocksInX-1:      # Type 6
            if topBlockCenter <= totalNumberOfBlocksIndices: #Para ver que no estemos en la primera capa de la matriz
                aux.append(topBlockCenter)
            if topBlockLeft <= totalNumberOfBlocksIndices:
                aux.append(topBlockLeft)
            if topBlockDown <= totalNumberOfBlocksIndices:
                aux.append(topBlockDown)
            if topBlockUp <= totalNumberOfBlocksIndices:
                aux.append(topBlockUp)

        else:       # Type 5            
            if topBlockCenter <= totalNumberOfBlocksIndices:
                aux.append(topBlockLeft)
            if topBlockCenter <= totalNumberOfBlocksIndices:
                aux.append(topBlockRight)
            if topBlockCenter <= totalNumberOfBlocksIndices:
                aux.append(topBlockDown)
            if topBlockCenter <= totalNumberOfBlocksIndices:
                aux.append(topBlockUp)

        aux.sort()
        if aux == []:
            aux.append(i)
        block_sup.append(aux)
    #Return a list of the predecessor blocks for each one of them, in their predeterminated order.
    return block_sup
