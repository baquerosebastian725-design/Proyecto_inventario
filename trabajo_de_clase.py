import asyncio
import time

async def ingresar_mascota(nombre, tiempo_horas):
    try:
        print(f"Ingresando a {nombre} a la veterinaria")
        await asyncio.sleep(2)
        print(f"{nombre} lleva {tiempo_horas} horas en la veterinaria")

    except Exception as e:
        print(f"Error al ingresar a la mascota: {e}")


async def examinar_mascota(nombre, sintomas):
    try:
        print(f"Examinando a {nombre}")
        await asyncio.sleep(3)

        if sintomas == "vomito":
            print(f"{nombre} necesita tratamiento veterinario")
            estado = "delicado"

        elif sintomas == "fiebre":
            print(f"{nombre} necesita medicamentos")
            estado = "delicado"

        else:
            print(f"{nombre} está saludable")
            estado = "saludable"

        print("Examen finalizado")
        return estado

    except Exception as e:
        print(f"Error al examinar a {nombre}: {e}")
        return "error"


async def calcular_hidratacion(peso_kg, tiempo_horas):
    try:
        if tiempo_horas <= 0:
            raise Exception("El tiempo debe ser mayor que cero")

        constante_hidratacion = 50
        hidratacion = peso_kg * constante_hidratacion / tiempo_horas

        print(f"La mascota necesita {hidratacion} ml")

    except Exception as e:
        print(f"Error en los datos de hidratación: {e}")

    except Exception as e:
        print(f"Error al calcular la hidratación: {e}")

async def realizar_diagnostico(nombre, peso_kg, sintomas, tiempo_horas):
    try:
        await ingresar_mascota(nombre, tiempo_horas)

        estado = await examinar_mascota(nombre, sintomas)

        if estado == "delicado":
            await calcular_hidratacion(peso_kg, tiempo_horas)

        elif estado == "saludable":
            print(f"{nombre} no requiere hidratación")

        else:
            print(f"No se completo el diagnóstico de {nombre}")

        print(f"Diagnóstico de {nombre}: {estado}")

    except Exception as e:
        print(f"Error en el diagnóstico de {nombre}: {e}")

async def main():
    try:
        tareas = [
            realizar_diagnostico("Manolo", 10, "vomito", 2),
            realizar_diagnostico("Thor", 15, "saludable", 3),
            realizar_diagnostico("Doky", 8, "fiebre", 4)
        ]

        await asyncio.gather(*tareas)

    except Exception as e:
        print(f"Error al ejecutar las tareas: {e}")

try:
    asyncio.run(main())

except Exception as e:
    print(f"Error al iniciar el programa: {e}")
