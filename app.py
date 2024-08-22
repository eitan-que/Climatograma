from flask import Flask, render_template, request, redirect, url_for
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)

def determinar_hemisferio(temperaturas):
    max_temp_index = temperaturas.index(max(temperaturas))
    if max_temp_index in [0, 1, 11]:  # Meses de Diciembre, Enero, Febrero
        return "sur"
    elif max_temp_index in [5, 6, 7]:  # Meses de Junio, Julio, Agosto
        return "norte"
    else:
        return "indeterminado"

def tipo_clima(promedio):
    if promedio >= 20:
        return "cálido"
    elif promedio > 10:
        return "templado"
    else:
        return "frío"

def determinar_area(latitud):
    if latitud < 20:
        return "cálido"
    elif latitud < 60:
        return "templado"
    else:
        return "frío"

def tipo_precipitacion(total_precipitacion):
    if total_precipitacion > 2000:
        return "húmedo"
    elif total_precipitacion > 1000:
        return "semi-húmedo"
    elif total_precipitacion > 500:
        return "semi-árido"
    else:
        return "árido"

def analizar_topografia(temperaturas, precipitaciones):
    if temperaturas.index(max(temperaturas)) == precipitaciones.index(max(precipitaciones)):
        return "llana"
    else:
        return "montañosa"

def analizar_continentalidad(temperaturas):
    rango_temperaturas = max(temperaturas) - min(temperaturas)
    if rango_temperaturas < 10:
        return "marítima"
    elif rango_temperaturas < 20:
        return "media"
    else:
        return "continental"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nom = request.form['nombre']
        temperaturaI = request.form['temperatura']
        temperatura_minI = request.form['temperatura_min']
        temperatura_maxI = request.form['temperatura_max']
        preciI = request.form['precipitacion']

        temperaturas = [float(temp) for temp in temperaturaI.split(',') if temp.strip()]
        temperaturas_min = [float(temp) for temp in temperatura_minI.split(',') if temp.strip()]
        temperaturas_max = [float(temp) for temp in temperatura_maxI.split(',') if temp.strip()]
        precipitaciones = [float(pre) for pre in preciI.split(',')]
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

        # Cálculos
        promedio_temp = sum(temperaturas) / len(temperaturas)
        total_precipitacion = sum(precipitaciones)

        hemisferio = determinar_hemisferio(temperaturas)
        clima = tipo_clima(promedio_temp)
        area = determinar_area(abs(hemisferio == 'sur') * 23.5)  # Usando latitud de referencia según el hemisferio
        precipitacion_tipo = tipo_precipitacion(total_precipitacion)
        topografia = analizar_topografia(temperaturas, precipitaciones)
        continentalidad = analizar_continentalidad(temperaturas)

        # Gráfico
        plt.figure(figsize=(10, 6))
        plt.bar(meses, precipitaciones, color='blue', alpha=0.7, label='Precipitaciones')
        
        # Añadir las líneas de temperaturas
        plt.plot(meses, temperaturas_min, color='yellow', marker='o', linestyle='-', label='Temp Mínima')
        plt.plot(meses, temperaturas, color='orange', marker='o', linestyle='-', label='Temp Media')
        plt.plot(meses, temperaturas_max, color='red', marker='o', linestyle='-', label='Temp Máxima')

        # Añadir textos con datos climáticos
        plt.text(11, min(precipitaciones) - 10, f'Zona {topografia}', fontsize=12, ha='center')
        plt.text(11, min(precipitaciones) - 20, f'Clima {clima}', fontsize=12, ha='center')
        plt.text(11, min(precipitaciones) - 30, f'Hemisferio {hemisferio.capitalize()}', fontsize=12, ha='center')
        plt.text(11, min(precipitaciones) - 40, f'Área {area}', fontsize=12, ha='center')
        plt.text(11, min(precipitaciones) - 50, f'Tipo de Precipitación {precipitacion_tipo}', fontsize=12, ha='center')
        plt.text(11, min(precipitaciones) - 60, f'Continentalidad {continentalidad}', fontsize=12, ha='center')

        # Mostrar temperaturas mínima y máxima en el gráfico
        plt.text(0, max(temperaturas_max) + 5, f'Temp Máx: {max(temperaturas_max)}°C', fontsize=10, ha='left', va='top')
        plt.text(0, max(temperaturas_max) + 10, f'Temp Mín: {min(temperaturas_min)}°C', fontsize=10, ha='left', va='top')

        plt.xlabel('Meses')
        plt.ylabel('Temperatura / Precipitaciones')
        plt.title(f'Climatograma de: {nom}')
        plt.legend()

        # Guardar imagen en base64
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        return render_template('index.html', plot_url=plot_url)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
