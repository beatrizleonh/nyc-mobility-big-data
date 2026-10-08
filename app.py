import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

    # Catálogo oficial de zonas de NYC TLC (keep_default_na=False evita
    # que los valores "N/A" del catálogo se conviertan en nulos)
    zonas = pd.read_csv(
        "data/taxi_zone_lookup.csv",
        keep_default_na=False
    )
    zonas["zona"] = zonas["Zone"] + " (" + zonas["Borough"] + ")"
    zonas.loc[zonas["LocationID"] == 265, "zona"] = "Fuera de NYC"
    zonas.loc[zonas["LocationID"] == 264, "zona"] = "Desconocida"

    total_viajes_zonas = origen["total_trips"].sum()

    origen = origen.merge(
        zonas[["LocationID", "zona"]],
        left_on="PULocationID",
        right_on="LocationID",
        how="left"
    )
    destino = destino.merge(
        zonas[["LocationID", "zona"]],
        left_on="DOLocationID",
        right_on="LocationID",
        how="left"
    )

    participacion_top10 = (
        origen.nlargest(10, "total_trips")["total_trips"].sum()
        / total_viajes_zonas
    )

    origen = origen.nlargest(15, "total_trips")
    destino = destino.nlargest(15, "total_trips")

    return (
        mensual, anual, horario, diario, origen, destino, economia,
        participacion_top10
    )


(
    mensual, anual, horario, diario, origen, destino, economia,
    participacion_top10
) = cargar_datos()


# ============================================================
# PREPARACIÓN
# ============================================================

mensual["fecha"] = pd.to_datetime(
    dict(year=mensual["year"], month=mensual["month"], day=1)
)

economia["fecha"] = pd.to_datetime(
    dict(year=economia["year"], month=economia["month"], day=1)
)

economia["participacion_conductor"] = (
    economia["total_driver_pay"] / economia["total_base_fare"] * 100
)

# Indicadores de 2024 usados en el escenario de impacto
anio_reciente = int(anual["year"].max())

viajes_anio_reciente = int(
    mensual.loc[mensual["year"] == anio_reciente, "total_trips"].sum()
)

tarifa_total_anio_reciente = float(
    economia.loc[economia["year"] == anio_reciente, "total_base_fare"].sum()
)

