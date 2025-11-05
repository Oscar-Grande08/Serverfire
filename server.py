from flask import Flask, request, jsonify
from flask_cors import CORS  # permite peticiones desde otros dispositivos (como la ESP32)

app = Flask(__name__)
CORS(app)  # habilita CORS para todos los orígenes

# Lista global para guardar las lecturas recibidas
lecturas = []


@app.route('/')
def home():
    return """
    <h1>Servidor IoT activo ✅</h1>
    <p>Bienvenido, la API está lista para recibir y consultar datos.</p>
    <ul>
        <li><b>POST /datos</b> → para enviar lecturas desde la ESP32.</li>
        <li><b>GET /lecturas</b> → para ver las lecturas recibidas.</li>
    </ul>
    """


@app.route('/datos', methods=['POST'])
def recibir_datos():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No se recibieron datos"}), 400

        temperatura = data.get('temperatura')
        humedad = data.get('humedad')

        lectura = {"temperatura": temperatura, "humedad": humedad}
        lecturas.append(lectura)  # Guarda la lectura en la lista

        print(f"📡 Datos recibidos -> Temperatura: {temperatura}°C | Humedad: {humedad}%")

        return jsonify({
            "mensaje": "Datos recibidos correctamente",
            "lectura": lectura
        }), 200

    except Exception as e:
        print("❌ Error al procesar datos:", e)
        return jsonify({"error": str(e)}), 500


@app.route('/lecturas', methods=['GET'])
def obtener_lecturas():
    """Devuelve todas las lecturas almacenadas en formato JSON"""
    return jsonify({
        "cantidad": len(lecturas),
        "lecturas": lecturas
    }), 200


if __name__ == '__main__':
    # Ejecuta el servidor en todas las direcciones disponibles (0.0.0.0) en el puerto 5000
    app.run(host='0.0.0.0', port=5000)
