# =========================================================
# PROYECTO: Créditos agropecuarios en Cundinamarca
# Versión final para sustentación
# =========================================================

import pandas as pd
import matplotlib.pyplot as plt

# -------- PASO 1: Cargar el dataset --------
df = pd.read_excel('DATASETCUNDINAMARCA.xlsx')
print("Filas:", len(df), "| Columnas:", len(df.columns))


# -------- PASO 2: Limpieza de datos --------

# 2.1 Quitamos columna que no aporta (todo es Cundinamarca)
df = df.drop(columns=['Departamento Inversion'])

# 2.2 Los vacíos en FAG significan "sin garantía", se llenan con 0
df['% FAG'] = df['% FAG'].fillna(0)
df['Vlr Inic Garantia'] = df['Vlr Inic Garantia'].fillna(0)

# 2.3 Cambiamos códigos por palabras claras
df['Genero'] = df['Genero'].replace({'H': 'Hombre', 'M': 'Mujer', 'S': 'Sociedad'})
df['PostConflicto'] = df['Municipio de PostConflico?'].replace({'S': 'Sí', 'N': 'No'})

# 2.4 Quitamos duplicados
df = df.drop_duplicates()

print("Limpieza completa")
print()


# -------- PASO 3: Estadísticas generales (para la presentación) --------
print("=== ESTADÍSTICAS GENERALES ===")
print(f"Total de créditos: {len(df):,}")
print(f"Dinero total: ${df['Valor Inversion'].sum()/1e9:,.0f} mil millones")
print(f"Crédito promedio: ${df['Valor Inversion'].mean()/1e6:,.0f} millones")
print(f"Municipios beneficiados: {df['Municipio Inversion'].nunique()}")
print(f"Periodo: {df['Año'].min()} - {df['Año'].max()}")
print()


# =========================================================
# GRÁFICA 1: Top 10 municipios con MÁS dinero
# =========================================================
top_municipios = df.groupby('Municipio Inversion')['Valor Inversion'].sum()
top_municipios = top_municipios.sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
plt.barh(top_municipios.index, top_municipios.values / 1e9, color='steelblue')
plt.title('Top 10 municipios con más financiación')
plt.xlabel('Miles de millones COP')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()


# =========================================================
# GRÁFICA 2: Top 10 municipios con MENOS dinero (los olvidados)
# =========================================================
bot_municipios = df.groupby('Municipio Inversion')['Valor Inversion'].sum()
bot_municipios = bot_municipios.sort_values().head(10)

plt.figure(figsize=(10, 6))
plt.barh(bot_municipios.index, bot_municipios.values / 1e6, color='salmon')
plt.title('10 municipios con menor financiación')
plt.xlabel('Millones COP')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()


# =========================================================
# GRÁFICA 3: Distribución del dinero por tipo de productor
# =========================================================
por_productor = df.groupby('Tipo Productor')['Valor Inversion'].sum()

plt.figure(figsize=(7, 7))
plt.pie(por_productor, labels=por_productor.index, autopct='%1.1f%%',
        colors=['#06A77D', '#F1A208', '#A4031F', '#2E86AB'])
plt.title('Distribución del dinero por tipo de productor')
plt.show()


# =========================================================
# GRÁFICA 4: Cantidad de créditos por tipo de productor
# (el contraste con la gráfica 3 es clave para mostrar la desigualdad)
# =========================================================
cantidad_productor = df['Tipo Productor'].value_counts()

plt.figure(figsize=(8, 6))
plt.bar(cantidad_productor.index, cantidad_productor.values, color='teal')
plt.title('Cantidad de créditos por tipo de productor')
plt.ylabel('Cantidad de créditos')
plt.show()


# =========================================================
# GRÁFICA 5: Evolución del crédito por año
# =========================================================
por_año = df.groupby('Año')['Valor Inversion'].sum()

plt.figure(figsize=(8, 5))
plt.plot(por_año.index, por_año.values / 1e9, marker='o', linewidth=2, color='darkblue')
plt.title('Evolución del crédito agropecuario')
plt.xlabel('Año')
plt.ylabel('Miles de millones COP')
plt.grid(True)
plt.show()


# =========================================================
# GRÁFICA 6: Créditos por género y año (agrupados)
# =========================================================
genero_año = df.groupby(['Año', 'Genero'])['Valor Inversion'].sum().unstack() / 1e9

plt.figure(figsize=(9, 5))
genero_año.plot(kind='bar', ax=plt.gca(), color=['#2E86AB', '#E63946', '#06A77D'])
plt.title('Créditos por género y año')
plt.xlabel('Año')
plt.ylabel('Miles de millones COP')
plt.xticks(rotation=0)
plt.legend(title='Género')
plt.tight_layout()
plt.show()


# =========================================================
# GRÁFICA 7: Mapa de Cundinamarca por municipio
# =========================================================
mapa_datos = df.groupby('Municipio Inversion').agg(
    lat=('LATITUD', 'mean'),
    lon=('LONGITUD', 'mean'),
    dinero=('Valor Inversion', 'sum')
).reset_index()

plt.figure(figsize=(10, 8))
plt.scatter(mapa_datos['lon'], mapa_datos['lat'],
            s=mapa_datos['dinero'] / 1e10,
            c=mapa_datos['dinero'] / 1e9,
            cmap='YlOrRd', alpha=0.7, edgecolors='black')
plt.colorbar(label='Miles de millones COP')
plt.title('Mapa de Cundinamarca: dinero por municipio')
plt.xlabel('Longitud')
plt.ylabel('Latitud')
plt.tight_layout()
plt.show()


# =========================================================
# TABLAS RESUMEN ÚTILES
# =========================================================
print("\n=== RESUMEN POR TIPO DE PRODUCTOR ===")
print(df.groupby('Tipo Productor').agg(
    Cantidad=('Valor Inversion', 'count'),
    Dinero_total=('Valor Inversion', 'sum'),
    Promedio=('Valor Inversion', 'mean')
).round(0))

print("\n=== TOP 5 MUNICIPIOS ===")
print(top_municipios.head().round(0))

print("\n=== CRÉDITOS POR GÉNERO ===")
print(df.groupby('Genero')['Valor Inversion'].agg(['count', 'sum', 'mean']).round(0))