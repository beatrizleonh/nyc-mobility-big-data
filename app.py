import pandas as pd
import streamlit as st


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="NYC Mobility Intelligence",
    page_icon="🚕",
    layout="wide"
)


# ============================================================
# CARGA DE DATOS
# ============================================================

@st.cache_data
def cargar_datos():

    mensual = pd.read_csv("data/monthly_summary.csv")
    anual = pd.read_csv("data/annual_sql_summary.csv")
    horario = pd.read_csv("data/hourly_summary.csv")
    diario = pd.read_csv("data/daily_summary.csv")
    origen = pd.read_csv("data/top_pickup_zones.csv")
    destino = pd.read_csv("data/top_dropoff_zones.csv")
    economia = pd.read_csv("data/monthly_economics.csv")

    origen = origen.nlargest(15, "total_trips")
    destino = destino.nlargest(15, "total_trips")

    return mensual, anual, horario, diario, origen, destino, economia


mensual, anual, horario, diario, origen, destino, economia = cargar_datos()


# ============================================================
# PREPARACIÓN
# ============================================================

mensual["fecha"] = pd.to_datetime(
    dict(year=mensual["year"], month=mensual["month"], day=1)
)

economia["fecha"] = pd.to_datetime(
    dict(year=economia["year"], month=economia["month"], day=1)
)


# ============================================================
# ESTILO
# ============================================================

