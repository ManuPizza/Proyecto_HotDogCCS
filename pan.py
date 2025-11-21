from ingrediente import Ingrediente
#Clase pan, clase hija de ingrediente
class pan(Ingrediente):
    def __init__(self, nombre, tipo, tamaño, unidad, inventario = 0):
        super().__init__(nombre, inventario)
        self.tipo = tipo
        self.tamaño = tamaño
        self.unidad = unidad