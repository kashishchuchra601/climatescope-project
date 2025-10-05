import pandas as pd
df = pd.read_csv("data/GlobalWeatherRepository.csv")
# print("Dataset loaded successfully!")
# print("Number of rows:", len(df))
# print("Columns:", df.columns.tolist())

# print(df.info())
# print(df.describe())

# print("Missing values before cleaning:")
# print(df.isnull().sum())
# df = df.dropna(subset=["temperature_celsius", "humidity"])
# print(" Missing values handled successfully.")


# Remove impossible values
# df = df[(df["temperature_celsius"] > -50) & (df["temperature_celsius"] < 60)]
# df = df[(df["humidity"] >= 0) & (df["humidity"] <= 100)]
# print(" Anomalies handled successfully.")


# from sklearn.preprocessing import MinMaxScaler
# scaler = MinMaxScaler()
# df[["temperature_celsius", "humidity"]] = scaler.fit_transform(df[["temperature_celsius", "humidity"]])
# print(" Values normalized successfully.")



df['last_updated'] = pd.to_datetime(df['last_updated'], errors='coerce')
df = df.dropna(subset=['last_updated'])
monthly_avg = df.groupby(df['last_updated'].dt.to_period('M')).mean(numeric_only=True).reset_index()
monthly_avg.to_csv('data/monthly_average.csv', index=False)
print(" Aggregated to monthly averages and saved successfully!")