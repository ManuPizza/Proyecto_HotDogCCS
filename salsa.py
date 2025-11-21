from ingrediente import Ingrediente
#Clase salsa, clase hija de ingrediente
class salsa(Ingrediente):
    def __init__(self, nombre, base, color, inventario = 0):
        super().__init__(nombre, inventario)
        self.base = base
        self.color = color