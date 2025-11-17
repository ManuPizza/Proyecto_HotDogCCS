import funciones
def main():
    menu,inventario = funciones.cargar_archivo("https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-1/main/menu.json","https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-1/main/ingredientes.json")
    while True:
        decision = input("Introduce el numero según el modulo al que desees acceder: \n1- Modulo de Ingredientes \n2- Modulo de inventario \n3- Modulo de menú \n4- Simular día de ventas \n5-Guardar y salir \n------->").lower()
        if decision == "1":
            print("Has ingresado al modulo de estadisticas")
            while True:
                decision2 = input("Introduce el número según lo que quieras hacer:\n1-Listar productos por categoria\n2-Listar productos por categoria y por tipo\n3-Agregar un ingrediente\n4-Eliminar un ingrediente\n5-Regresar al menú principal\n------->").lower()
                if decision2 == "1":
                    funciones.productos_categoria(inventario)
                elif decision2 == "2":
                    aux = funciones.productos_tipos(inventario)
                    if aux:
                        print(aux)
                elif decision2 == "3":
                    funciones.agregar(inventario)
                elif decision2 == "4":
                    funciones.eliminar_inventario(inventario,menu)
                elif decision2 == "5":
                    break
                else:
                    print("No has introducido una opción válida, intenta de nuevo")
        elif decision == "2":
            while True:
                decision2 = input("Introduce el número según lo que desees hacer:\n1-Visualizar todo el inventario\n2-Buscar la existencia de un ingrediente en especifico \n3-Listar las existencias de todos los ingredientes de una categoria\n4-Actualizar la existencia de un producto en especifico\n5-Regresar al menú principal\n------->").lower()
                if decision2== "1":
                    funciones.ver_inventario(inventario)
                elif decision2 == "2":
                    funciones.buscar(inventario)
                elif decision2 == "3":
                    funciones.productos_tipos(inventario)
                elif decision2 == "4":
                    funciones.agregar(inventario)
                elif decision2 == "5":
                    break
                else:
                    print("No has introducido una opción válida, intenta de nuevo")
        elif decision == "3":
            while True:
                decision2 = input("Introduce el número según lo que desees hacer:\n1-Ver lista de HotDogs\n2-Ver disponibilidad para un HotDog especifico\n3-Agregar un nuevo HotDog\n4-eliminar un HotDog\n5-Volver al menú principal\n------>")
                if decision2 == "1":
                    funciones.ver_menu(menu)
                elif decision2 == "2":
                    usado = funciones.buscar_menu(menu)
                    if usado.comprobar_inventario():
                        print("El HotDog está disponible")
                    else:
                        print("El HotDog no está disponible")
                elif decision2 == "3":
                    funciones.agregar_hotdog(inventario,menu)
                elif decision2 == "4":
                    funciones.eliminar(menu,inventario)
                elif decision2 == "5":
                    break
                else:
                    print("Has introducido una opción inválida")
        elif decision == "4":
            funciones.simular_dia(menu,inventario)
        elif decision == "5":
            print("Gracias por usar nuestro programa")
            funciones.guardar(menu,inventario)
            break
        else:
            print("Has introducido una opción inválida, por favor intenta de nuevo")
        
main()