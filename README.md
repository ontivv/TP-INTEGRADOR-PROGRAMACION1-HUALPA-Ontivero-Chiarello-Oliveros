# TP-INTEGRADOR-PROGRAMACION1-HUALPA-Ontivero-Chiarello-Oliveros

# Sistema de Gestión de inventario jerárquico

En este proyecto se implementa una gestion de inventario CRUD.Su característica principal es el uso de persistencia avanzada mediante una estructura de directorios jerárquica que se gestiona mediante un sistema de archivos.

Estructura jerárquica:

nivel 1 (Raiz):La carpeta raíz llamada .\datos\ .En esta carpeta se contiene toda la informacion estructurada jerarquicamente.


nivel 2 (Categorias):Dentro de la carpeta datos a partir del sistema de gestion de archivos dinamicamente.


Nivel 3 (Marca): Dentro de cada carpeta de Categoría, se crean subcarpetas basadas en la Marca del producto.

Archivo (Datos): Dentro de la carpeta de Marca, se almacena un archivo items.csv que contiene los productos (diccionarios) correspondientes a esa jerarquía específica.

---------------------------------------------------------------------------------------------------------

# Módulos del Proyecto

main.py: Menú principal e iniciador del programa
.
lectura.py: Carga recursiva de datos (cargar_datos_recursivo) y funciones de 
muestra/filtrado.

crud.py: Funciones que escriben en disco (Alta, Modificación, Eliminación).

estadisticas.py: Calcula estadísticas (promedios, conteos) y ordena los datos.

validaciones.py: Funciones reutilizables para validar entradas (números positivos, no vacíos).

# LINK DEL VIDEO:

https://drive.google.com/file/d/1f9OfXvqVxYe3klh_EvnrsX_Bh3LAIKXm/view?usp=sharing

# LINK DEL REPO:

https://github.com/ontivv/TP-INTEGRADOR-PROGRAMACION1-HUALPA-Ontivero-Chiarello-Oliveros.git