import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('DATASETCUNDINAMARCA.xlsx')



print("Filas:", len(df), "| Columnas:", len(df.columns))



# 2: LIMPIEZA DE DATOS


# Elimina una columna que no se necesita
df = df.drop(columns=['Departamento Inversion'])

# Si hay espacios vacíos en "% FAG", los reemplaza por 0
# fillna = llenar datos vacíos
df['% FAG'] = df["% FAG"].fillna(0)

# Hace lo mismo con la columna de garantía
df['Vlr Inic Garantia'] = df['Vlr Inic Garantia'].fillna(0)


# H -> Hombre
# M -> Mujer
# S -> Sociedad
df['Genero'] = df['Genero'].replace({
    'H': 'Hombre',
    'M': 'Mujer',
    'S': 'Sociedad'
})

# Elimina filas repetidas para evitar datos duplicados
df = df.drop_duplicates()

# TOTAL = suma de todo el dinero invertido
TOTAL = df['Valor Inversion'].sum()

# TOTAL_CRED = cantidad total de créditos
TOTAL_CRED = len(df)

print("Limpieza completa\n")



# 3: ESTADÍSTICAS GENERALES


print("=== ESTADÍSTICAS GENERALES ===")

# Muestra cantidad total de créditos
print(f"Total de créditos: {TOTAL_CRED:,}")

# Muestra todo el dinero en miles de millones
print(f"Dinero total: ${TOTAL/1e9:,.0f} mil millones")

# Calcula el promedio de cada crédito
print(f"Crédito promedio: ${df['Valor Inversion'].mean()/1e6:,.0f} millones")

# Cuenta cuántos municipios diferentes hay
print(f"Municipios beneficiados: {df['Municipio Inversion'].nunique()}")

# Muestra desde qué año hasta qué año hay datos
print(f"Periodo: {df['Año'].min()} - {df['Año'].max()}\n")


# GRÁFICA 1:
# TOP 10 MUNICIPIOS CON MÁS DINERO



