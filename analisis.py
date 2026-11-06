import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("clean_data/master_poverty_data.csv")

# Filtrar solo países con datos completos en 2020 (para graficar bonito)
df['year'] = df['year'].astype(str) # arregla el tipo de dato
df_2020 = df[(df['year'] == '2020') & (df['tasa_pobreza'].notna()) & (df['gini'].notna())]

# Gráfico 1: ¿Más desigualdad = más pobreza?
plt.figure()
plt.scatter(df_2020['gini'], df_2020['tasa_pobreza'])
plt.title('Relación Gini vs Tasa de Pobreza (2020)')
plt.xlabel('Gini (Desigualdad)')
plt.ylabel('Tasa Pobreza %')
plt.savefig('grafico_gini_pobreza.png')
print("Gráfico 1 guardado")

# Ver países más desiguales
print("\nTop 10 países más desiguales (2020):")
print(df_2020.sort_values('gini', ascending=False)[['Country Name','gini','tasa_pobreza']].head(10))