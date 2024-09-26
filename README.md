
# WebApp de Análisis de Climatogramas

## Descripción

Esta aplicación web permite generar y analizar **climatogramas** a partir de datos ingresados por el usuario. Utiliza **Python** con el framework **Flask** para manejar las solicitudes y generar gráficos climáticos con **Matplotlib**. La app procesa información sobre las temperaturas y precipitaciones mensuales para determinar características climáticas como el tipo de clima, hemisferio, topografía y más.

## Tecnologías Utilizadas

- **Frontend**: HTML5 y CSS3
- **Backend**: Python (Flask)
- **Librerías**:
  - **Matplotlib**: Generación de gráficos.
  - **NumPy**: Cálculos numéricos.
  - **io** y **base64**: Manipulación de imágenes para su visualización en el navegador.

## Funcionalidades

- El usuario puede ingresar los datos de temperaturas y precipitaciones mensuales.
- La aplicación genera un climatograma visual que muestra:
  - **Temperatura mínima, media y máxima** a lo largo del año.
  - **Precipitaciones mensuales**.
- Análisis climático basado en los datos ingresados, que incluye:
  - **Hemisferio** (norte o sur).
  - **Tipo de clima** (cálido, templado o frío).
  - **Área** (según latitud).
  - **Tipo de precipitación** (húmedo, semi-húmedo, semi-árido, árido).
  - **Topografía** (llana o montañosa).
  - **Continentalidad** (marítima, media o continental).
  - **Amplitud térmica** en los meses de mayor y menor precipitación.

## Instalación y Configuración

### Requisitos

- Python 3.x
- Librerías: Flask, Matplotlib, NumPy

### Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/usuario/climatogramas-app.git
   ```

2. Instala las dependencias:
   ```bash
   pip install Flask matplotlib numpy
   ```

3. Inicia la aplicación:
   ```bash
   python app.py
   ```

4. Abre tu navegador y ve a `http://127.0.0.1:5000/`.


## Uso

1. En la página principal, introduce:
   - El **nombre** del lugar.
   - Las **temperaturas medias, mínimas y máximas** de cada mes (separadas por comas).
   - Las **precipitaciones mensuales** (separadas por comas).
   
2. Haz clic en **Generar Climatograma**.

3. La aplicación generará el gráfico y mostrará el análisis de los datos climáticos.

## Archivos

### `app.py`
Archivo principal de la aplicación que contiene la lógica para procesar los datos climáticos, generar gráficos y manejar las rutas.

### `templates/index.html`
Plantilla HTML que permite al usuario ingresar los datos y visualizar el climatograma generado.

### `static/styles.css`
Archivo de estilo para dar formato a la página web.

## Ejemplo de Datos

Temperaturas medias: `15.2, 14.6, 17.8, 20.1, 22.3, 24.5, 25.6, 26.1, 23.4, 19.9, 17.3, 15.0`

Temperaturas mínimas: `7.9, 6.9, 8.1, 10.2, 12.5, 14.3, 15.6, 16.0, 14.4, 10.1, 8.0, 6.0`

Temperaturas máximas: `22.5, 22.4, 23.1, 25.0, 27.5, 29.1, 30.2, 31.5, 28.4, 24.1, 23.0, 21.0`

Precipitaciones: `22, 30, 50, 70, 90, 110, 130, 140, 100, 60, 30, 20`
