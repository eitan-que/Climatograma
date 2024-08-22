from flask import Flask, render_template, request, redirect, url_for
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)

def determinar_hemisferio(temperaturas):
    temp_junio_julio = max(temperaturas[5], temperaturas[6])  # Junio, Julio
    temp_diciembre_enero = max(temperaturas[11], temperaturas[0])  # Diciembre, Enero
    
    if temp_junio_julio > temp_diciembre_enero:
        return "norte"
    else:
        return "sur"

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

def amplitud_termica_meses(temperaturas_min, temperaturas_max, precipitaciones):
    amplitud_termica = [max_temp - min_temp for max_temp, min_temp in zip(temperaturas_max, temperaturas_min)]
    
    # Mes de mayor precipitación
    mes_mayor_precipitacion = precipitaciones.index(max(precipitaciones))
    menor_amplitud_termica = amplitud_termica[mes_mayor_precipitacion]

    # Mes de menor precipitación
    mes_menor_precipitacion = precipitaciones.index(min(precipitaciones))
    mayor_amplitud_termica = amplitud_termica[mes_menor_precipitacion]

    return (mes_mayor_precipitacion, round(menor_amplitud_termica, 2)), (mes_menor_precipitacion, round(mayor_amplitud_termica, 2))

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

        promedio_temp = round(sum(temperaturas) / len(temperaturas), 2)
        total_precipitacion = sum(precipitaciones)

        hemisferio = determinar_hemisferio(temperaturas)
        clima = tipo_clima(promedio_temp)
        area = determinar_area(abs(hemisferio == 'sur') * 23.5)
        precipitacion_tipo = tipo_precipitacion(total_precipitacion)
        topografia = analizar_topografia(temperaturas, precipitaciones)
        continentalidad = analizar_continentalidad(temperaturas)
        
        (mes_mayor_precipitacion, menor_amplitud), (mes_menor_precipitacion, mayor_amplitud) = amplitud_termica_meses(temperaturas_min, temperaturas_max, precipitaciones)

        # Gráfico
        plt.figure(figsize=(10, 6))
        plt.bar(meses, precipitaciones, color='blue', alpha=0.7, label='Precipitaciones')
        
        plt.plot(meses, temperaturas_min, color='yellow', marker='o', linestyle='-', label='Temp Mínima')
        plt.plot(meses, temperaturas, color='orange', marker='o', linestyle='-', label='Temp Media')
        plt.plot(meses, temperaturas_max, color='red', marker='o', linestyle='-', label='Temp Máxima')

        plt.xlabel('Meses')
        plt.ylabel('Temperatura / Precipitaciones')
        plt.title(f'Climatograma de: {nom}')
        plt.legend()

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        # Datos para mostrar en HTML
        datos_climaticos = {
            "nombre": nom,
            "hemisferio": hemisferio.capitalize(),
            "clima": clima,
            "area": area,
            "tipo_precipitacion": precipitacion_tipo,
            "topografia": topografia,
            "continentalidad": continentalidad,
            "mayor_amplitud_mes": meses[mes_menor_precipitacion],
            "mayor_amplitud": mayor_amplitud,
            "menor_amplitud_mes": meses[mes_mayor_precipitacion],
            "menor_amplitud": menor_amplitud,
            "temp_max": round(max(temperaturas_max), 2),
            "temp_media": promedio_temp,
            "temp_min": round(min(temperaturas_min), 2)
        }

        return render_template('index.html', plot_url=plot_url, datos_climaticos=datos_climaticos)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
