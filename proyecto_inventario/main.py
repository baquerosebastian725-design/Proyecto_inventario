import asyncio
from database import crear_producto, obtener_producto, actualizar_stock, eliminar_producto, vender_producto

async def prueba_estres():
    print("-----Iniciando prueba--------")
    tarea_creacion = [
        crear_producto("m001", "llanta trasera", 10),
        crear_producto("m002", "Inyectores", 50),
        crear_producto("m003", "Tornillo culata", 25)
    ]

    try: 
        await asyncio.gather(*tarea_creacion)
        print("Productos creados exitosamente")
    except Exception as e:
        print(f"Error de creacpn: {e}")

    print("\nActualizar y consultar")
    try: 
        resultado = await asyncio.gather[
            actualizar_stock (8, "M001"),
            obtener_producto ("M002")
        ]
        
        print("Operaciones mixtas completas.")
        print(f"  -  Update devolution: {resultado[0]}")
        print(f"  -  Get devolution: {resultado[1]}")
    except Exception as e:
        print("Error en operaciones mixtas.")

async def intentar_venta(numero, codigo, cantidad):
    try:
        resultado = await vender_producto(codigo, cantidad)
        print(f"Venta es :{numero} y el resultado es: {resultado}")
    except ValueError as e:
        print(f"Venta es :{numero}: ValueError{e}")
    except KeyError as e:
        print(f"Venta es: {numero}: KeyError {e}")
    except Exception as e:
        print(f"Venta es:{numero}: error{e}")

async def simulacion_ventas():
    print("\n---- Procesando 4 ventas simultáneas -----")
    await asyncio.gather(
        intentar_venta(1, "m001", 2),     # venta y lo que queda en el stock
        intentar_venta(2, "m003", 24),    # queda en 1 y lanza la alerta
        intentar_venta(3, "m002", 500),   # pide mas 
        intentar_venta(4, "m999", 1),     # producto que no existe
    )
    print("Todas las ventas respondieron (las alertas siguen en segundo plano)...")
    await asyncio.sleep(3)  # da tiempo a que la alerta termine para que despues cierre 
    

async def main():
    await prueba_estres()
    await simulacion_ventas()

asyncio.run(main())