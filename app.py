from flask import Flask, render_template, request, send_file
import pandas as pd
from io import StringIO, BytesIO

app = Flask(__name__)

# Función que procesa el CSV
def limpiar_csv(contenido_csv):
    # Convertir el archivo en un DataFrame
    lines = contenido_csv.strip().split("\n")
    start_index = 0
    for i, line in enumerate(lines):
        if "Fecha de inicio (huso horario de UTC)" in line:
            start_index = i
            break

    # Obtener solo las líneas con datos
    data_lines = lines[start_index:]
    clean_data = "\n".join(data_lines)

    # Reemplazar comas por puntos en los números
    clean_data = clean_data.replace(",", ".")

    # Reemplazar tabuladores por comas
    clean_data = clean_data.replace("\t", ",")

    # Crear el DataFrame
    df = pd.read_csv(StringIO(clean_data))
    
    # Guardar en un archivo CSV
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return output

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    if 'file' not in request.files:
        return "No file uploaded", 400
    file = request.files['file']

    if file.filename == '':
        return "No file selected", 400

    # Procesar el archivo CSV
    contenido_csv = file.read().decode('utf-8')
    output = limpiar_csv(contenido_csv)

    # Devolver el archivo procesado
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name='archivo_procesado.csv')

# Eliminar o comentar esta línea en producción
# if __name__ == "__main__":
#     app.run(debug=True)
