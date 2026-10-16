import json
import aiofiles
import asyncio

ARCHIVO_BD = "inventario.json"

async def leer_base_datos():
    try: 
        async with aiofiles.open(ARCHIVO_BD, mode='r' , encoding='utf-8') as f:
            contenido = await f.read()
            return json.loads(contenido)
    except FileNotFoundError:
        return []  # Retorna una lista vacía si el archivo no existe  

async def guardar_base_datos(datos):
    async with aiofiles.open(ARCHIVO_BD, mode='w', encoding='utf-8') as f:
        await f.write(json.dumps(datos, indent=4))

# === Create === Post

async def crear_producto(codigo, nombre, stock):
    #Simular latencia
    await asyncio.sleep(0.5)
    datos = await leer_base_datos()

    for dato in datos:
        if dato['codigo'] == codigo:#son los parametros de la funcion y el dato que ya existe en la base de datos
            raise ValueError(f"El producto con el código {codigo} ya existe.")
        
    nuevo_producto = {"codigo": codigo,"nombre": nombre,"stock": stock}
    datos.append(nuevo_producto)#agregar a los datos que ya existen el nuevo producto
    await guardar_base_datos(datos)#guarda el archivo con el nuevo producto
    return nuevo_producto#devuelve el nuevo producto creado

#=== Read === Get

async def obtener_producto(codigo):
    await asyncio.sleep(0.2)
    datos = await leer_base_datos()
    for dato in datos:
        if dato['codigo'] == codigo:
            return dato
    raise KeyError(f"Producto {codigo} no ha sido encontrado.")

#=== Update === Put

async def actualizar_stock(nuevo_stock, codigo):
    await asyncio.sleep(0.5)
    datos = await leer_base_datos()

    for dato in datos:
        if dato ["codigo"] == codigo:
            dato["stock"] = nuevo_stock
            await guardar_base_datos
            return dato
    raise KeyError(f"Producto {codigo} no ha sido encontrado.")

# === Delete ===

async def eliminar_producto(codigo):
    await asyncio.sleep(0.5)
    datos = await leer_base_datos()

    nuevos_datos = [dato for dato in datos if dato["codigo"] != codigo]