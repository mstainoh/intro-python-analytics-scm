# Anexo — Notas teóricas y conclusiones

Notas para acompañar el notebook `analisis_SUBE_2026`. Resumen de las decisiones de diseño, los hallazgos y —sobre todo— las consideraciones metodológicas a tener presentes al leer o extender el modelo.

---

## 1. Resumen del ejercicio

Se trabajó con los usos diarios de SUBE (2020–2026), enfocados en el AMBA, cruzados con las tarifas (boleto mínimo) de colectivo, subte y tren y con el IPC para deflactar. El notebook tiene tres partes: ingesta y limpieza (con checkpoint en parquet), análisis descriptivo, y un modelo predictivo de viajes diarios de subte con un what-if de precio.

---

## 2. Decisiones de datos

- **Foco en SUBE + tarifas; afuera radares y datos geo.** Los radares y los datos de barrios/paradas aportaban a un análisis de tráfico/georreferencia que quedó fuera de alcance. Mantenerlos sumaba dependencias pesadas (geopandas/folium) sin servir al objetivo de forecast.
- **Feriados curados a mano (con puentes).** Se prefirió la lista curada por sobre una librería automática porque los *feriados puente* se declaran por decreto y las librerías suelen errarlos. En transporte, el calendario es un driver de primer orden, así que la precisión importa.
- **Tarifa real, no nominal.** La tarifa nominal sube de forma monótona por inflación. Para cualquier análisis de demanda hay que usar la **tarifa real** (deflactada por IPC, en pesos constantes de ene-2020): `tarifa_real = tarifa × IPC_base / IPC_mes`. La demanda responde al precio relativo, no al número nominal.
- **Checkpoint en parquet.** La ingesta (descarga de varios años de CSV) es cara; el análisis y el modelo son baratos y se iteran mucho. Separar ambos con un checkpoint en parquet, más una guarda `try/except NameError`, permite correr el notebook completo de arriba a abajo *o* saltar directo a una sección.

---

## 3. Hallazgos descriptivos

- **Concentración (Pareto).** Pocas líneas de colectivo concentran la mayoría de los viajes del AMBA.
- **Estacionalidad de calendario fuerte.** Día de la semana (hábil vs fin de semana) y feriados explican gran parte de la varianza diaria. Es el efecto más limpio y predecible.
- **Tarifa real: congelamiento y salto.** En términos reales, la tarifa cayó fuerte durante el período de congelamiento y saltó con los aumentos de 2024–2025. El gráfico nominal (monótono) y el real (en U) cuentan historias opuestas: solo el real es interpretable económicamente.
- **Correlaciones, con cuidado.** La correlación viajes~precio está contaminada por la **tendencia común pos-pandemia**: tanto los viajes (recuperación) como los precios (inflación) crecen en el tiempo, generando correlación espuria. Usar tarifa real ayuda, pero la lectura honesta requiere detrendar o controlar la tendencia.

---

## 4. Notas de modelado

### 4.1 Validación temporal, no aleatoria
En una serie de tiempo, un split aleatorio mete el futuro en el entrenamiento (*data leakage*): el modelo interpola entre puntos vecinos en el tiempo e infla artificialmente la métrica. El split debe respetar el orden: **entrenar en el pasado, validar en el futuro** (acá train 2022–2025, test 2026). El ideal es validación *walk-forward* (ventana expansiva).

### 4.2 Tendencia y extrapolación (la lección central)
Sin un término de tendencia, el modelo solo repite el patrón estacional promedio y no proyecta crecimiento. Pero hay una sutileza decisiva:

> **Los modelos de árboles (RF, GBM) no extrapolan.** Para un valor de feature fuera del rango de entrenamiento, predicen el valor de la última hoja, es decir, **constante**.

Por eso, en el test 2026, el GBM "achata" la predicción: el `trend` queda fuera de rango y el modelo no puede seguir subiendo el nivel. El resultado es un sesgo sistemático: **sobrepredice al inicio del horizonte y subpredice al final** (su baseline plano queda por encima del piso estacional de enero y por debajo del crecimiento de mediados de año). El modelo **log-lineal**, en cambio, extrapola la tendencia y sigue al observado.

Implicancia práctica: para forecastear una serie con tendencia, usar un modelo que extrapole (lineal o de serie temporal), **o** detrendar primero y modelar el residuo estacional con el árbol.

### 4.3 Modelo log-log y elasticidades
Tomar `log(viajes)` y `log(tarifa)` hace que cada coeficiente de tarifa sea directamente una **elasticidad** (Δ% viajes por Δ% precio): interpretable y fácil de usar en el what-if (`Δ%viajes ≈ elasticidad × log(1+cambio)`).

