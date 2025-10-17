 #perform statistical analysis(data dustribution(histogram &box plot),correlation,seasonal patterns)
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Load dataset
df = pd.read_csv(r"C:\Users\Kashi\Desktop\climatescope-project\data\monthly_average.csv")

# Display basic info
# print(df.describe())
#correlation heatmap
# numeric_df=df.select_dtypes(include=['number'])
# plt.figure(figsize=(8,6))
# sns.heatmap(numeric_df.corr(),annot=True, cmap="coolwarm")
# plt.title("correlation heatmap")
# plt.show()




# Extreme temperature condition (above 40°C)
# extreme_temps = df[df['temperature_celsius'] > 40]

# Extreme rainfall condition (precipitation more than 100 mm)
# extreme_rain = df[df['precip_mm'] > 100]

# Plot temperature distribution
# sns.histplot(df['temperature_celsius'], bins=30, kde=True)
# plt.axvline(40, color='red', linestyle='--')
# plt.title('Temperature Distribution with Extreme Threshold (40°C)')
# plt.xlabel('Temperature (°C)')
# plt.ylabel('Frequency')
# plt.show()
# print("Number of extremely hot days:", len(extreme_temps))
# print("Number of heavy rainfall days:", len(extreme_rain))





#compare
# def assign_region (lat):
#     if lat>=23.5:
#         return 'North'
#     elif lat>=8:
#         return'Central'
#     else:
#         return'South'
# df['region']=df['latitude'].apply(assign_region)
# region_avg=df.groupby('region')['temperature_celsius'].mean().reset_index()
# sns.barplot(data=region_avg, x='region',y='temperature_celsius')
# plt.title('average temperature by region ')
# plt.xlabel('region')
# plt.ylabel('average temperature ')
# plt.show()

df['last_updated']=pd.to_datetime(df['last_updated'])
df['month']=df['last_updated'].dt.strftime('%b')
def assign_region(lat):
    if lat>=23.5:
        return 'north' 
    elif lat>=8:
        return 'central'
    else:
        return 'south'
df['region']=df['latitude'].apply(assign_region)
fig=px.line(df, x='month', y='temperature_celsius', color='region', title='monthly temperature trend by region', markers=True)
fig.show()