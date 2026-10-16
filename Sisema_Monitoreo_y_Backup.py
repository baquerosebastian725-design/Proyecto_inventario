import asyncio
import json
import time
import aiofiles

SIMULAR_DISCO_LENTO = True


async def monitorear_sistema():
    while True:
        print(f"[{time.strftime('%X')}] Monitor: Sistema funcionando OK...")
        await asyncio.sleep(2)


async def hacer_backup(archivo_origen, archivo_destino):
    print(f"[{time.strftime('%X')}] Backup: leyendo {archivo_origen}...")
    async with aiofiles.open(archivo_origen, mode="r", encoding="utf-8") as f:
        texto_json = await f.read()

    datos = json.loads(texto_json)
    if SIMULAR_DISCO_LENTO:
        await asyncio.sleep(2)
    async with aiofiles.open(archivo_destino, mode="w", encoding="utf-8") as f:
        await f.write(json.dumps(datos, indent=4))

    print(f"[{time.strftime('%X')}] Backup: copia guardada en {archivo_destino}")


async def main():
    print(" Sistema de Monitoreo y Backup de Taller")
    tarea_monitor = asyncio.create_task(monitorear_sistema())

    try:
        await asyncio.wait_for(hacer_backup("inventario.json", "backup.json"),timeout=1.0)
    except asyncio.TimeoutError:
        print("Alerta: El backup falló por lentitud del disco")
    except json.JSONDecodeError:
        print("Error: El archivo inventario.json tiene la estructura rota")
    except FileNotFoundError:
        print("Error: No se encontró el archivo inventario.json")

    await asyncio.sleep(3)
    tarea_monitor.cancel()
    print("Fin del programa")


asyncio.run(main())