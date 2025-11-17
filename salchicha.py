from ingrediente import Ingrediente
class salchicha(Ingrediente):
    def __init__(self, nombre, tipo, tamaño, unidad, inventario = 0):
        super().__init__(nombre, inventario)
        self.tipo = tipo
        self.tamaño = tamaño
        self.unidad = unidad