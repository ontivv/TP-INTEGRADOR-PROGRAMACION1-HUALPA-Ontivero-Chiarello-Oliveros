# Módulo para las operaciones de Create, Update y Delete. 
# Este es el único módulo que escribe en el disco duro. 

import os
import csv

# Importamos las funciones de nuestro módulo de validaciones 
try: 
    from validaciones import validar_no_vacio, validar_numero_positivo 
except ImportError: 
    print("Error: No se encontró el módulo 'validaciones.py'.") 
    exit()

# Constantes del Módulo.
CARPETA_RAIZ = "datos"
NOMBRE_ARCHIVO_CSV = "items.csv"
FIELDNAMES = ["id", "nombre", "precio", "stock"]

def alta_producto():
    """
    (CREATE) 
    Pide los datos de un nuevo producto, crea la estructura 
    jerárquica de carpetas si no existe y agrega el producto 
    al archivo CSV correspondiente
    """
    print("\n--- 1. Alta de Nuevo Producto ---")

    # --- 1. Entrada de Datos ---
    # Entrada de Datos (Jerarquía) 
    categoria = input("Ingrese la Categoría (ej: Hardware): ").strip()
    marca = input("Ingrese la Marca (ej: Intel): ").strip()

    # Entrada de Datos (Atributos) 
    nombre = input("Ingrese el Nombre del producto (ej: Core i5): ").strip()
    precio_str = input("Ingrese el Precio del producto (ej: 250.50): ") 
    stock_str = input("Ingrese el Stock inicial (ej: 50): ") 

    # --- 2. Validaciones Estrictas y Conversión --- 
    
    # Validación de no vacíos 
    if not (validar_no_vacio(categoria) and
            validar_no_vacio(marca) and
            validar_no_vacio(nombre)):
        print("\nError: Categoría, Marca y Nombre no pueden estar vacíos.") 
        return # Salir de la función si hay un error
    
    # Validación y conversión de numéricos (deben ser > 0) 
    valido_precio, precio = validar_numero_positivo(precio_str)
    valido_stock, stock_num = validar_numero_positivo(stock_str)
    
    # Conversión final del stock a entero (si es válido)
    stock = int(stock_num) if valido_stock else None
    
    if not (valido_precio and valido_stock):
        print("\nError en Precio o Stock. Deben ser números > 0.")
        return # Salir de la función si hay un error

    # --- 3. Construcción de Ruta y Creación de Carpetas --- 
    ruta_directorio = os.path.join(CARPETA_RAIZ, categoria, marca)

    try:
        # Crea toda la jerarquía de carpetas si no existe. 
        os.makedirs(ruta_directorio, exist_ok=True)
    except OSError as e:
        print(f"\nError crítico al crear la estructura de directorios: {e}") 
        return # Salir si no se puede crear la ruta 

    # Ruta del archivo CSV dentro del último directorio
    ruta_archivo = os.path.join(ruta_directorio, NOMBRE_ARCHIVO_CSV)

    # --- 4. Preparación del Ítem y Persistencia ---
    # Generamos un ID simple (puedes mejorarlo) 
    item_id = f"{categoria[:3].upper()}-{marca[:3].upper()}-{stock}" 
    
    nuevo_producto = { 
        'id': item_id, 
        'nombre': nombre, 
        'precio': precio, 
        'stock': stock 
    } 

    # Verificamos si el archivo ya existe para no duplicar cabeceras 
    escribir_header = not os.path.exists(ruta_archivo)

    try:
        with open(ruta_archivo, mode='a', newline='', encoding='utf-8') as f: 
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)

            if escribir_header:
                writer.writeheader()

            writer.writerow(nuevo_producto)

        print(f"\n¡Éxito! Producto '{nombre}' agregado en '{ruta_archivo}'") 

    except IOError as e:
        print(f"\nError de E/S al escribir en el archivo: {e}") 
    except Exception as e:
        print(f"\nOcurrió un error inesperado al escribir: {e}")

# --- Funciones de Persistencia (Update y Delete) ---

