# NYC Mobility Intelligence 🚕

## Proyecto Integrador: Arquitectura y Estrategia de Big Data

**NYC Mobility Intelligence** es una solución integral de Big Data diseñada para transformar datos masivos de viajes de vehículos de transporte de alto volumen (FHVHV) de la ciudad de Nueva York en información útil para la toma de decisiones operativas y estratégicas.

El proyecto procesa **15.86 GiB de datos originales en formato Parquet**, correspondientes a **684,376,551 viajes registrados entre enero de 2022 y diciembre de 2024**. La solución integra Google Cloud Storage, Google Dataproc, PySpark, MariaDB, SQL y Streamlit para construir un pipeline escalable desde la ingesta de datos hasta su visualización ejecutiva.

---

## 1. Problema de negocio

Los sistemas de movilidad generan cientos de millones de registros individuales de viajes. Este volumen dificulta el análisis mediante herramientas convencionales como hojas de cálculo, bases de datos locales o scripts simples.

El proyecto busca transformar este volumen de información histórica en un producto analítico que permita a los responsables de planeación y operación comprender:

- Cómo cambia la demanda de movilidad a lo largo del tiempo.
- Qué horas y días concentran el mayor volumen de viajes.
- Cómo se comportan la duración y velocidad promedio de los viajes.
- Qué zonas concentran mayor actividad de origen y destino.
- Cómo evolucionan la tarifa base de los pasajeros y el pago a conductores.

El objetivo no es únicamente procesar grandes volúmenes de datos, sino convertirlos en información accesible para apoyar decisiones operativas y estratégicas.

---

## 2. Visión general de la solución

La solución sigue una arquitectura distribuida y simplificada:

```text
Datos FHVHV de NYC TLC
          ↓
 Google Cloud Storage
       Capa RAW
          ↓
 Google Dataproc + PySpark
          ↓
 Limpieza + Transformación
          ↓
 Google Cloud Storage
   Capa CURATED en Parquet
  particionada por año y mes
          ↓
 Agregaciones analíticas
          ↓
 ┌──────────────────┬──────────────────┐
 │                  │                  │
MariaDB        CSV analíticos
Capa SQL              │
                      ↓
                  Streamlit
                      ↓
             Dashboard ejecutivo
```

La arquitectura sigue el principio **KISS (Keep It Simple, Stupid)**: el conjunto masivo de datos se procesa mediante cómputo distribuido y el dashboard final consume resultados analíticos compactos, evitando procesar nuevamente cientos de millones de registros cada vez que un usuario consulta la aplicación.

---

## 3. Fuente y escala de los datos

**Fuente:** NYC Taxi & Limousine Commission (NYC TLC), High Volume For-Hire Vehicle Trip Records.

**Periodo:** enero de 2022 a diciembre de 2024.

**Archivos:** 36 archivos mensuales en formato Parquet.

| Métrica | Resultado |
|---|---:|
| Volumen RAW | 15.86 GiB |
| Registros originales | 684,376,551 |
| Registros limpios | 683,913,899 |
| Registros inválidos eliminados | 462,652 |
| Porcentaje eliminado | 0.0676% |
| Cobertura temporal | 36 meses |

Los datos originales se conservan separados de los datos transformados para mantener trazabilidad y reproducibilidad.

---

## 4. Pipeline de datos

### Ingesta

Los 36 archivos mensuales en formato Parquet fueron almacenados en una capa **RAW** dentro de Google Cloud Storage.

### Limpieza y transformación

Se utilizó PySpark sobre Google Dataproc para realizar de manera distribuida los procesos de validación, limpieza y transformación.

Los controles de calidad incluyeron:

- Distancias de viaje inválidas o no positivas.
- Duraciones inválidas o no positivas.
- Tarifas base negativas.
- Pagos negativos a conductores.
- Fechas inválidas.
- Análisis de valores nulos.
- Compatibilidad de esquemas entre archivos Parquet mensuales.

Además, se generaron variables analíticas como:

- `year`
- `month`
- `day_of_week`
- `pickup_hour`
- `trip_minutes`
- `avg_speed_mph`

### Optimización del almacenamiento

El conjunto de datos limpio fue almacenado nuevamente en formato Parquet dentro de la capa **CURATED**, particionado por:

```text
year/
└── month/
```

Se validaron correctamente las **36 particiones año-mes**.

También se comprobó el uso de **partition pruning** en Spark. Una consulta filtrada para diciembre de 2024 contabilizó **21,062,630 viajes en aproximadamente 0.69 segundos**, verificándose en el plan de ejecución la aplicación de filtros sobre las particiones.

---

## 5. Capa analítica

En lugar de enviar los cientos de millones de registros directamente a la herramienta de visualización, PySpark genera conjuntos de datos analíticos compactos.

Se construyeron indicadores de:

- Viajes anuales.
- Demanda mensual.
- Demanda y operación por hora.
- Demanda por día de la semana.
- Principales zonas de origen.
- Principales zonas de destino.
- Evolución mensual de tarifa base y pago a conductores.

Estos resultados funcionan como capa de consumo para SQL y para el dashboard ejecutivo.

---

## 6. Capa SQL con MariaDB

