# Datos de Transporte AMBA

Este directorio contiene series históricas de tarifas nominales (ARS) del transporte público en el Área Metropolitana de Buenos Aires (AMBA), utilizadas para análisis exploratorio, modelado económico y ejercicios de analytics.

## 📁 Archivos

- `precio_colectivo.csv`
- `precio_subte.csv`
- `precio_tren.csv`

Cada archivo contiene la misma estructura y representa el valor del boleto mínimo (tramo base) para cada modo de transporte.

---

## 📊 Estructura de los datos

Columnas:

- `fecha_desde`: fecha de entrada en vigencia del cuadro tarifario (formato YYYY-MM-DD)
- `valor_ars`: tarifa nominal en pesos argentinos (ARS)
- `notas`: descripción cualitativa del cambio (ej: aumento, quita de subsidios, indexación, etc.)

---

## 🚍 Cobertura

- Región: Área Metropolitana de Buenos Aires (AMBA)
- Tipo de tarifa: boleto mínimo (tramo más corto / sección 1)
- Unidad: pesos corrientes (no ajustado por inflación)

---

## ⚠️ Consideraciones metodológicas

- Los valores pueden variar según:
  - jurisdicción (Nación, CABA, Provincia)
  - línea o servicio específico
- Se utiliza una serie representativa para análisis agregado (proxy de costo de transporte).
