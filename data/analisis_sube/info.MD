# Datos de Transporte AMBA

Este directorio contiene series históricas de tarifas nominales (ARS) del transporte público en el Área Metropolitana de Buenos Aires (AMBA), junto con el IPC para deflactación. Se utiliza para análisis exploratorio, modelado económico y ejercicios de analytics.

## 📁 Archivos

### Tarifas (boleto mínimo)
- `precio_colectivo.csv`
- `precio_subte.csv`
- `precio_tren.csv`

Cada archivo representa el valor del boleto mínimo (tramo base) para cada modo de transporte.

### Índice de Precios al Consumidor
- `ipc.csv` — IPC mensual (índice de nivel), 2018–2026, para deflactación de tarifas nominales en pesos constantes.

---

## 📊 Estructura de los datos

### Tarifas (`precio_*.csv`)

Columnas:

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `fecha_desde` | date | Fecha de entrada en vigencia del cuadro tarifario (YYYY-MM-DD) |
| `valor_ars` | float | Tarifa nominal en pesos argentinos (ARS, pesos corrientes) |
| `notas` | str | Descripción cualitativa (ej: "aumento", "quita de subsidios", "indexación") |

### IPC (`ipc.csv`)

Columnas:

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `fecha` | date | Primer día del mes (YYYY-MM-01) |
| `ipc` | float | Índice de nivel IPC (base móvil, INDEC) |

---

## 🚍 Cobertura

- **Región:** Área Metropolitana de Buenos Aires (AMBA)
- **Tipo de tarifa:** boleto mínimo (tramo más corto / sección 1)
- **Unidad (tarifas):** pesos corrientes (nominales), sin ajuste por inflación
- **Período (IPC):** 2018-01 a 2026-04

---

## 💡 Uso: Tarifa Real vs Nominal

Las tarifas se guardan en **pesos corrientes (nominales)**. Para análisis económico (elasticidad, demanda), usar la **tarifa real** (deflactada):

```
tarifa_real = tarifa_nominal × IPC(base) / IPC(mes)
```

Ejemplo: tarifa real en pesos constantes de enero 2020:

```
IPC_ene_2020 = 289.83 (aproximado)
tarifa_real = valor_ars × 289.83 / IPC(mes_observado)
```

La tarifa real es lo que importa económicamente: muestra la evolución del poder de compra (si sube en términos reales, es un encarecimiento; si baja, es baratura relativa). La nominal sube por inflación aunque la demanda se comporte igual.

---

## ⚠️ Consideraciones metodológicas

### Variabilidad
Los valores pueden variar según:
- **Jurisdicción:** Nacional (subte), CABA, Provincia de Buenos Aires
- **Línea o servicio:** algunos servicios tienen tarifas especiales
- **Tarjeta o tipo de usuario:** aquí se reporta el boleto mínimo para usuario general

Se utiliza una serie representativa para análisis agregado (proxy de costo de transporte).

### Confiabilidad
- **Tarifas:** compiladas de normativas y anuncios oficiales; pueden tener lag respecto a la publicación formal.
- **IPC:** fuente INDEC (Instituto Nacional de Estadísticas y Censos, Argentina). Datos sujetos a revisiones metodológicas.

### Limitaciones
- No captan subsidios específicos (estudiantes, jubilados, tarjetas reducidas).
- El IPC es agregado nacional; puede no reflejar exactamente la CPI de transporte en AMBA.
- Para períodos post-datos (junio 2026 en adelante), usar el último IPC disponible en interpolación.

---

## 📚 Análisis relacionado

El notebook `analisis_SUBE.ipynb` (en `../notebooks/`) integra estos datos con usos diarios SUBE desde 2020, realiza análisis descriptivo y un modelo predictivo con elasticidad de precio. Para contexto teórico, ver `docs/anexo_SUBE_2026.md`.