tarifa_promedio_anio_reciente = (
    tarifa_total_anio_reciente / viajes_anio_reciente
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
        se evalúa mediante un escenario: si una mejor planeación de la oferta
        permitiera atender 0.1% más viajes, el valor bruto potencial en
        tarifa base sería de alrededor de 6.3 millones de dólares al año,
        frente a un costo de procesamiento del orden de 8 dólares. Este valor
        no representa utilidad neta.
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
        f"""
        Debido a que los datos públicos de NYC TLC no contienen los costos
        internos de una empresa, el impacto se calcula mediante un escenario:
        qué pasaría si una mejor planeación de la oferta permitiera atender un
        porcentaje adicional de viajes. El cálculo usa los
        {viajes_anio_reciente:,} viajes de {anio_reciente} y su tarifa base
        promedio de ${tarifa_promedio_anio_reciente:,.2f} USD.
        """
    )

    mejora = st.slider(
        "Viajes adicionales atendidos por una mejor planeación (%)",
        min_value=0.05,
        max_value=1.0,
        value=0.1,
        step=0.05
    )

    viajes_adicionales = viajes_anio_reciente * (mejora / 100)
    valor_bruto = viajes_adicionales * tarifa_promedio_anio_reciente

    roi1, roi2, roi3 = st.columns(3)

    roi1.metric(
        "Viajes adicionales al año",
        f"{viajes_adicionales:,.0f}"
    )

    roi2.metric(
        "Valor bruto potencial anual",
        f"${valor_bruto / 1_000_000:,.1f} M USD"
    )

    roi3.metric(
        "Costo estimado del procesamiento",
        "~8 USD"
    )

    st.caption(
        "El valor bruto potencial corresponde a tarifa base de pasajeros y "
        "no representa utilidad neta, ya que no descuenta pago al conductor, "
        "operación, seguros, impuestos, incentivos ni comisiones. El costo "
        "del procesamiento es una estimación: 0.86 USD por hora según la "
        "consola de GCP, por cerca de 9.5 horas de clúster encendido."
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

    st.markdown("**Viajes y velocidad promedio por hora**")

    fig_hora = make_subplots(specs=[[{"secondary_y": True}]])

    fig_hora.add_trace(
        go.Bar(
            x=horario["pickup_hour"],
            y=horario["total_trips"],
            name="Viajes",
            marker_color="#4c78a8"
        ),
        secondary_y=False
    )

    fig_hora.add_trace(
        go.Scatter(
            x=horario["pickup_hour"],
            y=horario["avg_speed_mph"],
            name="Velocidad promedio (mph)",
            mode="lines+markers",
            line=dict(color="#e45756", width=3)
        ),
        secondary_y=True
    )

    fig_hora.update_xaxes(
        title_text="Hora de recogida", dtick=1, range=[-0.5, 23.5]
    )
    fig_hora.update_yaxes(title_text="Viajes", secondary_y=False)
    fig_hora.update_yaxes(title_text="Velocidad (mph)", secondary_y=True)
    fig_hora.update_layout(
        height=420,
        legend=dict(orientation="h", y=1.12),
        margin=dict(t=40, b=40)
    )

    st.plotly_chart(fig_hora, use_container_width=True)

    viajes_tarde = horario.loc[
        horario["pickup_hour"].between(16, 20), "total_trips"
    ].sum()

    participacion_tarde = viajes_tarde / horario["total_trips"].sum() * 100

    velocidad_max = horario["avg_speed_mph"].max()
    velocidad_min = horario["avg_speed_mph"].min()
    caida_velocidad = (1 - velocidad_min / velocidad_max) * 100

    st.info(
        f"De 16:00 a 20:59 se concentra el {participacion_tarde:.1f}% de "
        f"todos los viajes, con el pico a las {hora_pico}:00. En esas mismas "
        f"horas la velocidad promedio es la más baja del día: cae "
        f"{caida_velocidad:.1f}% respecto a la hora más rápida, por lo que "
        "cada vehículo completa menos viajes justo cuando más se necesitan."
    )

    st.markdown("**Viajes por día de la semana**")

    diario_grafica = diario.sort_values("day_of_week").copy()

    # Orden de lunes a domingo (en los datos 1 = domingo)
    diario_grafica["orden"] = (diario_grafica["day_of_week"] + 5) % 7

    diario_grafica = diario_grafica.sort_values("orden")

    diario_grafica["dia"] = diario_grafica[
        "day_name"
    ].replace(traduccion_dias)

    fig_dia = px.bar(
        diario_grafica,
        x="dia",
        y="total_trips",
        labels={"dia": "Día", "total_trips": "Viajes"},
        color_discrete_sequence=["#4c78a8"]
    )

    fig_dia.update_layout(height=360, margin=dict(t=20, b=40))

    st.plotly_chart(fig_dia, use_container_width=True)

    # --------------------------------------------------------
    # Geografía
    # --------------------------------------------------------

    st.subheader("Concentración geográfica")

    izquierda, derecha = st.columns(2)

    with izquierda:
        st.markdown("**15 principales zonas de origen**")

        fig_origen = px.bar(
            origen.sort_values("total_trips"),
            x="total_trips",
            y="zona",
            orientation="h",
            labels={"total_trips": "Viajes", "zona": ""},
            color_discrete_sequence=["#4c78a8"]
        )

        fig_origen.update_layout(height=520, margin=dict(t=20, b=40))

        st.plotly_chart(fig_origen, use_container_width=True)

    with derecha:
        st.markdown("**15 principales zonas de destino**")

        fig_destino = px.bar(
            destino.sort_values("total_trips"),
            x="total_trips",
            y="zona",
            orientation="h",
            labels={"total_trips": "Viajes", "zona": ""},
            color_discrete_sequence=["#4c78a8"]
        )

        fig_destino.update_layout(height=520, margin=dict(t=20, b=40))

        st.plotly_chart(fig_destino, use_container_width=True)

    st.info(
        f"La demanda está repartida en toda la ciudad: las 10 zonas con más "
        f"viajes de origen suman solo el {participacion_top10 * 100:.1f}% del "
        "total. Los aeropuertos de LaGuardia y JFK son los principales "
        "orígenes y tienen los viajes más largos, mientras que el principal "
        "destino es fuera de la ciudad, donde casi no se registran viajes "
        "de origen."
    )

    st.caption(
        "Nombres de zona tomados del catálogo oficial de NYC TLC "
        "(taxi_zone_lookup.csv)."
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
    )[["avg_base_fare", "avg_driver_pay"]].rename(
        columns={
            "avg_base_fare": "Tarifa base promedio (USD)",
            "avg_driver_pay": "Pago promedio al conductor (USD)"
        }
    )

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

    st.markdown("**Proporción de la tarifa base que se paga al conductor (%)**")

    fig_part = px.line(
        economia,
        x="fecha",
        y="participacion_conductor",
        labels={"fecha": "", "participacion_conductor": "% de la tarifa base"},
        color_discrete_sequence=["#4c78a8"]
    )

    fig_part.update_yaxes(range=[70, 85])
    fig_part.update_layout(height=320, margin=dict(t=20, b=40))

    st.plotly_chart(fig_part, use_container_width=True)

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
          aproximadamente **212.1 millones en 2022 a 239.4 millones en 2024**
          (+9.5% en 2023 y +3.0% en 2024), es decir, el crecimiento se está
          desacelerando.

        - **Concentración temporal:** de **16:00 a 20:59** ocurre el
          **28.0%** de los viajes y el pico es a las **18:00 horas**.

        - **Presión operativa:** en esas mismas horas la velocidad promedio
          cae a cerca de **11 mph**, contra **20.8 mph** a las 4:00.

        - **Demanda semanal:** el **sábado** tiene **37.1% más viajes** que
          el lunes, y viernes y sábado suman el **32.6%** del total.

        - **Concentración geográfica:** la demanda está repartida (las 10
          zonas principales suman el **13.5%**), con **LaGuardia** y **JFK**
          como principales orígenes. **28.2 millones** de viajes terminan
          fuera de la ciudad y **4.7 millones** en Newark.

        - **Economía:** la tarifa base promedio subió **41.8%** y el pago
          promedio al conductor **37.7%** entre enero de 2022 y diciembre de
          2024.
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

        **5. Aeropuertos**  
        Mantener presencia constante en LaGuardia y JFK, los principales
        orígenes de viajes y los de mayor duración.

        **6. Viajes fuera de la ciudad**  
        Evaluar incentivos para el regreso de los viajes que terminan fuera
        de NYC o en Newark, donde casi no se registran viajes de origen.
        """
    )

    st.warning(
        "Las recomendaciones representan apoyo analítico para la planeación. "
        "El conjunto de datos no contiene información sobre disponibilidad "
        "de conductores, costos internos, tráfico en tiempo real ni capacidad "
        "de flota, por lo que no constituye un sistema automático de "
        "optimización."
    )
