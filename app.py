import os

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine


# ------------------------------------------------------------
# Configuración de la página
# ------------------------------------------------------------

st.set_page_config(
    page_title="NYC Mobility Intelligence",
    page_icon="🚕",
    layout="wide"
)


# ------------------------------------------------------------
# Conexión a MariaDB
# ------------------------------------------------------------

@st.cache_resource
def get_engine():
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "3307")
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME", "nyc_mobility")

    if not password:
        st.error("DB_PASSWORD no está configurada.")
        st.stop()

    return create_engine(
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    )


@st.cache_data
def load_data():
    engine = get_engine()

    monthly = pd.read_sql(
        "SELECT * FROM monthly_summary ORDER BY year, month",
        engine
    )

    annual = pd.read_sql(
        "SELECT * FROM annual_sql_summary ORDER BY year",
        engine
    )

    hourly = pd.read_sql(
        "SELECT * FROM hourly_summary ORDER BY pickup_hour",
        engine
    )

    daily = pd.read_sql(
        "SELECT * FROM daily_summary ORDER BY day_of_week",
        engine
    )

    pickup = pd.read_sql(
        """
        SELECT *
        FROM top_pickup_zones
        ORDER BY total_trips DESC
        LIMIT 15
        """,
        engine
    )

    dropoff = pd.read_sql(
        """
        SELECT *
        FROM top_dropoff_zones
        ORDER BY total_trips DESC
        LIMIT 15
        """,
        engine
    )

    economics = pd.read_sql(
        "SELECT * FROM monthly_economics ORDER BY year, month",
        engine
    )

    return monthly, annual, hourly, daily, pickup, dropoff, economics


monthly, annual, hourly, daily, pickup, dropoff, economics = load_data()


# ------------------------------------------------------------
# Preparación de variables
# ------------------------------------------------------------

monthly["date"] = pd.to_datetime(
    dict(year=monthly["year"], month=monthly["month"], day=1)
)

economics["date"] = pd.to_datetime(
    dict(year=economics["year"], month=economics["month"], day=1)
)


# ------------------------------------------------------------
# Encabezado
# ------------------------------------------------------------

st.title("🚕 NYC Mobility Intelligence")

st.caption(
    "Executive analytics of High Volume For-Hire Vehicle trips "
    "in New York City | 2022–2024"
)


# ------------------------------------------------------------
# 1. Resumen ejecutivo
# ------------------------------------------------------------

st.header("Executive Overview")

total_trips = int(annual["annual_trips"].sum())
latest_year_trips = int(
    annual.loc[annual["year"] == annual["year"].max(), "annual_trips"].iloc[0]
)

peak_hour = int(
    hourly.loc[hourly["total_trips"].idxmax(), "pickup_hour"]
)

peak_day = daily.loc[
    daily["total_trips"].idxmax(), "day_name"
]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Trips analyzed",
    f"{total_trips / 1_000_000:.1f} M"
)

col2.metric(
    "Trips in 2024",
    f"{latest_year_trips / 1_000_000:.1f} M"
)

col3.metric(
    "Peak demand hour",
    f"{peak_hour}:00"
)

col4.metric(
    "Highest-demand day",
    peak_day
)

st.subheader("Annual trip volume")

annual_chart = annual.set_index("year")[["annual_trips"]]
st.bar_chart(annual_chart)

st.subheader("Monthly demand evolution")

monthly_chart = monthly.set_index("date")[["total_trips"]]
st.line_chart(monthly_chart)


# ------------------------------------------------------------
# 2. Demanda y operación
# ------------------------------------------------------------

st.header("Demand & Operations")

left, right = st.columns(2)

with left:
    st.subheader("Trips by hour")
    hourly_chart = hourly.set_index("pickup_hour")[["total_trips"]]
    st.bar_chart(hourly_chart)

with right:
    st.subheader("Trips by day of week")
    daily_chart = daily.set_index("day_name")[["total_trips"]]
    st.bar_chart(daily_chart)

st.subheader("Average speed by hour")

speed_chart = hourly.set_index("pickup_hour")[["avg_speed_mph"]]
st.line_chart(speed_chart)


# ------------------------------------------------------------
# 3. Geografía
# ------------------------------------------------------------

st.header("Geographic Demand")

left, right = st.columns(2)

with left:
    st.subheader("Top 15 pickup zones")

    pickup_chart = (
        pickup
        .set_index("PULocationID")[["total_trips"]]
    )

    st.bar_chart(pickup_chart)

with right:
    st.subheader("Top 15 dropoff zones")

    dropoff_chart = (
        dropoff
        .set_index("DOLocationID")[["total_trips"]]
    )

    st.bar_chart(dropoff_chart)

st.caption(
    "Zones are represented using NYC TLC Location IDs."
)


# ------------------------------------------------------------
# 4. Economía
# ------------------------------------------------------------

st.header("Trip Economics")

st.subheader("Average passenger base fare and driver pay")

economic_avg = economics.set_index("date")[
    ["avg_base_fare", "avg_driver_pay"]
]

st.line_chart(economic_avg)

left, right = st.columns(2)

with left:
    st.metric(
        "Average base fare — Dec 2024",
        f"${float(economics.iloc[-1]['avg_base_fare']):,.2f}"
    )

with right:
    st.metric(
        "Average driver pay — Dec 2024",
        f"${float(economics.iloc[-1]['avg_driver_pay']):,.2f}"
    )


# ------------------------------------------------------------
# Metodología
# ------------------------------------------------------------

with st.expander("Data architecture & methodology"):
    st.markdown(
        """
        **Pipeline**

        NYC TLC FHVHV Parquet data  
        → Google Cloud Storage (RAW)  
        → Google Dataproc + PySpark  
        → Cleaning and transformation  
        → Partitioned CURATED Parquet  
        → Analytical aggregations  
        → MariaDB  
        → Streamlit executive dashboard

        **Processing scale**

        - RAW data: 15.86 GiB
        - Original records: 684,376,551
        - Clean records: 683,913,899
        - Period: January 2022 – December 2024
        """
    )
