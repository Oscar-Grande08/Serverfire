from flask import Flask, request, jsonify
from flask_cors import CORS  # <--- agrega esto

app = Flask(__name__)
CORS(app)  # <--- habilita CORS

@app.route('/')
def home():
    return """
    <h1>Servidor IoT activo ✅</h1>
    <p>Bienvenido, la API está lista para recibir datos.</p>
    <p>Usa el endpoint <b>/datos</b> para enviar lecturas desde la ESP32.</p>
    """

@app.route('/datos', methods=['POST'])
def recibir_datos():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No se recibieron datos"}), 400

        temperatura = data.get('temperatura')
        humedad = data.get('humedad')

        print(f"📡 Datos recibidos -> Temperatura: {temperatura}°C | Humedad: {humedad}%")

        return jsonify({
            "mensaje": "Datos recibidos correctamente",
            "temperatura": temperatura,
            "humedad": humedad
        }), 200

    except Exception as e:
        print("❌ Error al procesar datos:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
