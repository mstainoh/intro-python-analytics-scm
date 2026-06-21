# Introducción a Python para Supply Chain Analytics

Material de nivelación y práctica para un máster en Supply Chain Analytics.
El objetivo es que alumnos sin experiencia previa puedan **leer código Python simple y entender qué hace**.

## Pre-clase: nivelación asincrónica (~2 h)

### 1. Lecturas recomendadas

Está lleno en internet de material introductorio. Recomendaciones:

- En YouTube, buscá **"Aprende Python - Curso completo para principiantes"** en el canal
  [freeCodeCamp Español](https://www.youtube.com/freecodecampespanol).
  Solo necesitás ver los **primeros 35–40 minutos** (hasta variables y operadores).
- [Python for Everybody](https://www.py4e.com/) — curso bien sencillo con material y videos.
  Con los primeros 10 capítulos es más que suficiente.

### 2. Notebook introductoria en Google Colab (45–60 min)

Hacé click para abrirla directo en tu navegador, sin instalar nada:

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mstainoh/intro-python-analytics-scm/blob/main/notebooks/python_intro_supply_chain.ipynb)

> Solo necesitás una cuenta de Google. Ejecutá cada celda en orden con el botón ▶️.

Contenido: variables, listas, `if`, `for`, EOQ, pandas, y gráficos — todo con ejemplos de supply chain.

## Notebooks de clase

| Notebook | Tema | Nivel | Duración |
|---|---|---|---|
| `python_intro_supply_chain.ipynb` | Fundamentos de Python con ejemplos SCM | Introductorio | ~90 min |
| `Market_Basket_analysis.ipynb` | Análisis de canasta (apriori, asociación) | Intermedio | ~60 min |
| `analisis_SUBE_2026.ipynb` | Análisis predictivo de demanda de transporte (AMBA) | Intermedio-avanzado | ~90 min |
| `analisis_SUBE.ipynb` | Análisis exploratorio de transporte público (legacy) | Intermedio | ~45 min |

### 🚆 Sobre el análisis de transporte (SUBE)

El notebook `analisis_SUBE_2026.ipynb` es una actualización completa de análisis de transporte público en el AMBA (2020–2026) que incluye:

- **Parte 1:** Ingesta de datos SUBE + tarifas reales + IPC + checkpoint en parquet
- **Parte 2:** Análisis descriptivo (Pareto, estacionalidad, tarifas nominal vs real)
- **Parte 3:** Modelo predictivo de viajes diarios de subte + elasticidades de precio + what-if

**Para el contexto teórico completo** (decisiones metodológicas, limitaciones, notas de modelado), ver [`docs/anexo_SUBE_2026.md`](docs/anexo_SUBE_2026.md).

Para documentación de datos (fuentes, schema, deflactación), ver [`data/analisis_sube/README.md`](data/analisis_sube/README.md).

## Cómo correr un notebook localmente

### 1. Clonar el repo
```bash
git clone https://github.com/mstainoh/intro-python-analytics-scm.git
cd intro-python-analytics-scm
```

### 2. Crear un entorno virtual (recomendado)
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
```

Para el notebook de SUBE además:
```bash
pip install pyarrow
```

### 4. Lanzar Jupyter
```bash
jupyter notebook
```

Luego abrí el notebook que quieras desde la interfaz.

## Estructura del repo

```
.
├── README.md                          # Este archivo
├── LICENSE
├── docs/
│   └── anexo_SUBE_2026.md            # Contexto teórico del modelo predictivo
├── data/
│   ├── analisis_sube/
│   │   ├── README.md                 # Diccionario de datos, fuentes
│   │   ├── precio_colectivo.csv
│   │   ├── precio_subte.csv
│   │   ├── precio_tren.csv
│   │   ├── ipc.csv
│   │   └── info.MD
│   ├── countries/
│   │   ├── countries.csv
│   │   └── countries.geojson
│   └── groceries/
│       └── Groceries_dataset.csv
├── notebooks/
│   ├── python_intro_supply_chain.ipynb
│   ├── Market_Basket_analysis.ipynb
│   ├── analisis_SUBE_2026.ipynb       # Nuevo: análisis predictivo completo
│   └── analisis_SUBE.ipynb            # Legacy
└── scripts/
    └── download_ipc.py
```

## Licencia

MIT