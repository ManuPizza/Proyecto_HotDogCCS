from ingrediente import Ingrediente
class pan(Ingrediente):
    def __init__(self, nombre, tipo, tamaño, unidad, inventario = 0):
        super().__init__(inventario, nombre)
        self.tipo = tipo
        self.tamaño = tamaño
        self.unidad = unidad