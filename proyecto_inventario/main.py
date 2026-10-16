import asyncio
# Importar funciones de otro archivo
from database import crear_producto, obtener_producto , actualizar_Stock, eliminar_producto

async def prueba_de_estres():
    print("-----INICIANDO PREBA -----")
    tareas_creacion = [
        crear_producto("m001", "Llanta trasera ", 10),
        crear_producto("m002", "Filtro de Aire ", 25),
        crear_producto("m003", "Bujia ", 50)
    ]

    try:
        await asyncio.gather(*tareas_creacion)
        print("Productos creados exitosamente")
    except Exception as e:
        print(f"Error de Creacion:{e}")

    print("\n ")        