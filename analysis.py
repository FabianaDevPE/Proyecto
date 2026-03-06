import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create an engine / connection
conn = psycopg2.connect("postgresql://poryectito_bd_user:LddnT8PoLQmuIN0eTPgeZLIEx2qlgKTO@dpg-d6lcnafafjfc73fav460-a.oregon-postgres.render.com/poryectito_bd")
df = pd.read_sql('SELECT * FROM living', conn)

# Clean numerical columns
df['Cost of living, 2017'] = pd.to_numeric(df['Cost of living, 2017'], errors='coerce')
df['Global rank'] = pd.to_numeric(df['Global rank'], errors='coerce')

# Drop rows with NaN in Cost of living
df = df.dropna(subset=['Cost of living, 2017'])

# 1. Dataset Review
num_rows = len(df)
num_cols = len(df.columns)
avg_cost = df['Cost of living, 2017'].mean()
highest_cost_country = df.loc[df['Cost of living, 2017'].idxmax(), 'Countries']
lowest_cost_country = df.loc[df['Cost of living, 2017'].idxmin(), 'Countries']

# Peru stats
peru_row = df[df['Countries'].str.contains('Peru', case=False, na=False)]
if not peru_row.empty:
    peru_cost = peru_row['Cost of living, 2017'].values[0]
    peru_rank = peru_row['Global rank'].values[0]
else:
    peru_cost = "Not Found"
    peru_rank = "Not Found"

print("--- REVISIÓN INICIAL DEL DATASET ---")
print(f"Nro. de Filas: {num_rows}")
print(f"Nro. de Columnas: {num_cols}")
print(f"Costo de vida promedio: {avg_cost:.2f}")
print(f"País con costo de vida más alto: {highest_cost_country}")
print(f"País con costo de vida más bajo: {lowest_cost_country}")
print(f"Costo de Vida en Perú: {peru_cost}")
print(f"Ranking de Perú: {peru_rank}")

# 2. Visualizations
sns.set_theme(style="whitegrid")
output_dir = r"d:\Proyecto"

# Top 10 Countries with highest cost of living
top_10_highest = df.nlargest(10, 'Cost of living, 2017')
plt.figure(figsize=(10, 6))
sns.barplot(data=top_10_highest, x='Cost of living, 2017', y='Countries', palette='Reds_r')
plt.title("Los 10 países con el costo de vida más alto (2017)")
plt.xlabel("Costo de Vida")
plt.ylabel("Países")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "top_10_highest.png"))
plt.show()

# Top 10 Countries with lowest cost of living
top_10_lowest = df.nsmallest(10, 'Cost of living, 2017')
plt.figure(figsize=(10, 6))
sns.barplot(data=top_10_lowest, x='Cost of living, 2017', y='Countries', palette='Greens_r')
plt.title("Los 10 países con el costo de vida más bajo (2017)")
plt.xlabel("Costo de Vida")
plt.ylabel("Países")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "top_10_lowest.png"))
plt.show()

# Cost of living of countries in America
america_df = df[df['Continent'].str.contains('America', case=False, na=False)].sort_values(by='Cost of living, 2017', ascending=False)
plt.figure(figsize=(10, len(america_df) * 0.3 + 2)) # Adjust height based on number of countries
sns.barplot(data=america_df, x='Cost of living, 2017', y='Countries', palette='Blues_r')
plt.title("Costo de vida de los países de América (2017)")
plt.xlabel("Costo de Vida")
plt.ylabel("Países")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "america_cost.png"))
plt.show()

print("--- EXECUTED SUCCESSFULLY ---")
