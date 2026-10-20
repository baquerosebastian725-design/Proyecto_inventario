from fastapi import FastAPI, HTTPException
from database import (
    leer_base_datos,
    obtener_producto,
    crear_producto,
    vender_producto
)

# Inicializar la aplicación
apiRest = FastAPI(
    title="API Inventarios SENA",
    description="Mi primera API asíncrona",
    version="1.0.0"
)


# Ruta principal
@apiRest.get("/")
async def ruta_principal():
    return {
        "Mensaje": "Bienvenido a mi primera API"
    }


# Estado del servidor
@apiRest.get("/estado")
async def estado_servidor():
    return {
        "status": "En línea",
        "servicios": "Operativos sin ningún inconveniente"
    }


# Ruta de suma
@apiRest.get("/suma")
async def estado_suma():
    return {
        "Suma": "2 + 78 = 80"
    }


# Listar todos los productos
@apiRest.get("/productos")
async def lista_productos():
    datos = await leer_base_datos()

    return {
        "Cantidad": len(datos),
        "Productos": datos
    }


# Buscar un producto por su código
@apiRest.get("/productos/{codigo_producto}")
async def buscar_un_producto(codigo_producto: str):
    try:
        producto = await obtener_producto(codigo_producto)
        return producto

    except KeyError:
        raise HTTPException(
            status_code=404,
            detail="El producto no existe en el inventario"
        )


# Listar las categorías existentes.
# Los productos actuales deben tener una clave "categoria"
# para aparecer en esta lista.
@apiRest.get("/categorias")
async def lista_categorias():
    datos = await leer_base_datos()

    categorias = sorted({
        producto["categoria"]
        for producto in datos
        if "categoria" in producto
    })

    return {
        "Categorías": categorias
    }


# Consultar productos con stock bajo
@apiRest.get("/alertas/stock")
async def alertas_stock():
    datos = await leer_base_datos()

    alertas = [
        producto
        for producto in datos
        if producto.get("stock", 0) < 5
    ]

    return {
        "Cantidad de alertas": len(alertas),
        "Productos con stock bajo": alertas
    }


# Buscar productos por nombre
@apiRest.get("/productos/buscar/{palabra_clave}")
async def buscar_productos(palabra_clave: str):
    datos = await leer_base_datos()

    productos_encontrados = [
        producto
        for producto in datos
        if palabra_clave.lower() in producto["nombre"].lower()
    ]

    return {
        "Cantidad": len(productos_encontrados),
        "Productos encontrados": productos_encontrados
    }