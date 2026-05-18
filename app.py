# =========================================================
# AgroEquidad - Aplicación Flask
# Análisis de créditos agropecuarios en Cundinamarca
# =========================================================

from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# =========================================================
# CARGA Y LIMPIEZA DEL DATASET (solo se hace 1 vez al iniciar)
# =========================================================
print("Cargando dataset...")
df = pd.read_excel('DATASETCUNDINAMARCA.xlsx')

# Limpieza
df = df.drop(columns=['Departamento Inversion'])
df['% FAG'] = df['% FAG'].fillna(0)
df['Vlr Inic Garantia'] = df['Vlr Inic Garantia'].fillna(0)
df['Genero'] = df['Genero'].replace({'H': 'Hombre', 'M': 'Mujer', 'S': 'Sociedad'})
df['PostConflicto'] = df['Municipio de PostConflico?'].replace({'S': 'Sí', 'N': 'No'})
df = df.drop_duplicates()

print(f"Dataset listo: {len(df):,} créditos")


# =========================================================
# FUNCIONES PARA CALCULAR LOS DATOS
# =========================================================

def estadisticas_generales():
    return {
        'total_creditos': int(len(df)),
        'dinero_total': float(df['Valor Inversion'].sum()),
        'credito_promedio': float(df['Valor Inversion'].mean()),
        'municipios': int(df['Municipio Inversion'].nunique()),
        'año_min': int(df['Año'].min()),
        'año_max': int(df['Año'].max()),
    }


def top_municipios(n=10):
    top = df.groupby('Municipio Inversion')['Valor Inversion'].sum()
    top = top.sort_values(ascending=False).head(n)
    return [{'nombre': nombre, 'col': float(valor)} for nombre, valor in top.items()]


def bottom_municipios(n=10):
    bot = df.groupby('Municipio Inversion')['Valor Inversion'].sum()
    bot = bot.sort_values().head(n)
    return [{'nombre': nombre, 'col': float(valor)} for nombre, valor in bot.items()]


def por_tipo_productor():
    resultado = {}
    for tipo in df['Tipo Productor'].unique():
        sub = df[df['Tipo Productor'] == tipo]
        resultado[tipo] = {
            'cantidad': int(len(sub)),
            'dinero': float(sub['Valor Inversion'].sum()),
            'promedio': float(sub['Valor Inversion'].mean()),
        }
    return resultado


def por_genero():
    resultado = {}
    for genero in df['Genero'].unique():
        sub = df[df['Genero'] == genero]
        resultado[genero] = {
            'cantidad': int(len(sub)),
            'dinero': float(sub['Valor Inversion'].sum()),
            'promedio': float(sub['Valor Inversion'].mean()),
        }
    return resultado


def evolucion_anual():
    evol = df.groupby('Año')['Valor Inversion'].sum()
    return [{'año': int(año), 'col': float(valor)} for año, valor in evol.items()]


# =========================================================
# RUTAS DE LA APLICACIÓN
# =========================================================

@app.route('/')
def home():
    """Página principal: pasa todos los datos al HTML"""
    datos = {
        'stats': estadisticas_generales(),
        'top_municipios': top_municipios(10),
        'bot_municipios': bottom_municipios(10),
        'productores': por_tipo_productor(),
        'generos': por_genero(),
        'evolucion': evolucion_anual(),
    }
    return render_template('index.html', datos=datos)


@app.route('/api/datos')
def api_datos():
    """Endpoint JSON por si quieren consumir los datos desde otro lado"""
    return jsonify({
        'stats': estadisticas_generales(),
        'top_municipios': top_municipios(10),
        'bot_municipios': bottom_municipios(10),
        'productores': por_tipo_productor(),
        'generos': por_genero(),
        'evolucion': evolucion_anual(),
    })


# =========================================================
# EJECUTAR LA APP
# =========================================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)