import json
import aiofiles
import asyncio

ARCHIVO_BD = "Inventario.json"
db_lock = asyncio.Lock()


async def leer_base_datos():
    try:
        async with aiofiles.open(ARCHIVO_BD, mode="r", encoding="utf-8") as f:
            contenido = await f.read()
            return json.loads(contenido)
    except FileNotFoundError:
        return [] # lista vacia si el archivo no existe

async def guardar_base_datos(datos):
    async with aiofiles.open(ARCHIVO_BD, mode="w", encoding="utf-8") as f:
        await f.write(json.dumps(datos, indent=4))

async def crear_producto(codigo, nombre, stock):# la info dentro del () son parametros
    async with db_lock:

        await asyncio.sleep(0.5)
        datos = await leer_base_datos()

        for dato in datos:
            if dato["codigo"] == codigo:
                raise ValueError(f"El producto con el codigo {codigo} ya existe.")
            
        nuevo_producto = {"codigo": codigo, "nombre": nombre, "stock": stock}
        datos.append(nuevo_producto)# agregar a los datos que ya existen el nuevo producto
        await guardar_base_datos(datos)
        return nuevo_producto

#obtener_producto, actualizar_stock y eliminar_producto quedan 

async def alerta_stock_bajo(codigo, nombre, stock):
    await asyncio.sleep(2)  # simula el envío de la notificación al administrador
    print(f"   >>> ALERTA ADMIN: '{nombre}' ({codigo}) tiene stock bajo: {stock} unidades.")

async def vender_producto(codigo, cantidad_vendida):
    async with db_lock:

        await asyncio.sleep(0.5)
        datos = await leer_base_datos()
        for dato in datos:
            if dato["codigo"] == codigo:
                producto = dato
                break
        if producto:
            raise KeyError("Producto no encontrado")

        # Validación
        if cantidad_vendida > producto["stock"]:
            raise ValueError("Stock insuficiente")

        producto["stock"] -= cantidad_vendida
        await guardar_base_datos(datos)

        if producto["stock"] < 3: 
            tarea = asyncio.create_task(alerta_stock_bajo(producto["codigo"], producto["nombre"], producto["stock"]))
            tareas_alerta.append(tarea)

        # Retorno
        return {
            "Mensaje": "Se vendio la Venta",
            "Codigo": codigo,
            "PRODUCTO": producto["nombre"],
            "CANTIDAD_VENDIDA": cantidad_vendida,
            "STOCK_RESTANTE": producto["stock"],
            }