from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/api/data', methods=['POST'])
def receive_data():
    try:
        # Читаем JSON из тела POST [web:39][web:40]
        data = request.get_json()S
        
        soil_raw = data.get('soil_raw', 0)
        soil_percent = data.get('soil_percent', 0)
        dark = data.get('dark', False)
        
        # Логируем в консоль (можно в файл/БД)
        print(f"Получено: почва RAW={soil_raw}, %={soil_percent}, темно={dark}")
        
        # Сохраняем в файл (опционально)
        with open('sensors.log', 'a') as f:
            f.write(f"{soil_raw},{soil_percent},{dark}\n")
        
        return jsonify({"status": "OK", "received": data}), 200
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    print("Сервер запущен на http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)  # 0.0.0.0 = доступно из сети [web:39]
