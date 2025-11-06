# --- en lectura.py ---
import os
import csv

CARPETA_RAIZ = "datos"

def cargar_datos_recursivo(ruta_actual):
    """
    Recorre recursivamente la estructura de carpetas desde 'ruta_actual',
    lee todos los archivos 'items.csv' y consolida los datos
    en una única lista de diccionarios.
    """
    lista_global_items = []

    try:
        elementos = os.listdir(ruta_actual)
    except FileNotFoundError:
        print(f"Advertencia: El directorio '{ruta_actual}' no existe. Creándolo.")
        os.makedirs(CARPETA_RAIZ, exist_ok=True)
        return []
    except OSError as e:
        print(f"Error de OS al leer la ruta {ruta_actual}: {e}")
        return []

    if not elementos:
        return [] # Directorio vacío

    for elemento in elementos:
        ruta_completa = os.path.join(ruta_actual, elemento)

        if os.path.isdir(ruta_completa):
            items_hijos = cargar_datos_recursivo(ruta_completa)
            lista_global_items.extend(items_hijos)
        
        elif os.path.isfile(ruta_completa) and elemento == "items.csv": # O el nombre que uses
            try:
                with open(ruta_completa, mode='r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    
                    for fila in reader:
                        try:
                            # Convertimos los strings a números
                            fila['precio'] = float(fila['precio'])
                            fila['stock'] = int(fila['stock'])
                            
                            # Guardamos la ruta de origen
                            fila['ruta_origen'] = ruta_completa
                            
                            # Solo agregamos la fila si la conversión fue exitosa
                            lista_global_items.append(fila)
                            
                        except (ValueError, TypeError, KeyError) as e:
                            # Si 'precio' o 'stock' no son números,
                            # o falta una clave, la fila está corrupta.
                            print(f"Error: Dato corrupto en {ruta_completa}. Fila omitida: {fila}. Error: {e}")
                            continue # Salta esta fila y sigue con la siguiente
                        
                        
            except IOError as e:
                print(f"Error de E/S al leer {ruta_completa}: {e}")
            except Exception as e:
                print(f"Error inesperado procesando {ruta_completa}: {e}")

    return lista_global_items

def mostrar_todos_los_items(lista_items):
    """
    Muestra una lista formateada de todos los ítems que recibe.
    Esta función es reutilizable: sirve para mostrar la lista
    completa o una lista ya filtrada.
    """
    
    if not lista_items: #verificamos si la lista está vacía o no
        print("\n-----------------------------------------------------")
        print("No se encontraron productos.")
        print("-----------------------------------------------------")
        return 
    
    print(f"\n --- MOSTRANDO {len(lista_items)} PRODUCTO/S ---")
    for item in lista_items:
        print("-" * 40)
        #intentamos extraer la jerarquía de datos para mostrar la lista de items
        try:
            partes_ruta = item["ruta_origen"].split(os.sep)
            jerarquia = f"({partes_ruta[1]} / {partes_ruta[2]})" #asumimos la estructura datos\Nivel1\Nivel2\archivo

        except (KeyError, IndexError):
            jerarquia = "(Jerarquía desconocida)"

        try:
            #formateamos los datos principales
            print(f"  ID:     {item['id']}")
            print(f"  Nombre: {item['nombre']} {jerarquia}")
            print(f"  Precio: ${item['precio']:.2f}") # .2f = 2 decimales
            print(f"  Stock:  {item['stock']} unidades")
        
        except KeyError as e:
            #si a algun item le falta "id","nombre","precio","stock"
            print(f"    Error: Ítem mal formado. Le falta una clave {e}")
    
    print("-" * 40)


def filtrar_por_atributo(lista_global_items):
    """
    Permite al usuario filtrar la lista global por un atributo
    y un valor, y luego muestra los resultados usando
    la función mostrar_todos_los_items.
    """
    print("\n--- 3. Filtrar Productos ---")
    if not lista_global_items:
        print("No hay productos cargados para filtrar.")
        return

    print("Puede filtrar por 'nombre', 'marca' o 'categoria'.")
    # Nota: 'marca' y 'categoria' los extraemos de 'ruta_origen'
    
    atributo = input("Ingrese el atributo por el que desea filtrar: ").strip().lower()
    
    if atributo not in ['nombre', 'marca', 'categoria']:
        print("Error: Atributo no válido. Debe ser 'nombre', 'marca' o 'categoria'.")
        return

    valor_buscado = input(f"Ingrese el {atributo} que desea buscar: ").strip().lower()
    
    if not valor_buscado:
        print("Error: El valor de búsqueda no puede estar vacío.")
        return

    lista_filtrada = []
    for item in lista_global_items:
        try:
            if atributo == 'nombre':
                # Buscamos si el valor está CONTENIDO en el nombre (flexible)
                if valor_buscado in item['nombre'].lower():
                    lista_filtrada.append(item)
            
            else:
                # Para marca/categoria, extraemos de la ruta
                # datos/Categoria/Marca/items.csv
                partes_ruta = item['ruta_origen'].split(os.sep)
                categoria_item = partes_ruta[1].lower()
                marca_item = partes_ruta[2].lower()

                if atributo == 'categoria' and valor_buscado == categoria_item:
                    lista_filtrada.append(item)
                elif atributo == 'marca' and valor_buscado == marca_item:
                    lista_filtrada.append(item)

        except (KeyError, IndexError):
            # Si el ítem no tiene 'nombre' o 'ruta_origen'
            continue 

    # 3. Reutilizamos nuestra función de mostrar
    print(f"\nResultados del filtro ({atributo} = '{valor_buscado}'):")
    mostrar_todos_los_items(lista_filtrada)