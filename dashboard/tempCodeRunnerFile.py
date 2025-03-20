import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
day_df = pd.read_csv("./main-data.csv")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Sidebar Filters
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Tanggal Mulai", day_df['dteday'].min())
end_date = st.sidebar.date_input("Tanggal Akhir", day_df['dteday'].max())

season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
weather_conditions = {1: "Cerah", 2: "Mendung dan Berawan", 3: "Hujan Badai", 4: "Badai Salju"}

selected_season = st.sidebar.multiselect("Pilih Musim", list(season_labels.values()), default=list(season_labels.values()))
selected_weather = st.sidebar.multiselect("Pilih Kondisi Cuaca", list(weather_conditions.values()), default=list(weather_conditions.values()))

# Apply Filters
day_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & (day_df['dteday'] <= pd.to_datetime(end_date))]
day_df = day_df[day_df['season'].map(season_labels).isin(selected_season)]
day_df = day_df[day_df['weathersit'].map(weather_conditions).isin(selected_weather)]

# Analisis berdasarkan kondisi cuaca
total_orders_df = day_df.groupby('weathersit').agg({"cnt": "sum"}).reset_index()
total_orders_df["weathersit"] = total_orders_df["weathersit"].map(weather_conditions)
total_orders_df["percentage"] = (total_orders_df["cnt"] / total_orders_df["cnt"].sum()) * 100
total_orders_df.rename(columns={"weathersit": "Kondisi Cuaca", "percentage": "Persentase Penyewaan"}, inplace=True)

# Analisis berdasarkan musim
seasonal_orders_df = day_df.groupby('season').agg({"cnt": "sum"}).reset_index()
seasonal_orders_df["season"] = seasonal_orders_df["season"].map(season_labels)
seasonal_orders_df.rename(columns={"season": "Musim", "cnt": "Total Penyewaan"}, inplace=True)

# Dashboard
st.title("Bike Rentals Dashboard")

st.header("Persentase Penyewaan Sepeda berdasarkan Kondisi Cuaca")
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(total_orders_df["Kondisi Cuaca"], total_orders_df["Persentase Penyewaan"], color="#72BCD4", edgecolor='black')
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval:.1f}%', ha='center', va='bottom', fontsize=10, color='black')
ax.set_title("Persentase Penyewaan Sepeda berdasarkan Kondisi Cuaca", loc="center", fontsize=20, pad=20)
ax.set_xlabel("Kondisi Cuaca", fontsize=14, labelpad=10)
ax.set_ylabel("Persentase Penyewaan (%)", fontsize=14, labelpad=10)
ax.set_ylim(0, 100)
ax.grid(axis='y', linestyle='--', linewidth=0.7)
st.pyplot(fig)

st.header("Pengaruh Musim terhadap Jumlah Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(seasonal_orders_df["Musim"], seasonal_orders_df["Total Penyewaan"], color="#72BCD4", edgecolor='black')
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{int(yval):,}', ha='center', va='bottom', fontsize=10, color='black')
ax.set_title("Pengaruh Musim terhadap Jumlah Penyewaan Sepeda", loc="center", fontsize=20, pad=20)
ax.set_xlabel("Musim", fontsize=14, labelpad=10)
ax.set_ylabel("Total Penyewaan", fontsize=14, labelpad=10)
ax.set_ylim(0, seasonal_orders_df["Total Penyewaan"].max() * 1.1)
ax.grid(axis='y', linestyle='--', linewidth=0.7)
st.pyplot(fig)

# RFM Analysis
rfm_df = day_df.groupby("dteday").agg({"cnt": "sum"}).reset_index()
recent_date = day_df["dteday"].max()
rfm_df["recency"] = (recent_date - rfm_df["dteday"]).dt.days
rfm_df["frequency"] = 1  # Asumsinya, satu hari satu transaksi
rfm_df.rename(columns={"cnt": "monetary"}, inplace=True)

# Menampilkan RFM Analysis di dashboard
st.header("RFM Analysis")
st.dataframe(rfm_df)
