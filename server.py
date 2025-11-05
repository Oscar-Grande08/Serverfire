# -----------------------------------------------
# Servidor Flask para recibir datos de la ESP32
# Autor: Oscar Grande
# Despliegue: Render (100% gratuito)
# -----------------------------------------------

from flask import Flask, request, jsonify

app = Flask(__name__)

# ------------------ RUTA PRINCIPAL ------------------
@app.route('/')
def home():
    return """
    <h1>Servidor IoT activo ✅</h1>
    <p>Bienvenido, la API está lista para recibir datos.</p>
    <p>Usa el endpoint <b>/datos</b> para enviar lecturas desde la ESP32.</p>
    """

# ------------------ RUTA /DATOS ------------------
@app.route('/datos', methods=['POST'])
def recibir_datos():
    try:
        # Se obtiene el JSON que envía la ESP32
        data = request.get_json()

        if not data:
            return jsonify({"error": "No se recibieron datos"}), 400

        # Extraer valores del JSON
        temperatura = data.get('temperatura')
        humedad = data.get('humedad')

        # Mostrar en la consola del servidor (útil para pruebas)
        print(f"📡 Datos recibidos -> Temperatura: {temperatura}°C | Humedad: {humedad}%")

        # Responder a la ESP32
        return jsonify({
            "mensaje": "Datos recibidos correctamente",
            "temperatura": temperatura,
            "humedad": humedad
        }), 200

    except Exception as e:
        print("❌ Error al procesar datos:", e)
        return jsonify({"error": "Error interno del servidor"}), 500


# ------------------ CONFIGURACIÓN DEL SERVIDOR ------------------
if __name__ == '__main__':
    # host="0.0.0.0" permite conexiones externas (necesario en Render)
    # port=5000 es el puerto estándar que Render detecta automáticamente
    app.run(host='0.0.0.0', port=5000)
