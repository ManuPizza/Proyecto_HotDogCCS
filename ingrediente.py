#Clase padre y abstracta ingrediente
class Ingrediente():
    def __init__(self, nombre, inventario = 0):
        self.nombre = nombre
        self.inventario = inventario
    #Muestra el nombre e inventario disponible, funciona para las subclases (No utiliza polimorfismo)
    def mostrar(self):
        print(f"{self.nombre} disponible en inventario: {self.inventario}")
    #Elimina un ingrediente asegurandose que se eliminen las recetas
    def eliminando(self, menu, ubicacion):
        aux = []
        for receta in menu:
            for x in vars(receta).values():
                if x:
                    if not isinstance(x,list):
                        if x == self:
                            aux.append(receta)
                            menu.remove(receta)
                            break
                    else:
                        if self in x:
                            aux.append(receta)
                            menu.remove(receta)
                            break
        if aux:            
            print("Si eliminas este ingrediente se eliminarán los siguientes hotdogs:")
            for z in aux:
                print(z.nombre)
        
            while True:
                decision = input(f"Está seguro que desea eliminar el ingrediente: {self.nombre}. Solo coloque (si) o (no)------> ").lower()
                if decision == "si":
                    ubicacion.remove(self)
                    return True
                elif decision == "no":
                    menu.extend(aux)
                    return False
                else:
                    print("Opcion inválida, solo debes colocar si o no")
        else:
            ubicacion.remove(self)
            return True
    