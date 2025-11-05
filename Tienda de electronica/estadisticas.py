# --- estadisticas.py ---
# Módulo para calcular estadísticas y realizar ordenamientos
# sobre la lista global de ítems en memoria.
import os # Lo usamos para extraer la categoría de la ruta


def mostrar_estadisticas(lista_items):
    """
    Calcula y muestra un resumen de estadísticas basadas en la
    lista total de ítems, como se pide en los requisitos[cite: 208].
    """
    print("\n--- 6. Estadísticas del Inventario ---")
    
    
    # 1. Cantidad Total de Ítems [cite: 208]
    total_items = len(lista_items)
    if total_items == 0:
        print("No hay datos cargados para calcular estadísticas.")
        return
    print(f"Cantidad Total de Productos: {total_items}")
    
    
    # 2. Promedio de Precios [cite: 208]
    try:
        # Sumamos el 'precio' de cada item en la lista
        suma_precios = sum(item.get('precio', 0) for item in lista_items)
        precio_promedio = suma_precios / total_items
        print(f"Precio Promedio del Inventario: ${precio_promedio:.2f}")
    except ZeroDivisionError:
        print("Precio Promedio del Inventario: N/A")
    except TypeError:
        print("Error: Algunos precios no son numéricos.")
    
    
    # 3. Suma Total de Stock [cite: 208]
    try:
        total_stock = sum(item.get('stock', 0) for item in lista_items)
        print(f"Stock Total en Inventario: {total_stock} unidades")
    except TypeError:
        print("Error: Algunos valores de stock no son numéricos.")
    
    
    # 4. Recuento de ítems por Categoría (Primer Nivel) [cite: 208]
    conteo_categorias = {}
    for item in lista_items:
        try:
            # Extraemos la categoría de la ruta de origen
            categoria = item['ruta_origen'].split(os.sep)[1]
            # Usamos .get() para sumar 1 al conteo existente o empezar en 0+1
            conteo_categorias[categoria] = conteo_categorias.get(categoria, 0) + 1
        except (KeyError, IndexError):
            # Si el item no tiene 'ruta_origen' o la ruta es inválida
            conteo_categorias["_sin_categoria"] = conteo_categorias.get("_sin_categoria", 0) + 1
            print("\nConteo por Categoría (Primer Nivel):")
            if conteo_categorias:
                for cat, count in conteo_categorias.items():
                    print(f" - {cat}: {count} producto(s)")
            else:
                print(" - No se pudieron agrupar categorías.")


def ordenar_productos(lista_items):
    """
    Permite al usuario ordenar la lista completa de ítems
    por dos o más criterios (nombre y precio)[cite: 207].
    Devuelve una NUEVA lista ordenada.
    """
    
    print("\n--- 7. Ordenar Productos ---")
    if not lista_items:
        print("No hay productos para ordenar.")
        # Devuelve la lista vacía original
        return lista_items
    
    print("¿Por cuál criterio desea ordenar?")
    print(" 1. Nombre (A-Z)")
    print(" 2. Precio (Más barato primero)")
    print(" 3. Precio (Más caro primero)")
    
    criterio = input("Seleccione una opción (1-3): ").strip()
    lista_ordenada = []
    try:
        if criterio == '1':
            # key=lambda item: item['nombre'].lower()
            # .lower() asegura que el orden no distinga mayúsculas (A-z)
            lista_ordenada = sorted(lista_items, key=lambda item: item.get('nombre', '').lower())
            print("Productos ordenados por nombre (A-Z).")
            
        elif criterio == '2':
            # Orden numérico ascendente (default)
            lista_ordenada = sorted(lista_items, key=lambda item: item.get('precio', 0.0))
            print("Productos ordenados por precio (ascendente).")
            
        elif criterio == '3':
            # Orden numérico descendente (reverse=True)
            lista_ordenada = sorted(lista_items, key=lambda item: item.get('precio', 0.0),
            reverse=True)
            print("Productos ordenados por precio (descendente).")
            
        else:
            print("Opción no válida. No se realizó el ordenamiento.")
            return lista_items # Devuelve la lista original sin cambios
        
        # Si el ordenamiento fue exitoso, devolvemos la nueva lista
        return lista_ordenada
    except TypeError:
        print("Error: No se pudo ordenar. Verifique que los datos de precio/nombre sean correctos.")
        return lista_items # Devuelve la lista original
    except KeyError as e:
        print(f"Error: Falta la clave {e} en algunos ítems.")
        return lista_items # Devuelve la lista original
