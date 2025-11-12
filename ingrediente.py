class Ingrediente():
    def __init__(self, nombre, inventario= 0):
        self.inventario = inventario
        self.nombre = nombre
    def disponibilidad(self, cantidad):
        if cantidad <= self.inventario:
            return True
        return False
    def mostrar(self):
        print(f"{self.nombre} disponible en inventario: {self.inventario}")