def _sobrescribir_archivo_csv(ruta_archivo, lista_global_items, FIELDNAMES):
    """
    Función auxiliar interna para filtrar los items de una ruta específica
    (ruta_archivo) desde la lista global y sobrescribir su archivo CSV.
    
    Recuerda: esta función ELIMINA la clave 'ruta_origen' antes de escribir.
    """
    items_a_persistir = []
    
    # 1. Recorrer la lista global para obtener solo los items de esta ruta
    for item in lista_global_items:
        if item.get('ruta_origen') == ruta_archivo:
            # 2. Crear una copia del item SIN la clave 'ruta_origen' 
            # (ya que no debe ir en el CSV)
            item_para_csv = {k: v for k, v in item.items() if k != 'ruta_origen'}
            items_a_persistir.append(item_para_csv)

    # 3. Persistir el cambio (sobrescribir con modo 'w')
    try:
        with open(ruta_archivo, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(items_a_persistir)
        return True
    except IOError as e:
        print(f"\nError de E/S al sobrescribir el archivo '{ruta_archivo}': {e}")
        return False
    except Exception as e:
        print(f"\nOcurrió un error inesperado al guardar: {e}")
        return False


def modificar_producto(lista_global_items, FIELDNAMES):
    """ 
    (UPDATE) 
    Modifica un ítem en la lista de memoria y luego sobrescribe 
    el archivo CSV de origen para persistir el cambio.
    """ 
    print("\n--- 4. Modificar Producto ---") 
    
    # La lista global debe pasarse como argumento desde el módulo principal
    if not lista_global_items: 
        print("No hay datos cargados para modificar. Ejecuta la lectura primero.") 
        return 
    
    # --- 1. Identificación y Búsqueda ---
    id_a_modificar = input("Ingrese el ID del producto a modificar: ").strip() 
    
    item_encontrado = None 
    for item in lista_global_items: 
        if item.get('id') == id_a_modificar: 
            item_encontrado = item 
            break # Encontramos el item, rompemos el bucle 
    
    if item_encontrado: 
        print(f"Modificando: {item_encontrado.get('nombre', 'N/A')}") 
        
        # --- 2. Pedir nuevos datos y validar ---
        nuevo_precio_str = input(f"Nuevo precio (actual: {item_encontrado.get('precio', 0)}): ") 
        nuevo_stock_str = input(f"Nuevo stock (actual: {item_encontrado.get('stock', 0)}): ") 
        
        # Validación de numéricos 
        valido_precio, nuevo_precio = validar_numero_positivo(nuevo_precio_str) 
        valido_stock, nuevo_stock_num = validar_numero_positivo(nuevo_stock_str) 
        
        if not (valido_precio and valido_stock): 
            print("\nError en los datos (deben ser > 0 y numéricos). Modificación cancelada.") 
            return 
        
        # --- 3. Actualizar en memoria (el diccionario original de la lista) ---
        item_encontrado['precio'] = nuevo_precio 
        item_encontrado['stock'] = int(nuevo_stock_num) 
        
        ruta_original = item_encontrado.get('ruta_origen') 
        
        if not ruta_original: 
            print("Error: El ítem no tiene ruta de origen ('ruta_origen' no fue cargada). No se puede guardar.") 
            return 
        
        # --- 4. Persistir el cambio (Sobrescribir el CSV) ---
        # Usamos la función auxiliar para sobrescribir solo el archivo de origen
        if _sobrescribir_archivo_csv(ruta_original, lista_global_items, FIELDNAMES):
            print("\n¡Producto modificado exitosamente en disco!")
        # Si falla, la función auxiliar ya imprimió el error
            
    else: 
        print(f"No se encontró ningún producto con el ID: {id_a_modificar}") 


# --- Funciones de Persistencia (Delete) ---

def eliminar_producto(lista_global_items, FIELDNAMES):
    """ 
    (DELETE) 
    Elimina un ítem de la lista de memoria y luego sobrescribe 
    el archivo CSV de origen para persistir el cambio.
    """ 
    print("\n--- 5. Eliminar Producto ---") 
    
    # La lista global debe pasarse como argumento desde el módulo principal
    if not lista_global_items: 
        print("No hay datos cargados para eliminar.") 
        return 

    # --- 1. Identificación y Búsqueda ---
    id_a_eliminar = input("Ingrese el ID del producto a eliminar: ").strip() 

    item_encontrado = None 
    for item in lista_global_items: 
        if item.get('id') == id_a_eliminar: 
            item_encontrado = item 
            break 

    if item_encontrado: 
        
        # 2. Confirmación
        confirmar = input(f"¿Seguro que desea eliminar '{item_encontrado.get('nombre')}'? (s/n): ").lower() 
        if confirmar != 's': 
            print("Eliminación cancelada.") 
            return 
        
        # 3. Obtener ruta de origen antes de remover
        ruta_original = item_encontrado.get('ruta_origen') 

        if not ruta_original: 
            print("Advertencia: Ítem eliminado de memoria, pero no se pudo encontrar la ruta de origen.") 
            return 
        
        try: 
            # 4. Remover el ítem de la lista en memoria
            # ESTA ES LA ÚNICA ACCIÓN QUE MODIFICA lista_global_items
            lista_global_items.remove(item_encontrado) 
            
            # 5. Persistir el cambio (Sobrescribir el CSV)
            # La función auxiliar filtra los items restantes y reescribe el archivo.
            if _sobrescribir_archivo_csv(ruta_original, lista_global_items, FIELDNAMES):
                print("\n¡Producto eliminado exitosamente de memoria y disco!")

        except Exception as e: 
            # Captura errores de sobrescritura o de remoción
            print(f"\nOcurrió un error al intentar eliminar o guardar: {e}") 
    
    else: 
        print(f"No se encontró ningún producto con el ID: {id_a_eliminar}")
