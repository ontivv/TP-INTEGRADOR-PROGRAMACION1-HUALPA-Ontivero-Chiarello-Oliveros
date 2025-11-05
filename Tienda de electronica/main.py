#importamos las funciones
from lectura import cargar_datos_recursivo, mostrar_todos_los_items, filtrar_por_atributo
from crud import alta_producto, modificar_producto, eliminar_producto
from estadisticas import mostrar_estadisticas, ordenar_productos # <-- AÑADIDAS

CARPETA_RAIZ = "datos"
FIELDNAMES = ["id", "nombre", "precio", "stock"]

def menu_principal():
    print("Cargando base de datos...")
    DATOS_EN_MEMORIA = cargar_datos_recursivo(CARPETA_RAIZ)
    print(f"¡Carga completa! {len(DATOS_EN_MEMORIA)} ítems encontrados.")

    while True:
        print("\n--- MENÚ PRINCIPAL TPI ---")
        print("--- CRUD ---")
        print("1. Alta de producto (Create)")
        print("2. Mostrar TODOS los productos (Read)")
        print("3. Filtrar productos (Read)")
        print("4. Modificar producto (Update)")
        print("5. Eliminar producto (Delete)")
        print("--- ANÁLISIS ---")
        print("6. Mostrar Estadísticas")
        print("7. Ordenar y Mostrar")
        print("8. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            alta_producto()
            DATOS_EN_MEMORIA = cargar_datos_recursivo(CARPETA_RAIZ) #recargamos los datos
            
        elif opcion == '2':
            mostrar_todos_los_items(DATOS_EN_MEMORIA) 
        
        elif opcion == '3':
            filtrar_por_atributo(DATOS_EN_MEMORIA)
            
        elif opcion == '4':
            modificar_producto(DATOS_EN_MEMORIA,FIELDNAMES) #modifica en memoria Y disco
            
        elif opcion == '5':
            eliminar_producto(DATOS_EN_MEMORIA,FIELDNAMES) #elimina de memoria Y disco
            
        elif opcion == '6':
            mostrar_estadisticas(DATOS_EN_MEMORIA) #solo lee de memoria
            
        elif opcion == '7':
            #ordenar() devuelve una NUEVA lista ordenada
            lista_ordenada_para_mostrar = ordenar_productos(DATOS_EN_MEMORIA)
            #reutilizamos mostrar() para imprimir esa nueva lista
            mostrar_todos_los_items(lista_ordenada_para_mostrar)
            
        elif opcion == '8':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu_principal()