Se implementó MariaDB como capa relacional para demostrar el consumo estructurado de los resultados generados mediante Big Data.

Se crearon y validaron siete tablas analíticas:

| Tabla | Registros |
|---|---:|
| `annual_sql_summary` | 3 |
| `daily_summary` | 7 |
| `hourly_summary` | 24 |
| `monthly_economics` | 36 |
| `monthly_summary` | 36 |
| `top_dropoff_zones` | 264 |
| `top_pickup_zones` | 263 |

El repositorio incluye scripts SQL reproducibles para la creación del esquema y la carga de los datos.

---

## 7. Dashboard ejecutivo

Los resultados analíticos se presentan mediante una aplicación interactiva desarrollada con Streamlit.

El dashboard permite analizar:

- Indicadores ejecutivos principales.
- Evolución anual y mensual de la demanda.
- Demanda por hora.
- Demanda por día de la semana.
- Velocidad promedio por hora.
- Principales zonas de origen y destino.
- Evolución de tarifa base y pago a conductores.

### Aplicación desplegada

La aplicación se encuentra desplegada públicamente mediante Streamlit Community Cloud.

La versión final contará con dos vistas principales:

### 📋 Estrategia del proyecto

Presentará el problema de negocio, las cuatro preguntas del CDO, la arquitectura desarrollada y el impacto/ROI de la solución.

### 📊 Inteligencia de movilidad

Representará el producto como sería utilizado en un escenario real por responsables de operación y planeación para consultar indicadores y apoyar la toma de decisiones.

---

## 8. Hallazgos principales

El análisis realizado permite identificar inicialmente que:

- El volumen anual aumentó de aproximadamente **212.1 millones de viajes en 2022 a 239.4 millones en 2024**.
- La mayor concentración acumulada de demanda por hora se presenta alrededor de las **18:00 horas**.
- El **sábado** registra el mayor volumen acumulado de viajes entre los días de la semana.
- La velocidad promedio disminuye considerablemente durante periodos de alta demanda durante el día y la tarde.
- Los indicadores de tarifa base de pasajeros y pago a conductores presentan una tendencia creciente durante el periodo analizado.

Estos resultados serán utilizados para formular recomendaciones operativas y estratégicas.

---

## 9. Tecnologías utilizadas

| Capa | Tecnología |
|---|---|
| Fuente | NYC TLC |
| Almacenamiento en nube | Google Cloud Storage |
| Infraestructura distribuida | Google Dataproc |
| Procesamiento Big Data | Apache Spark / PySpark |
| Almacenamiento optimizado | Parquet particionado |
| Capa relacional | MariaDB / SQL |
| Visualización | Streamlit |
| Control de versiones | GitHub |

---

## 10. Estructura del repositorio

```text
nyc-mobility-big-data/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── annual_sql_summary.csv
│   ├── daily_summary.csv
│   ├── hourly_summary.csv
│   ├── monthly_economics.csv
│   ├── monthly_summary.csv
│   ├── top_dropoff_zones.csv
│   └── top_pickup_zones.csv
│
├── ipynb/
│   └── NYC_Mobility_Big_Data.ipynb
│
└── sql/
    ├── 01_schema_mariadb.sql
    └── 02_load_data.sql
```

Los archivos masivos de las capas RAW y CURATED no se almacenan en GitHub debido a su tamaño.

---

## 11. Las cuatro preguntas del CDO

### ¿Qué estamos construyendo?

Un producto escalable de inteligencia de movilidad que transforma cientos de millones de registros de viajes de vehículos de transporte de alto volumen de Nueva York en indicadores operativos y ejecutivos.

### ¿Para qué lo estamos haciendo?

Para reducir la complejidad asociada al análisis de grandes volúmenes de información histórica de movilidad y proporcionar información accesible sobre demanda, comportamiento operativo, concentración geográfica y tendencias económicas.

### ¿Cómo lo estamos resolviendo?

Mediante una arquitectura distribuida que utiliza Google Cloud Storage para almacenamiento, Dataproc y PySpark para ETL a gran escala, Parquet particionado para persistencia optimizada, MariaDB como capa relacional y Streamlit para visualización ejecutiva.

### ¿A quién beneficia y cuál es el ROI?

Los usuarios objetivo son responsables de operación y planeación de movilidad que necesitan acceder rápidamente a patrones históricos de demanda y desempeño operativo.

El ROI se cuantificará mediante escenarios operativos y supuestos explícitos y medibles, evitando atribuir a la solución ahorros financieros que no puedan demostrarse con los datos disponibles.

---

## 12. Estado del proyecto

- [x] Ingesta de más de 15 GB
- [x] Procesamiento distribuido con PySpark
- [x] Limpieza y transformación
- [x] Almacenamiento Parquet particionado
- [x] Validación de calidad e integridad
- [x] Agregaciones analíticas
- [x] Implementación de MariaDB / SQL
- [x] Despliegue inicial del dashboard en Streamlit
- [ ] Modelo estratégico de ROI
- [ ] Diagrama final de arquitectura
- [ ] Vista estratégica y vista operativa final en Streamlit
- [ ] Documento técnico-ejecutivo
- [ ] Executive Pitch
