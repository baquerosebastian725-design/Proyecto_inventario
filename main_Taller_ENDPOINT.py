from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field 
import json
from pathlib import Path
import asyncio



app = FastAPI()
ARCHIVO = Path("Taller.json")


async def leer_ordenes():
    if not ARCHIVO.exists():
        ARCHIVO.write_text("[]", encoding="utf-8")
    with ARCHIVO.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)
async def guardar_ordenes(ordenes):
    with ARCHIVO.open("w", encoding="utf-8") as archivo:
        json.dump(ordenes, archivo, indent=4, ensure_ascii=False)


class OrdenCreate(BaseModel):
    placa: str = Field(max_length=6)
    modelo: str
    falla_reportada: str
class OrdenUpdate(BaseModel):
    nuevo_estado: str
    costo_reparacion: float



@app.post("ordenes")
async def crear_orden(orden: OrdenCreate):
    ordenes = await leer_ordenes()
    for existente in ordenes:
        if existente["placa"] == orden.placa:
            if existente["estado"] != "Entregada":
                raise HTTPException(
                    status_code=400,
                    detail="La moto ya se encuentra en el taller"
                )
    nueva_orden = {
        "placa": orden.placa,
        "modelo": orden.modelo,
        "falla_reportada": orden.falla_reportada,
        "estado": "En diagnóstico",
        "costo_reparacion": 0
    }
    ordenes.append(nueva_orden)
    await guardar_ordenes(ordenes)
    return nueva_orden




@app.get("ordenes")
async def consultar_ordenes():
    ordenes = await leer_ordenes()
    return ordenes


@app.put("ordenes{placa}")
async def actualizar_orden(placa: str, datos: OrdenUpdate):
    ordenes = await leer_ordenes()
    for orden in ordenes:
        if orden["placa"] == placa:
            if datos.nuevo_estado == "Reparada":
                if datos.costo_reparacion <= 0:
                    raise HTTPException(
                        status_code=400,
                        detail=("El valor de la reparación debe ser mayor a cero para que sea la orden reparada")
                    )
            orden["estado"] = datos.nuevo_estado
            orden["costo_reparacion"] = datos.costo_reparacion
            await guardar_ordenes(ordenes)
            return orden
    raise HTTPException(
        status_code=404,
        detail="Orden no encontrada"
        )