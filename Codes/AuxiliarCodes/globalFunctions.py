def getNumberOfBlocksInADimension(coordDimensions):
    uniqueDimensions = []
    for dimension in coordDimensions.values():
        if dimension not in uniqueDimensions:
            uniqueDimensions.append(dimension)
    size = uniqueDimensions[1]-uniqueDimensions[0]
    maxDimension = max(uniqueDimensions)
    minDimension = min(uniqueDimensions)
    numberOfDifferentBlocks = len(uniqueDimensions)
    return (size, maxDimension, minDimension ,numberOfDifferentBlocks)