### 4.4 Colinealidad de los precios
Las tres tarifas reales se mueven casi juntas en el tiempo. La colinealidad **no afecta la predicción agregada**, pero vuelve **inestables los coeficientes individuales** (varianza alta, signos que pueden invertirse). Por eso las elasticidades cruzadas hay que leerlas con pinzas. Mitigaciones: usar precio relativo (ratio), regularización (ridge), o no sobre-interpretar coeficientes sueltos.

### 4.5 Forecast condicional a un escenario
Para predecir el futuro se necesitan los valores futuros de las features. El calendario y la tendencia se derivan solos; pero la **tarifa futura es desconocida**, así que el forecast es **condicional a un escenario de tarifa** (acá: mantener la última tarifa real). Esto no es un defecto sino la naturaleza del problema, y es justamente lo que habilita el what-if ("¿y si la tarifa sube X%?").

### 4.6 Qué mide cada métrica
- **bias** (error medio firmado): sesgo sistemático. Un MAE bajo con bias alto = modelo corrido. El bias del GBM **cambia de signo** entre enero y junio: la firma de la falta de extrapolación.
- **MAE**: error absoluto medio, en unidades de viajes, robusto a outliers.
- **RMSE**: penaliza más los errores grandes (sensible a feriados mal predichos).
- **MAPE**: error porcentual, comparable entre escalas, pero explota con valores chicos (cuidado con días de muy bajo tráfico).

El **cross-plot predicho vs observado** complementa las métricas: un modelo bien calibrado se pega a la identidad `y=x`; un modelo que no extrapola muestra la nube "rotada" (puntos por encima de la línea en valores bajos, por debajo en valores altos).

---

## 5. El problema de identificación del precio

La estimación de elasticidad acá es **ilustrativa, no causal**. El precio no varía entre unidades en un mismo día; varía solo en el tiempo, en unos pocos escalones (≈una docena en seis años). Esos escalones coinciden con otros cambios (recuperación pos-pandemia, tendencia secular, decisiones de política), así que el "efecto precio" está **confundido** con todo lo que se movió en esas fechas. Un modelo con mes + tendencia + precio le atribuye casi todo al tiempo, y el coeficiente de precio queda mal identificado.

Para acercarse a lo causal haría falta: un **event-study** alrededor de cada salto de tarifa (antes/después, controlando estación) —incluido en el notebook como chequeo cruzado—, variables instrumentales, o explotar variación cruzada entre modos o jurisdicciones. Como regla: si los dos enfoques (coeficiente y event-study) coinciden en orden de magnitud, se le puede dar algo más de crédito.

---

## 6. Limitaciones

- **Falta un feature de vacaciones / receso escolar.** El pozo profundo de la primera semana de enero queda sub-capturado: el modelo "sabe" que enero es bajo (dummy de mes) pero no que *esa semana* se desploma. Solo está flageado el 1-ene, no el período de receso.
- **La agregación semanal suaviza los pozos de feriado.**
- **No hay clima, paros, cortes de servicio ni eventos**, que mueven la demanda diaria.
- **El IPC llega hasta abril 2026** → los últimos meses usan el último índice disponible (inflación levemente subestimada ahí).
- **Subte como proxy.** No se modelan la geografía ni la sustitución intramodal.
- **El primer punto de enero** puede ser, en parte, una semana de cobertura parcial del dato.

---

## 7. Extensiones posibles

- Agregar feature de **receso escolar / vacaciones** y de eventos conocidos.
- Probar **modelos de serie temporal** con estacionalidad explícita (SARIMA, ETS, Prophet, state-space).
- **Validación walk-forward** en lugar de un único corte.
- **Intervalos de predicción** (regresión cuantílica, conformal prediction) además del punto.
- **Detrend + árbol**: combinar la extrapolación del modelo lineal con la flexibilidad del GBM.
- **Modelar los modos en conjunto** (sistema de demanda) para capturar mejor la sustitución.
- **Regularización** (ridge/lasso) para la colinealidad de precios.

---

## 8. Notas de reproducibilidad e ingeniería

- **Checkpoint en parquet** para separar la ingesta cara del análisis barato, con guarda `try/except NameError` para correr cada parte de forma independiente.
- **`merge_asof`** para los joins de funciones escalón: asignar la tarifa vigente y el IPC del mes a cada fecha (dirección *backward*).
- **Robustez en la ingesta**: saltar años inexistentes (p.ej. el corriente, parcial) y coercionar/descartar filas basura (`errors="coerce"` + `dropna`).
- **Semilla fija** en el GBM para reproducibilidad.
- Usar **tarifa real** en el modelo también mitiga (parcialmente) la extrapolación de los árboles respecto al precio: a diferencia de la nominal, que crece monótona, la real se mantiene en una banda comparable en el tiempo.