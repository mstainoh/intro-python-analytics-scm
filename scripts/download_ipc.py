"""
Descarga datos del IPC (Índice de Precios al Consumidor) de Argentina desde
la API oficial de datos.gob.ar y los guarda localmente para análisis reproducible.

Este script obtiene la serie de IPC nivel general nacional (frecuencia mensual,
base diciembre 2016), la procesa en un DataFrame limpio de pandas y la guarda
como archivo CSV dentro del directorio de datos del repositorio.

Salida:
    data/ipc.csv

Columnas:
    - fecha (datetime): fecha de la observación (frecuencia mensual)
    - ipc (float): nivel del índice IPC (no es tasa de inflación)

Fuente:
    https://apis.datos.gob.ar/series/api/series
    ID de serie: 148.3_INIVELNAL_DICI_M_26

Características:
    - Descarga datos desde 2018 (configurable)
    - Valida la respuesta de la API
    - Convierte tipos de datos correctamente
    - Ordena cronológicamente
    - Guarda el archivo en una ruta relativa al repositorio

Uso esperado:
    python scripts/update_ipc.py

Notas:
    - Los valores corresponden a niveles del índice (no variaciones porcentuales)
    - Es apto para deflactar series nominales (ej: tarifas de transporte)
    - Para análisis en términos reales, se recomienda normalizar el IPC a una base

Ejemplo de uso posterior:
    precio_real = precio_nominal / (ipc / ipc_base)

Autor:
    Parte del repositorio intro-python-analytics-scm
"""

import requests
import pandas as pd
from pathlib import Path

# output path relativo al repo
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "ipc.csv"

url = "https://apis.datos.gob.ar/series/api/series"

params = {
    "ids": "148.3_INIVELNAL_DICI_M_26",
    "format": "json",
    "start_date": "2018-01-01"
}

r = requests.get(url, params=params)
data = r.json()

# IMPORTANTE: nombre correcto de key
if 'data' not in data:
  raise ValueError(f'No se pudo descargar los datos de {url} - response (<200 chars): {str(data)[:200]}')

df = pd.DataFrame(data["data"], columns=["fecha", "ipc"])

df["fecha"] = pd.to_datetime(df["fecha"])
df['ipc'] = pd.to_numeric(df['ipc'])
df = df.sort_values("fecha")

print('Data downloaded - last 3 rows:')
print(df.tail(3))
print()

df.to_csv(OUTPUT_PATH)