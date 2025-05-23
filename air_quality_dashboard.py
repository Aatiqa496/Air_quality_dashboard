import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set up page
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

# Load CSV data directly (this file must be in your repo)
df = pd.read_csv("air_quality_data.csv")

st.title("📊 Air Quality Dashboard")

# Data preview
st.write("Data Preview", df.head())

# You can add more charts here later
