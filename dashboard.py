# milestone3_dashboard_fixed.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🌍 Global Weather & Air Quality Dashboard",
                   layout="wide", page_icon="☁")

st.title("🌦 Global Weather & Air Quality Interactive Dashboard")
st.markdown("""
Explore weather and air quality patterns interactively.  
*Milestone 3 – Visualization Development & Interactivity*
            
<style>

/* MAIN PAGE BACKGROUND */
.block-container {
    padding-top: 2rem !important;  /* increased top padding to move heading down */
    padding-bottom: 2rem !important;
    background-color: #f4f7fb !important;
}

/* HEADER / MAIN TITLE */
h1 {
    color: #002147 !important;
    text-align: center !important;
    font-weight: 800 !important;
    font-size: 2.9rem !important;
    margin-top: 1.5rem !important;   
    margin-bottom: 1.5rem !important;
    background-color: #dce8ff !important;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
}

/* SUB HEADINGS */
h2, h3, h4 {
    color: #003366 !important;
    font-weight: 700 !important;
    margin-bottom: 0.6rem !important;
}

/* SIDEBAR DESIGN */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #eaf1fc 0%, #cfdff7 100%) !important;
    border-right: 2px solid #a3c4f3;
    box-shadow: 2px 0px 6px rgba(0,0,0,0.05);
}


[data-testid="stSidebar"] * {
    color: #B0B0B0 !important;  /* changed from blue to black */
    font-weight: 600 !important;
}

/* SIDEBAR INPUT BOXES */
div[data-baseweb="select"], .stDateInput, .stMultiSelect, .stTextInput {
    background-color: #FFFFFF !important;
    border-radius: 8px !important;
    border: 1.5px solid #003366 !important;
    color: #ffffff !important;  /* input text black */
}


/* FILTER HEADINGS  */    
[data-testid="stSidebar"] label, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3 {
    color: #F8F9FA !important;  /* changed from blue to black */
    font-weight: 700 !important;
    font-size: 1rem !important;
}

section[data-testid="stSidebar"] > div {
    margin-bottom: 0.8rem !important;
}

/* METRICS SECTION */
[data-testid="stMetric"] {
    background-color: white !important;
    border-radius: 12px;
    padding: 16px;
    margin: 6px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    text-align: center !important;
}
[data-testid="stMetricLabel"] {
    color: #002b5b !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
}
[data-testid="stMetricValue"] {
    color: #003366 !important;
    font-weight: 800 !important;
    font-size: 1.3rem !important;
}

/* PLOTLY CHARTS */
.js-plotly-plot {
    border-radius: 10px;
    background-color: white !important;
    padding: 10px !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)


# DATA LOAD

@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\Kashi\Desktop\climatescope-project\data\GlobalWeatherRepository_cleaned.csv")


    df['last_updated'] = pd.to_datetime(df['last_updated'], errors='coerce')
    df['Date'] = df['last_updated'].dt.date
    df['Hour'] = df['last_updated'].dt.hour


    df = df.dropna(subset=["latitude", "longitude"])
    return df

df = load_data()


# SIDEBAR FILTERS

st.sidebar.header("🔍 Filters")

# Date filter
min_date, max_date = df['Date'].min(), df['Date'].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

if len(date_range) == 2:
    df = df[(df['Date'] >= date_range[0]) & (df['Date'] <= date_range[1])]

# Temperature filter (range)
temp_min, temp_max = float(df["temperature_celsius"].min()), float(df["temperature_celsius"].max())
temp_range = st.sidebar.slider("Select Temperature Range (°C)", temp_min, temp_max, (temp_min, temp_max))
df = df[(df["temperature_celsius"] >= temp_range[0]) & (df["temperature_celsius"] <= temp_range[1])]

# Variable selector
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
default_var = "temperature_celsius" if "temperature_celsius" in numeric_cols else numeric_cols[0]
selected_variable = st.sidebar.selectbox("Select variable to visualize", numeric_cols, index=numeric_cols.index(default_var))

# SUMMARY METRICS

st.subheader("📊 Key Weather Statistics")

col1, col2, col3, col4 = st.columns(4)
col1.metric("🌡 Avg Temperature (°C)", f"{df['temperature_celsius'].mean():.2f}")
col2.metric("💧 Avg Humidity (%)", f"{df['humidity'].mean():.2f}")
col3.metric("🌬 Avg Wind Speed (kph)", f"{df['wind_kph'].mean():.2f}")
col4.metric("📈 Avg Pressure (mb)", f"{df['pressure_mb'].mean():.2f}")


# TABS SETUP

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌡 Temperature Trends", 
    "🌫 Air Quality Analysis", 
    "🌍 Geospatial Visualization", 
    "📊 Correlation Heatmap", 
    "🧭 Insights Summary"
])


# TAB 1 — TEMPERATURE & WEATHER TRENDS

with tab1:
    st.subheader("📈 Temperature and Weather Trends")
    fig_temp = px.line(df, x="last_updated", y=selected_variable,
                       title=f"{selected_variable.replace('_',' ').title()} Over Time",
                       markers=True, template="plotly_white")
    st.plotly_chart(fig_temp, use_container_width=True)

    # Comparison chart
    st.markdown("#### Compare Multiple Weather Variables")
    compare_vars = st.multiselect("Select variables to compare", numeric_cols, 
                                  default=["temperature_celsius", "humidity"])
    if compare_vars:
        fig_comp = px.line(df, x="last_updated", y=compare_vars, template="plotly_white")
        st.plotly_chart(fig_comp, use_container_width=True)


# TAB 2 — AIR QUALITY ANALYSIS

with tab2:
    st.subheader("💨 Air Quality Metrics")
    air_cols = [c for c in df.columns if "air_quality" in c.lower()]
    if air_cols:
        selected_aq = st.selectbox("Select Air Quality Parameter", air_cols)
        fig_aq = px.line(df, x="last_updated", y=selected_aq,
                         title=f"{selected_aq.replace('_',' ').title()} Over Time",
                         color_discrete_sequence=["#1f77b4"], template="plotly_white")
        st.plotly_chart(fig_aq, use_container_width=True)

        # Comparison
        st.markdown("#### Compare Multiple Air Quality Components")
        aq_compare = st.multiselect("Select components", air_cols, 
                                    default=["air_quality_PM2.5", "air_quality_PM10"] if "air_quality_PM2.5" in air_cols else air_cols[:2])
        if aq_compare:
            fig_compare = px.line(df, x="last_updated", y=aq_compare, template="plotly_white")
            st.plotly_chart(fig_compare, use_container_width=True)
    else:
        st.warning("No air quality columns found in dataset.")


# TAB 3 — GEOSPATIAL VISUALIZATION

with tab3:
    st.subheader("🗺 Global Temperature Distribution")
    if "latitude" in df.columns and "longitude" in df.columns:
        fig_map = px.scatter_geo(df,
                                 lat="latitude", lon="longitude",
                                 color="temperature_celsius",
                                 size="humidity",
                                 title="Global Temperature & Humidity Distribution",
                                 projection="natural earth",
                                 color_continuous_scale="RdYlBu_r",
                                 hover_data=["pressure_mb", "visibility_km"])
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("Latitude/Longitude columns not found in dataset.")


# TAB 4 — CORRELATION HEATMAP

with tab4:
    st.subheader("📊 Correlation Between Weather & Air Quality Variables")
    corr = df[numeric_cols].corr()
    fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r",
                         title="Correlation Heatmap", aspect="auto")
    st.plotly_chart(fig_corr, use_container_width=True)


# TAB 5 — INSIGHTS & CONCLUSION

with tab5:
    st.subheader("🧭 Key Insights and Findings")
    st.info("""
    *🌡 Temperature:*  
    - Daily fluctuations visible; lower humidity corresponds with temperature peaks.

    *💨 Air Quality:*  
    - PM2.5 and PM10 levels strongly correlated, reflecting particulate density.  
    - CO and NO₂ rise when visibility drops.

    *🌍 Geospatial Patterns:*  
    - Coastal areas show moderate temperatures and high humidity.  
    - Air quality varies widely across locations.

    *📈 Correlation:*  
    - Temperature inversely correlated with humidity.  
    - PM2.5 ↔ PM10 correlation > 0.9.  
    - Wind speed helps disperse pollutants.

    *✅ Conclusion:*  
    - Weather and air quality are interlinked; this dashboard shows their dynamic interaction in real time.
    """)

st.success("✅ Milestone 3 Dashboard Completed!")