top_municipios = (
    df.groupby('Municipio Inversion')['Valor Inversion']
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

# Tamaño de la gráfica
plt.figure(figsize=(10, 6))

# Colores:
# los primeros 3 más oscuros para resaltarlos
colores = ['#2D6A4F' if i < 3 else '#52B788'
           for i in range(len(top_municipios))]

# Gráfica horizontal
plt.barh(
    top_municipios.index,
    top_municipios.values / 1e9,
    color=colores
)

# Título
plt.title(
    'Top 10 municipios con más financiación',
    fontsize=14,
    fontweight='bold'
)

# Texto del eje X
plt.xlabel('Miles de millones COP')

# Invierte el orden para que el mayor quede arriba
plt.gca().invert_yaxis()

# Ajusta espacios automáticamente
plt.tight_layout()

# Muestra la gráfica
plt.show()



# GRÁFICA 2:
# 10 MUNICIPIOS CON MENOS DINERO


# Igual que la anterior, pero de menor a mayor
bot_municipios = (
    df.groupby('Municipio Inversion')['Valor Inversion']
      .sum()
      .sort_values()
      .head(10)
)

plt.figure(figsize=(10, 6))

# Gráfica horizontal color rojo
plt.barh(
    bot_municipios.index,
    bot_municipios.values / 1e6,
    color='#C1392B'
)

plt.title(
    '10 municipios con menor financiación',
    fontsize=14,
    fontweight='bold'
)

plt.xlabel('Millones COP')

# Para que el más pequeño quede arriba
plt.gca().invert_yaxis()

plt.tight_layout()
plt.show()



# GRÁFICA 3:
# DISTRIBUCIÓN DEL DINERO POR TIPO DE PRODUCTOR
# (GRÁFICA DONA)


# Agrupa por tipo de productor y suma el dinero
por_productor_dinero = (
    df.groupby('Tipo Productor')['Valor Inversion']
      .sum()
)

# Crea figura y ejes
fig, ax = plt.subplots(figsize=(7, 7))

# Gráfica tipo dona
ax.pie(
    por_productor_dinero,

    # Nombres de las categorías
    labels=por_productor_dinero.index,

    # Muestra porcentaje automático
    autopct='%1.1f%%',

    # Colores personalizados
    colors=['#C1392B', '#C68642', '#2D6A4F', '#52B788'],

    # Hace el hueco del centro
    wedgeprops=dict(width=0.55),

    # Gira la gráfica
    startangle=90
)

ax.set_title(
    'Distribución del DINERO por tipo de productor',
    fontsize=13,
    fontweight='bold'
)

plt.tight_layout()
plt.show()



# GRÁFICA 4:
# % DE CRÉDITOS VS % DEL DINERO


# Crea un resumen agrupando por tipo de productor
resumen_prod = df.groupby('Tipo Productor').agg(

    # Cuenta créditos
    cantidad=('Valor Inversion', 'count'),

    # Suma dinero
    dinero=('Valor Inversion', 'sum')

).reset_index()

# Calcula el porcentaje de créditos
resumen_prod['pct_cantidad'] = (
    resumen_prod['cantidad'] / TOTAL_CRED * 100
)

# Calcula el porcentaje del dinero
resumen_prod['pct_dinero'] = (
    resumen_prod['dinero'] / TOTAL * 100
)

# Posiciones de las barras
x = range(len(resumen_prod))

# Ancho de cada barra
ancho = 0.35

plt.figure(figsize=(9, 6))

# Barras verdes = cantidad de créditos
plt.bar(
    [i - ancho/2 for i in x],
    resumen_prod['pct_cantidad'],
    width=ancho,
    label='% de créditos',
    color='#52B788'
)

# Barras rojas = porcentaje del dinero
plt.bar(
    [i + ancho/2 for i in x],
    resumen_prod['pct_dinero'],
    width=ancho,
    label='% del dinero',
    color='#C1392B'
)

# Nombres debajo de las barras
plt.xticks(x, resumen_prod['Tipo Productor'])

plt.ylabel('%')

plt.title(
    'Cantidad de créditos vs Dinero recibido por tipo de productor',
    fontsize=13,
    fontweight='bold'
)

# Muestra leyenda
plt.legend()

plt.tight_layout()
plt.show()



# GRÁFICA 5:
# EVOLUCIÓN ANUAL DEL CRÉDITO

# Agrupa por año y suma el dinero
por_año = df.groupby('Año')['Valor Inversion'].sum()

plt.figure(figsize=(8, 5))

# Línea principal
plt.plot(
    por_año.index,
    por_año.values / 1e9,

    marker='o',
    linewidth=2.5,
    color='#2D6A4F',

    markerfacecolor='#2D6A4F',
    markersize=8
)

# Sombra debajo de la línea
plt.fill_between(
    por_año.index,
    por_año.values / 1e9,

    alpha=0.08,
    color='#2D6A4F'
)

plt.title(
    'Evolución del crédito agropecuario — Cundinamarca',
    fontsize=13,
    fontweight='bold'
)

plt.xlabel('Año')
plt.ylabel('Miles de millones COP')

# Cuadrícula suave
plt.grid(True, color='#EDE8DC')

plt.tight_layout()
plt.show()



# GRÁFICA 6:
# MONTO TOTAL POR GÉNERO


# Agrupa por género y suma el dinero
por_genero = df.groupby('Genero')['Valor Inversion'].sum()

# Diccionario de colores
colores_gen = {
    'Sociedad': '#C68642',
    'Hombre': '#2563A8',
    'Mujer': '#D946A8'
}

# Busca el color de cada categoría
colores_lista = [
    colores_gen.get(g, '#999')
    for g in por_genero.index
]

plt.figure(figsize=(7, 5))

# Barras
bars = plt.bar(
    por_genero.index,
    por_genero.values / 1e9,
    color=colores_lista
)

plt.title(
    'Monto total de crédito por género',
    fontsize=13,
    fontweight='bold'
)

plt.ylabel('Miles de millones COP')

# Agrega números arriba de cada barra
for bar, val in zip(bars, por_genero.values):

    plt.text(
        bar.get_x() + bar.get_width()/2,

        # Posición arriba de la barra
        bar.get_height() + 20,

        # Texto
        f'${val/1e9:.1f}B',

        ha='center',
        va='bottom',
        fontsize=10
    )

plt.tight_layout()
plt.show()



# GRÁFICA 7:
# CRÉDITO PROMEDIO HOMBRES VS MUJERES


# Filtra solo hombres y mujeres
hm = df[df['Genero'].isin(['Hombre', 'Mujer'])]

# Calcula promedio por género
promedio_gen = hm.groupby('Genero')['Valor Inversion'].mean()

# Busca colores
colores_hm = [
    colores_gen.get(g, '#999')
    for g in promedio_gen.index
]

plt.figure(figsize=(6, 5))

# Barras
bars2 = plt.bar(
    promedio_gen.index,
    promedio_gen.values / 1e6,
    color=colores_hm
)

plt.title(
    'Crédito promedio: Hombres vs Mujeres\n(brecha del 38%)',
    fontsize=13,
    fontweight='bold'
)

plt.ylabel('Millones COP')

# Pone el promedio encima de cada barra
for bar, val in zip(bars2, promedio_gen.values):

    plt.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height() + 0.2,

        f'${val/1e6:.1f}M',

        ha='center',
        va='bottom',
        fontsize=10
    )

plt.tight_layout()
plt.show()


# TABLAS RESUMEN


print("\n=== RESUMEN POR TIPO DE PRODUCTOR ===")

# Muestra:
# cantidad de créditos
# dinero total
# promedio
print(
    df.groupby('Tipo Productor').agg(
        Cantidad=('Valor Inversion', 'count'),
        Dinero_total=('Valor Inversion', 'sum'),
        Promedio=('Valor Inversion', 'mean')
    ).round(0)
)

print("\n=== TOP 5 MUNICIPIOS ===")

# Muestra los municipios con más dinero
print(top_municipios.head().round(0))

print("\n=== CRÉDITOS POR GÉNERO ===")

# Cuenta, suma y promedio por género
print(
    df.groupby('Genero')['Valor Inversion']
      .agg(['count', 'sum', 'mean'])
      .round(0)
)