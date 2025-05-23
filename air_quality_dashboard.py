import streamlit as st
import pandas as pd
import zipfile
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

# Unzip and read the file
zip_path = "archive (2).zip"
data_file = None

with zipfile.ZipFile(zip_path, 'r') as z:
    # List files in the zip
    file_list = z.namelist()
    st.sidebar.write("Files in ZIP:", file_list)
    
    # Assume first CSV or Excel file
    for name in file_list:
        if name.endswith('.csv') or name.endswith('.xlsx'):
            data_file = name
            z.extract(name)
            break

# Check if we found a data file
if not data_file:
    st.error("No CSV or Excel file found in the ZIP archive.")
else:
    # Load dataset
    if data_file.endswith('.csv'):
        df = pd.read_csv(data_file)
    else:
        df = pd.read_excel(data_file)

    st.title("📊 Air Quality Dashboard")

    # Show raw data
    if st.checkbox("Show Raw Data"):
        st.write(df.head())

    # Basic info
    st.sidebar.header("Filters")

    # Assume columns like 'City', 'Date', 'PM2.5', 'PM10', etc.
    if 'City' in df.columns:
        cities = df['City'].dropna().unique()
        selected_cities = st.sidebar.multiselect("Select City", cities, default=cities[:1])
        df = df[df['City'].isin(selected_cities)]

    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])
        df = df.sort_values('Date')
        date_range = st.sidebar.date_input("Date Range", [df['Date'].min(), df['Date'].max()])
        if len(date_range) == 2:
            start_date, end_date = date_range
            df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

    # Plot air quality indicators
    pollutants = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']
    available_pollutants = [p for p in pollutants if p in df.columns]

    selected_pollutant = st.selectbox("Select Pollutant to Visualize", available_pollutants)

    if selected_pollutant:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=df, x='Date', y=selected_pollutant, hue='City' if 'City' in df.columns else None, ax=ax)
        ax.set_title(f"{selected_pollutant} Levels Over Time")
        st.pyplot(fig)

    # Show summary statistics
    st.subheader("Summary Statistics")
    st.write(df.describe(include='all'))

