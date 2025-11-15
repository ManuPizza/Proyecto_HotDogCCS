class Ingrediente():
    def __init__(self, nombre, inventario = 0):
        self.nombre = nombre
        self.inventario = inventario
    def disponibilidad(self, cantidad):
        if cantidad <= self.inventario:
            return True
        return False
    def mostrar(self):
        print(f"{self.nombre} disponible en inventario: {self.inventario}")
    def eliminando(self, menu):
        aux = []
        for x in menu:
            if self in x.ingredientes:
                aux.append(x)
                menu.remove(x)
        print(f"""Si eliminas este ingrediente se eliminarán los siguientes hotdogs:
              {aux}
              """)
        while True:
            decision = input(f"Está seguro que desea eliminar el ingrediente: {self.nombre}. Solo coloque (si) o (no)------> ").lower()
            if decision == "si":
                return True
            elif decision == "no":
                menu.extend(aux)
                return False
            else:
                print("Opcion inválida, solo debes colocar si o no")
    