st.markdown(
    """
    <style>
        .bloque-arquitectura {
            background-color: #f7f9fc;
            border: 1px solid #dfe5ec;
            border-radius: 12px;
            padding: 16px;
            margin: 8px 0;
            text-align: center;
        }

        .flecha {
            text-align: center;
            font-size: 25px;
            margin: 0;
        }

        .pregunta-cdo {
            background-color: #f7f9fc;
            border-left: 5px solid #4c78a8;
            border-radius: 8px;
            padding: 18px;
            margin-bottom: 15px;
        }

        .nota {
            background-color: #f7f9fc;
            border-radius: 10px;
            padding: 15px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ENCABEZADO
# ============================================================

st.title("🚕 NYC Mobility Intelligence")

st.caption(
    "Plataforma de inteligencia de movilidad basada en "
    "683.9 millones de viajes FHVHV de Nueva York | 2022–2024"
)


# ============================================================
# NAVEGACIÓN
# ============================================================

vista = st.radio(
    "Selecciona una vista:",
    ["📋 Estrategia del proyecto", "📊 Inteligencia de movilidad"],
    horizontal=True
)


# ============================================================
# VISTA 1 — ESTRATEGIA
# ============================================================

if vista == "📋 Estrategia del proyecto":

    st.header("Estrategia del proyecto")

    st.markdown(
        """
        **NYC Mobility Intelligence** transforma datos masivos de movilidad
        en información ejecutiva para apoyar la planeación y operación de
        plataformas de transporte de alto volumen.
        """
    )

    # --------------------------------------------------------
    # Problema de negocio
    # --------------------------------------------------------

    st.subheader("Problema de negocio")

    st.write(
        """
        Los sistemas de movilidad generan cientos de millones de registros
        individuales de viajes. Analizar este volumen mediante hojas de
        cálculo, bases de datos locales o scripts simples dificulta obtener
        información de manera eficiente para la toma de decisiones.

        La solución convierte este histórico masivo en indicadores accesibles
        que permiten identificar cuándo y dónde se concentra la demanda,
        reconocer periodos de mayor presión operativa y monitorear tendencias
        relevantes para la planeación.
        """
    )

    # --------------------------------------------------------
    # 4 preguntas del CDO
    # --------------------------------------------------------

    st.subheader("Las 4 preguntas del CDO")

    st.markdown(
        """
        <div class="pregunta-cdo">
        <b>1. ¿Qué estamos construyendo?</b><br><br>
        Un producto de datos escalable que transforma más de 683 millones
        de viajes FHVHV de Nueva York en indicadores ejecutivos de demanda,
        operación, concentración geográfica y comportamiento económico.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="pregunta-cdo">
        <b>2. ¿Para qué lo estamos haciendo?</b><br><br>
        Para convertir grandes volúmenes de información histórica de movilidad
        en información útil para la toma de decisiones, permitiendo identificar
        cuándo y dónde se concentra la demanda y reconocer periodos de mayor
        presión operativa.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="pregunta-cdo">
        <b>3. ¿Cómo lo estamos resolviendo?</b><br><br>
        Mediante una arquitectura distribuida que utiliza Google Cloud Storage,
        Dataproc y PySpark para el procesamiento masivo, Parquet particionado
        para almacenamiento optimizado, MariaDB como capa relacional y
        Streamlit como producto de visualización ejecutiva.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="pregunta-cdo">
        <b>4. ¿A quién beneficia y cuál es el ROI?</b><br><br>
        La solución está dirigida a equipos directivos de planeación y
        operaciones de plataformas de movilidad de alto volumen. Su impacto
        económico puede evaluarse mediante escenarios de ahorro de tiempo y
        costos analíticos, evitando atribuir beneficios financieros que no
        puedan demostrarse con los datos disponibles.
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # Arquitectura
    # --------------------------------------------------------

    st.subheader("Arquitectura de la solución")

    st.markdown(
        """
        <div class="bloque-arquitectura">
        <b>1. FUENTE · NYC TLC</b><br>
        FHVHV 2022–2024 · 36 archivos Parquet<br>
        684,376,551 registros
        </div>

        <div class="flecha">↓</div>

        <div class="bloque-arquitectura">
        <b>2. GOOGLE CLOUD STORAGE · RAW</b><br>
        15.86 GiB de datos originales
        </div>

        <div class="flecha">↓</div>

        <div class="bloque-arquitectura">
        <b>3. GOOGLE DATAPROC + PYSPARK</b><br>
        Limpieza · Validación · Transformación<br>
        684.4 M → 683.9 M registros
        </div>

        <div class="flecha">↓</div>

        <div class="bloque-arquitectura">
        <b>4. GOOGLE CLOUD STORAGE · CURATED</b><br>
        Parquet particionado por año y mes<br>
        36 particiones temporales
        </div>

        <div class="flecha">↓</div>

        <div class="bloque-arquitectura">
        <b>5. CAPA ANALÍTICA</b><br>
        Agregaciones PySpark · 7 conjuntos analíticos
        </div>
        """,
        unsafe_allow_html=True
    )

    col_sql, col_web = st.columns(2)

    with col_sql:
        st.markdown(
            """
            <div class="bloque-arquitectura">
            <b>🗄️ MariaDB / SQL</b><br>
            7 tablas analíticas<br>
            Capa relacional
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_web:
        st.markdown(
            """
            <div class="bloque-arquitectura">
            <b>📊 CSV analíticos → Streamlit</b><br>
            Dashboard ejecutivo<br>
            Consumo web
            </div>
            """,
            unsafe_allow_html=True
        )

    st.info(
        "Principio KISS: el procesamiento intensivo ocurre una sola vez "
        "sobre infraestructura distribuida. El dashboard consume resultados "
        "analíticos compactos en lugar de recorrer cientos de millones de "
        "registros en cada consulta."
    )

    # --------------------------------------------------------
    # Escala
    # --------------------------------------------------------

    st.subheader("Escala procesada")

    e1, e2, e3, e4 = st.columns(4)

    e1.metric("Datos RAW", "15.86 GiB")
    e2.metric("Registros originales", "684.4 M")
    e3.metric("Registros limpios", "683.9 M")
    e4.metric("Cobertura", "36 meses")

    # --------------------------------------------------------
    # ROI
    # --------------------------------------------------------

    st.subheader("Simulador de impacto económico")

    st.write(
        """
        Debido a que los datos públicos de NYC TLC no contienen los costos
        internos de una empresa, el ROI se calcula mediante un escenario
        configurable. Los valores siguientes son supuestos y pueden ser
        modificados por el usuario.
        """
    )

    r1, r2, r3 = st.columns(3)

    with r1:
        horas_actuales = st.number_input(
            "Horas mensuales dedicadas actualmente al análisis",
            min_value=0.0,
            value=80.0,
            step=5.0
        )

    with r2:
        costo_hora = st.number_input(
            "Costo promedio por hora del equipo (USD)",
            min_value=0.0,
            value=40.0,
            step=5.0
        )

    with r3:
        reduccion = st.slider(
            "Reducción estimada del tiempo de análisis",
            min_value=0,
            max_value=100,
            value=50,
            step=5
        )

    costo_actual_mensual = horas_actuales * costo_hora

    ahorro_horas = horas_actuales * (reduccion / 100)
    ahorro_mensual = ahorro_horas * costo_hora
    ahorro_anual = ahorro_mensual * 12

    roi1, roi2, roi3 = st.columns(3)

    roi1.metric(
        "Horas liberadas al mes",
        f"{ahorro_horas:,.1f}"
    )

    roi2.metric(
        "Ahorro potencial mensual",
        f"${ahorro_mensual:,.0f} USD"
    )

    roi3.metric(
        "Ahorro potencial anual",
        f"${ahorro_anual:,.0f} USD"
    )

    st.caption(
        "Este cálculo representa un escenario potencial basado en los "
        "supuestos introducidos por el usuario; no constituye un ahorro "
        "financiero observado."
    )


# ============================================================
# VISTA 2 — PRODUCTO DE USO REAL
# ============================================================

else:

    st.header("Inteligencia de movilidad")

    st.write(
        """
        Panel ejecutivo para monitorear patrones históricos de demanda,
        operación, concentración geográfica e indicadores económicos de
        viajes FHVHV en Nueva York.
        """
    )

    # --------------------------------------------------------
    # KPIs
    # --------------------------------------------------------

    total_viajes = int(anual["annual_trips"].sum())

    viajes_2024 = int(
        anual.loc[
            anual["year"] == anual["year"].max(),
            "annual_trips"
        ].iloc[0]
    )

    hora_pico = int(
        horario.loc[
            horario["total_trips"].idxmax(),
            "pickup_hour"
        ]
    )

    dia_pico = diario.loc[
        diario["total_trips"].idxmax(),
        "day_name"
    ]

    traduccion_dias = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }

    dia_pico = traduccion_dias.get(dia_pico, dia_pico)

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "Viajes analizados",
        f"{total_viajes / 1_000_000:.1f} M"
    )

    k2.metric(
        "Viajes en 2024",
        f"{viajes_2024 / 1_000_000:.1f} M"
    )

    k3.metric(
        "Hora de mayor demanda",
        f"{hora_pico}:00"
    )

    k4.metric(
        "Día de mayor demanda",
        dia_pico
    )

    # --------------------------------------------------------
    # Demanda
    # --------------------------------------------------------

    st.subheader("Evolución de la demanda")

    st.markdown("**Viajes por año**")

    grafica_anual = anual.set_index("year")[["annual_trips"]]
    st.bar_chart(grafica_anual)

    st.markdown("**Evolución mensual de viajes**")

    grafica_mensual = mensual.set_index("fecha")[["total_trips"]]
    st.line_chart(grafica_mensual)

    # --------------------------------------------------------
    # Operación
    # --------------------------------------------------------

    st.subheader("Demanda y operación")

    izquierda, derecha = st.columns(2)

    with izquierda:
        st.markdown("**Viajes por hora**")

        grafica_hora = horario.set_index(
            "pickup_hour"
        )[["total_trips"]]

        st.bar_chart(grafica_hora)

    with derecha:
        st.markdown("**Viajes por día de la semana**")

        diario_grafica = diario.copy()

        diario_grafica["dia"] = diario_grafica[
            "day_name"
        ].replace(traduccion_dias)

        grafica_dia = diario_grafica.set_index(
            "dia"
        )[["total_trips"]]

        st.bar_chart(grafica_dia)

    st.markdown("**Velocidad promedio por hora**")

    grafica_velocidad = horario.set_index(
        "pickup_hour"
    )[["avg_speed_mph"]]

    st.line_chart(grafica_velocidad)

    st.info(
        "La mayor demanda acumulada por hora se presenta alrededor de "
        "las 18:00. Estos periodos también coinciden con velocidades "
        "promedio relativamente bajas, información relevante para la "
        "planeación de capacidad operativa."
    )

    # --------------------------------------------------------
    # Geografía
    # --------------------------------------------------------

    st.subheader("Concentración geográfica")

    izquierda, derecha = st.columns(2)

    with izquierda:
        st.markdown("**15 principales zonas de origen**")

        grafica_origen = origen.set_index(
            "PULocationID"
        )[["total_trips"]]

        st.bar_chart(grafica_origen)

    with derecha:
        st.markdown("**15 principales zonas de destino**")

        grafica_destino = destino.set_index(
            "DOLocationID"
        )[["total_trips"]]

        st.bar_chart(grafica_destino)

    st.caption(
        "Las zonas se presentan mediante los LocationID oficiales de NYC TLC."
    )

    # --------------------------------------------------------
    # Economía
    # --------------------------------------------------------

    st.subheader("Indicadores económicos")

    st.markdown(
        "**Evolución de tarifa base promedio y pago promedio al conductor**"
    )

    grafica_economia = economia.set_index(
        "fecha"
    )[["avg_base_fare", "avg_driver_pay"]]

    st.line_chart(grafica_economia)

    eco1, eco2 = st.columns(2)

    eco1.metric(
        "Tarifa base promedio · dic. 2024",
        f"${float(economia.iloc[-1]['avg_base_fare']):,.2f}"
    )

    eco2.metric(
        "Pago promedio al conductor · dic. 2024",
        f"${float(economia.iloc[-1]['avg_driver_pay']):,.2f}"
    )

    st.caption(
        "La tarifa base corresponde al indicador base_passenger_fare "
        "del conjunto de datos y no debe interpretarse como ingreso neto "
        "de la plataforma."
    )

    # --------------------------------------------------------
    # Hallazgos para decisión
    # --------------------------------------------------------

    st.subheader("Hallazgos para la toma de decisiones")

    st.markdown(
        """
        - **Crecimiento de la demanda:** los viajes aumentaron de
          aproximadamente **212.1 millones en 2022 a 239.4 millones en 2024**.

        - **Concentración temporal:** las **18:00 horas** presentan el mayor
          volumen acumulado de viajes por hora.

        - **Demanda semanal:** el **sábado** concentra el mayor volumen
          acumulado de viajes.

        - **Presión operativa:** las menores velocidades promedio aparecen
          durante periodos de alta actividad diurna y vespertina.

        - **Concentración geográfica:** un conjunto reducido de LocationID
          concentra volúmenes particularmente elevados de origen y destino.
        """
    )

    # --------------------------------------------------------
    # Recomendaciones
    # --------------------------------------------------------

    st.subheader("Recomendaciones operativas")

    st.markdown(
        """
        **1. Planeación temporal de capacidad**  
        Considerar una mayor disponibilidad operativa durante las ventanas
        de demanda más elevada, particularmente alrededor del periodo
        vespertino.

        **2. Planeación semanal**  
        Incorporar el mayor volumen observado durante viernes y sábado en
        la programación de capacidad y seguimiento operativo.

        **3. Priorización geográfica**  
        Utilizar las zonas con mayor concentración histórica de viajes como
        puntos iniciales para análisis más detallados de asignación de
        capacidad.

        **4. Seguimiento de eficiencia operativa**  
        Monitorear conjuntamente demanda, duración y velocidad para detectar
        periodos en los que un alto volumen de viajes coincide con menor
        velocidad promedio.
        """
    )

    st.warning(
        "Las recomendaciones representan apoyo analítico para la planeación. "
        "El conjunto de datos no contiene información sobre disponibilidad "
        "de conductores, costos internos, tráfico en tiempo real ni capacidad "
        "de flota, por lo que no constituye un sistema automático de "
        "optimización."
    )
