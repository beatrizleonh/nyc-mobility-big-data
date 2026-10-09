# NYC Mobility Intelligence

Proyecto Final de la materia Grandes Datos.  
Maestría en Ciencia de Datos · Universidad Panamericana

**Alumnos:** Beatriz León Hernández y Juan Pablo Portillo Muralles  
Octubre 2026

NYC Mobility Intelligence es una arquitectura de Big Data diseñada para analizar
los viajes de vehículos de transporte de alto volumen (FHVHV) publicados por la
New York City Taxi & Limousine Commission (NYC TLC).

El proyecto procesa información de enero de 2022 a diciembre de 2024 para
responder una pregunta de negocio:

> ¿En qué zonas y horarios se concentra la demanda de viajes y dónde existen
> oportunidades para mejorar la asignación de vehículos?

Se procesaron **684,376,551 registros originales**, distribuidos en 36 archivos
Parquet con un tamaño total de **15.86 GiB (17.03 GB)**.
Después de la limpieza se conservaron **683,913,899 viajes válidos**.

## Arquitectura
El proyecto implementa un pipeline de extremo a extremo:

NYC TLC  
↓  
Google Cloud Storage - Raw  
↓  
Dataproc + PySpark  
↓  
Google Cloud Storage - Curated  
↓  
Capa analítica  
↓  
MariaDB + CSV  
↓  
GitHub + Streamlit

***Google Cloud Storage***
Bucket:
`nyc-mobility-bl-jp-2026`

Principales capas:
- `raw/high-volume-for-hire-vehicle/`: 36 archivos Parquet originales.
- `reference/`: archivos de referencia de zonas de la NYC TLC.
- `curated/fhvhv_trips/`: datos limpios y transformados.
- `analytics/`: conjuntos analíticos en Parquet.
- `analytics_csv/`: resultados analíticos exportados a CSV.

Los archivos de `raw` se conservaron sin modificaciones para mantener una copia
de la fuente original y permitir reproducir el procesamiento.

***Dataproc y PySpark***
El procesamiento distribuido se realizó en el clúster:

`nyc-clsuter-final`

Configuración utilizada:

- 1 nodo maestro.
- 2 nodos trabajadores.
- Máquinas `n1-standard-4`.
- Dataproc 2.3 sobre Debian 12.
- PySpark.
- Jupyter.
- Apagado automático después de una hora sin actividad.

Las transformaciones principales se realizaron mediante DataFrames de PySpark y
también se utilizó Spark SQL para generar y validar el resumen anual.

***Curated***
Después de la limpieza se obtuvieron: 683,913,899 viajes válidos

Los datos fueron almacenados nuevamente como Parquet y particionados por:
`year / month`
Esto permite que Spark consulte únicamente las particiones necesarias en lugar
de recorrer los tres años completos.

## Pipeline de datos

***1. Ingesta***

Se utilizaron 36 archivos mensuales de NYC TLC correspondientes al periodo:
enero 2022 - diciembre 2024

Los archivos fueron transferidos desde la fuente oficial hacia Cloud Storage.

***2. Homologación del esquema***

Se detectaron diferencias en los tipos de datos de `PULocationID` y
`DOLocationID` entre distintos meses.

Los archivos fueron leídos individualmente, las columnas se homologaron a
`long` y posteriormente se integraron mediante `unionByName`.

***3. Limpieza***
Se eliminaron registros con:

- `trip_miles <= 0`
- `trip_time <= 0`
- tarifa base negativa
- pago negativo al conductor
- llegada igual o anterior a la recogida

En total se eliminaron: 462,652 registros (0.068%)

Los valores nulos de campos opcionales se conservaron cuando no afectaban los
indicadores utilizados.

No se realizó desduplicación debido a que el dataset no contiene un
identificador único de viaje.

***4. Transformación***
Se generaron variables adicionales:
- `year`
- `month`
- `day_of_week`
- `pickup_hour`
- `trip_minutes`
- `avg_speed_mph`

***5. Capa analítica***
Se generaron siete conjuntos analíticos:

| Dataset | Descripción |
|---|---|
| `annual_sql_summary` | Indicadores anuales generados con Spark SQL |
| `monthly_summary` | Demanda y métricas por mes |
| `daily_summary` | Demanda por día de la semana |
| `hourly_summary` | Demanda, duración y velocidad por hora |
| `monthly_economics` | Indicadores económicos mensuales |
| `top_pickup_zones` | Indicadores por zona de origen |
| `top_dropoff_zones` | Indicadores por zona de destino |

Los resultados se almacenaron en Parquet para continuar trabajando dentro de
GCP y en CSV para la capa SQL y el dashboard.

***Capa SQL***
Se implementó una capa relacional utilizando **MariaDB 11.4** dentro de un
contenedor local de Docker.

Base de datos: `nyc_mobility`
La base contiene siete tablas correspondientes a los conjuntos analíticos.
Los scripts para reproducir esta capa se encuentran en:
-sql/01_schema_mariadb.sql
-sql/02_load_data.sql

***Rendimiento***
La capa `curated` fue particionada por año y mes.
Como prueba de rendimiento se consultó diciembre de 2024:
- Registros: **21,062,630**
- Tiempo de conteo: **0.69 segundos**

El plan de ejecución de Spark confirmó la aplicación de `PartitionFilters`
sobre `year = 2024` y `month = 12`.

Esto permite evitar la lectura de los otros 35 meses cuando una consulta requiere
únicamente un periodo específico.

***Principales resultados***
Entre los hallazgos obtenidos:

- Los viajes aumentaron de **212.1 millones en 2022** a **239.4 millones en 2024**.
- El crecimiento anual pasó de **9.5% en 2023** a **3.0% en 2024**.
- El **28% de los viajes** ocurre entre las 16:00 y las 20:59.
- El pico de demanda ocurre aproximadamente a las **18:00**.
- La velocidad promedio disminuye considerablemente durante las horas de mayor demanda.
- El sábado registra aproximadamente **37% más viajes que el lunes**.
- LaGuardia y JFK se encuentran entre las principales zonas de origen.
- La tarifa base promedio aumentó **41.8%** entre enero de 2022 y diciembre de 2024.


***Dashboard***
Los resultados se publicaron mediante una aplicación desarrollada con Streamlit.

El dashboard incluye dos vistas:
1. Estrategia del proyecto
- problema de negocio
- preguntas del CDO
- arquitectura
- escala del proyecto
- simulador de impacto económico potencial

2. Inteligencia de movilidad
- demanda anual y mensual
- demanda por día
- demanda y velocidad por hora
- zonas de origen y destino
- indicadores económicos
- hallazgos y recomendaciones

El dashboard consume los siete CSV analíticos almacenados en este repositorio,
por lo que no necesita procesar nuevamente los 684 millones de registros ni
mantener activo el clúster de Dataproc.

**Dashboard:**  
https://nyc-mobility-big-data-cpfpwpukkxthk22kkzkpet.streamlit.app/

---

***Estructura del repositorio***
```text
nyc-mobility-big-data/
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
├── sql/
│   ├── 01_schema_mariadb.sql
│   └── 02_load_data.sql
│
├── app.py
├── requirements.txt
└── README.md
