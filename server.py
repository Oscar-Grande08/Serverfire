
from flask import Flask, request, jsonify

app = Flask(__name__)

# Ruta principal para verificar conexión
@app.route('/')
def inicio():
    return "Servidor IoT activo", 200

# Ruta para recibir datos JSON desde la ESP32
@app.route('/datos', methods=['POST'])
def recibir_datos():
    data = request.get_json()
    print(" Datos recibidos:", data)
    return jsonify({"estado": "OK", "mensaje": "Datos recibidos correctamente"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
