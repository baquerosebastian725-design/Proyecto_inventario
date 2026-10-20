import json
import aiofiles
import asyncio

ARCHIVO_BD = "Inventario.json"

# Bloqueo para evitar que varias operaciones modifiquen
# el inventario al mismo tiempo.
db_lock = asyncio.Lock()

# Lista para registrar las tareas de alertas pendientes.
tareas_alerta = []


async def leer_base_datos():
    try:
        async with aiofiles.open(
            ARCHIVO_BD, mode="r", encoding="utf-8"
        ) as f:
            contenido = await f.read()
            return json.loads(contenido)

    except FileNotFoundError:
        return []


async def guardar_base_datos(datos):
    async with aiofiles.open(
        ARCHIVO_BD, mode="w", encoding="utf-8"
    ) as f:
        await f.write(json.dumps(datos, indent=4, ensure_ascii=False))


async def crear_producto(codigo, nombre, stock):
    async with db_lock:
        await asyncio.sleep(0.5)
        datos = await leer_base_datos()

        for dato in datos:
            if dato["codigo"] == codigo:
                raise ValueError(
                    f"El producto con el código {codigo} ya existe."
                )

        nuevo_producto = {
            "codigo": codigo,
            "nombre": nombre,
            "stock": stock
        }

        datos.append(nuevo_producto)
        await guardar_base_datos(datos)

        return nuevo_producto


# Buscar un producto por su código.
async def obtener_producto(codigo):
    async with db_lock:
        datos = await leer_base_datos()

        for dato in datos:
            if dato["codigo"] == codigo:
                return dato

        raise KeyError(f"Producto {codigo} no encontrado.")


# Simular una alerta de stock bajo.
async def alerta_stock_bajo(codigo, nombre, stock):
    await asyncio.sleep(2)

    print(
        f">>> ALERTA ADMIN: '{nombre}' ({codigo}) "
        f"tiene stock bajo: {stock} unidades."
    )


# Vender un producto y actualizar el inventario.
async def vender_producto(codigo, cantidad_vendida):
    async with db_lock:
        await asyncio.sleep(0.5)
        datos = await leer_base_datos()

        producto = None

        for dato in datos:
            if dato["codigo"] == codigo:
                producto = dato
                break

        # Verificar que el producto exista.
        if producto is None:
            raise KeyError(f"Producto {codigo} no encontrado.")

        # Validar la cantidad que se desea vender.
        if cantidad_vendida <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        if cantidad_vendida > producto["stock"]:
            raise ValueError("Stock insuficiente.")

        # Descontar las unidades vendidas.
        producto["stock"] -= cantidad_vendida

        await guardar_base_datos(datos)

        # Crear una alerta cuando queden menos de 3 unidades.
        if producto["stock"] < 3:
            tarea = asyncio.create_task(
                alerta_stock_bajo(
                    producto["codigo"],
                    producto["nombre"],
                    producto["stock"]
                )
            )
            tareas_alerta.append(tarea)

        return {
            "Mensaje": "Venta realizada correctamente",
            "Codigo": codigo,
            "PRODUCTO": producto["nombre"],
            "CANTIDAD_VENDIDA": cantidad_vendida,
            "STOCK_RESTANTE": producto["stock"]
        }