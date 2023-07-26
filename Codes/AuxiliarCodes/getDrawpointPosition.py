def getDrawpointPosition(dp,x_draw,y_draw,z_draw):
    aux_z = dp//((max(x_draw) + 1)*(max(y_draw) + 1))

    aux_y = (dp - aux_z * ((max(x_draw) + 1)*(max(y_draw) + 1)))//(max(x_draw) + 1)
    aux_x = (dp - aux_z * ((max(x_draw) + 1)*(max(y_draw) + 1)) - aux_y * (max(x_draw) + 1))

 
    posicion = [aux_x *2,aux_y*2 ,aux_z*2]

    return posicion