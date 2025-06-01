# acciones/colisiones.py

# FUNCION QUE DETECTA COLISIONES USANDO CAJAS DELIMITADORAS ALINEADAS A LOS EJES (AABB)
def aabbCollision(obj1_x, obj1_y, obj1_z, obj1_width, obj1_height, obj1_depth,
                  obj2_x, obj2_y, obj2_z, obj2_width, obj2_height, obj2_depth):
   
    # Calcular los límites mínimos y máximos para el objeto 1
    obj1_minX = obj1_x - obj1_width / 2.0
    obj1_maxX = obj1_x + obj1_width / 2.0
    obj1_minY = obj1_y - obj1_height / 2.0
    obj1_maxY = obj1_y + obj1_height / 2.0
    obj1_minZ = obj1_z - obj1_depth / 2.0
    obj1_maxZ = obj1_z + obj1_depth / 2.0

    # Calcular los límites mínimos y máximos para el objeto 2
    obj2_minX = obj2_x - obj2_width / 2.0
    obj2_maxX = obj2_x + obj2_width / 2.0
    obj2_minY = obj2_y - obj2_height / 2.0
    obj2_maxY = obj2_y + obj2_height / 2.0
    obj2_minZ = obj2_z - obj2_depth / 2.0
    obj2_maxZ = obj2_z + obj2_depth / 2.0

    # Comprobar la superposición en cada eje
    # Hay colisión si los rangos se superponen en todos los ejes (X, Y, Z)
    
    # Superposición en el eje X
    colisionX = obj1_maxX >= obj2_minX and obj1_minX <= obj2_maxX
    
    # Superposición en el eje Y
    colisionY = obj1_maxY >= obj2_minY and obj1_minY <= obj2_maxY
    
    # Superposición en el eje Z
    colisionZ = obj1_maxZ >= obj2_minZ and obj1_minZ <= obj2_maxZ

    # Si hay superposición en todos los ejes, entonces hay una colisión
    return colisionX and colisionY and colisionZ