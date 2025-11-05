# -----------------------------------------------
# Servidor Flask IoT - Recibe datos desde ESP32
# y permite consulta por Streamlit
# -----------------------------------------------
from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # permite acceso desde Streamlit u otras apps

DATA_FILE = "lecturas.csv"

# Crear archivo CSV si no existe
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["fecha", "humo_detectado"])


@app.route('/')
def home():
    return """
    <h2>🔥 Servidor IoT Activo ✅</h2>
    <p>Usa el endpoint <b>/datos</b> (POST) para enviar lecturas desde la ESP32.</p>
    <p>Y el endpoint <b>/ultimos</b> (GET) para ver los datos recientes.</p>
    """


@app.route('/datos', methods=['POST'])
def recibir_datos():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No se recibieron datos"}), 400
            
        humo = data.get("humo_detectado")

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"📡 {fecha} -> Humo={humo}")

        # Guardar en archivo CSV
        with open(DATA_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([fecha, humo])

        return jsonify({
            "mensaje": "Datos recibidos correctamente",
            "fecha": fecha,
            "humo_detectado": humo
        }), 200

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500


@app.route('/ultimos', methods=['GET'])
def ultimos_datos():
    """ Devuelve las últimas lecturas guardadas """
    datos = []
    try:
        with open(DATA_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                datos.append(row)
        return jsonify(datos[-20:])  # muestra los últimos 20 registros
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
