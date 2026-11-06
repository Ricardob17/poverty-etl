import pandas as pd

def limpiar_indicador(nombre_archivo, nombre_columna):
    """
    Proceso de limpieza ETL:
    1. Quita 4 filas basura del Banco Mundial
    2. Filtra años 2020-2023
    3. Convierte años de columnas a filas con melt
    4. Elimina vacíos
    """
    df = pd.read_csv(f"raw_data/{nombre_archivo}.csv", skiprows=4)
    df = df[["Country Name", "Country Code", "2020", "2021", "2022", "2023"]]
    df = df.melt(
        id_vars=["Country Name", "Country Code"],
        var_name="year",
        value_name=nombre_columna
    )
    df = df.dropna(subset=[nombre_columna])
    df.to_csv(f"clean_data/{nombre_archivo}_clean.csv", index=False)
    print(f"OK: {nombre_archivo} -> {len(df)} filas")
    return df

def crear_tabla_maestra():
    """Une los 5 indicadores en una tabla maestra con merge"""
    gini = pd.read_csv("clean_data/gini_clean.csv")
    pib = pd.read_csv("clean_data/pib_clean.csv")
    poblacion = pd.read_csv("clean_data/poblacion_clean.csv")
    tasa = pd.read_csv("clean_data/pobreza_tasa_clean.csv")
    brecha = pd.read_csv("clean_data/pobreza_brecha_clean.csv")

    df_master = gini.merge(pib, on=["Country Name", "Country Code", "year"], how="outer")
    df_master = df_master.merge(poblacion, on=["Country Name", "Country Code", "year"], how="outer")
    df_master = df_master.merge(tasa, on=["Country Name", "Country Code", "year"], how="outer")
    df_master = df_master.merge(brecha, on=["Country Name", "Country Code", "year"], how="outer")
    
    df_master = df_master.sort_values(["Country Name", "year"])
    df_master.to_csv("clean_data/master_poverty_data.csv", index=False)
    print(f"\nTABLA MAESTRA: {len(df_master)} filas - clean_data/master_poverty_data.csv")
    return df_master

# === EJECUCIÓN ETL COMPLETO ===
print("=== INICIANDO ETL POBREZA Y DESIGUALDAD ===\n")
limpiar_indicador("gini", "gini")
limpiar_indicador("pib", "pib_per_capita")
limpiar_indicador("poblacion", "poblacion")
limpiar_indicador("pobreza_tasa", "tasa_pobreza")
limpiar_indicador("pobreza_brecha", "brecha_pobreza")

print("\n=== CREANDO TABLA MAESTRA ===")
df_final = crear_tabla_maestra()
print(df_final.head(15))