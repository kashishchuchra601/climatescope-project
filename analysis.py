
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Global Weather Dashboard", layout="wide")
st.title("Global Weather Analysis Dashboard")
st.markdown("### Milestone 2 — Core Analysis & Visualization Design")
st.caption("Analyze global weather patterns, correlations, and regional comparisons using the cleaned dataset.")


@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\Kashi\Desktop\climatescope-project\data\GlobalWeatherRepository_cleaned.csv")
    df['last_updated'] = pd.to_datetime(df['last_updated'], errors='coerce')

    df['Year'] = df['last_updated'].dt.year
    
    df['last_updated'] = df['last_updated'].astype(str)
    
    return df

df = load_data()

with st.expander(" Summary Statistics"):
    st.write(df.describe())


# SIDEBAR FILTERS
st.sidebar.header(" Filters")

# Year Filter
years = sorted(df['Year'].dropna().unique())
selected_year = st.sidebar.selectbox("Select Year", years)
df = df[df['Year'] == selected_year]

# Country/Region Filter
country_col = next((col for col in df.columns if "country" in col.lower() or "region" in col.lower()), None)
if country_col:
    countries = sorted(df[country_col].dropna().unique())
    countries.insert(0, "All")  
    selected_countries = st.sidebar.multiselect(
        " Select Countries / Regions",
        countries,
        default=["All"]
    )
    if "All" not in selected_countries:
        df = df[df[country_col].isin(selected_countries)]
# DISTRIBUTION ANALYSIS
st.header(" Distribution Analysis")
num_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
if len(num_cols) > 0:
    selected_num = st.selectbox("Select a numerical variable to visualize distribution:", num_cols)
    fig_dist = px.histogram(df, x=selected_num, nbins=30, color_discrete_sequence=["#3A86FF"],
                            title=f"Distribution of {selected_num}")
    st.plotly_chart(fig_dist, use_container_width=True)
else:
    st.warning("No numerical columns found for distribution analysis.")


# TEMPERATURE TRENDS

if any("temp" in c.lower() for c in df.columns):
    st.header(" Temperature Trends")
    temp_col = [c for c in df.columns if "temp" in c.lower()][0]
    fig_line = px.line(df, x='Year', y=temp_col, color=country_col if country_col else None,
                       title="Temperature Trend Over Time", markers=True)
    st.plotly_chart(fig_line, use_container_width=True)


# COMPARATIVE ANALYSIS

if country_col and any("temp" in c.lower() for c in df.columns):
    st.header(" Comparative Analysis by Region")
    temp_col = [c for c in df.columns if "temp" in c.lower()][0]
    df_avg = df.groupby(country_col)[temp_col].mean().reset_index()
    fig_bar = px.bar(df_avg, x=country_col, y=temp_col, title="Average Temperature by Country/Region",
                     color=temp_col, color_continuous_scale="viridis")
    st.plotly_chart(fig_bar, use_container_width=True)


# CORRELATION ANALYSIS

st.header(" Correlation Heatmap")
if len(num_cols) > 1:
    corr = df[num_cols].corr()
    fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r",
                         title="Correlation Between Numerical Variables")
    st.plotly_chart(fig_corr, use_container_width=True)
else:
    st.warning("Not enough numerical data to compute correlation matrix.")


# EXTREME EVENTS
st.header("Extreme Weather Events")
if any("temp" in c.lower() for c in df.columns):
    temp_col = [c for c in df.columns if "temp" in c.lower()][0]
    hottest = df.loc[df[temp_col].idxmax()]
    coldest = df.loc[df[temp_col].idxmin()]
    st.markdown(f" Hottest Record: {hottest[temp_col]:.2f} at {hottest[country_col] if country_col else 'Unknown'} in {hottest['Year']}")
    st.markdown(f" Coldest Record: {coldest[temp_col]:.2f} at {coldest[country_col] if country_col else 'Unknown'} in {coldest['Year']}")


# INSIGHTS SECTION

st.header(" Insights & Observations")
st.markdown("""
- Temperature Distribution: Observe whether temperature is normally distributed or skewed.
- Regional Comparison: Compare average temperatures across selected countries.
- Correlation: Identify strong relationships between weather metrics (e.g., humidity ↔ rainfall).
- Trend Analysis: Observe how temperature changes across years for different regions.
- Extreme Values: Detect outliers or unusual weather patterns.
""")

st.success(" Milestone 2 Dashboard successfully built using the cleaned dataset.")














