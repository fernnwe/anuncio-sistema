from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Lista en memoria para guardar los comentarios (temporalmente)
comentarios_en_memoria = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/comentarios', methods=['GET', 'POST'])
def comentarios():
    if request.method == 'POST':
        data = request.get_json()
        nombre = data.get('nombre')
        texto = data.get('texto')
        if nombre and texto:
            comentarios_en_memoria.insert(0, {"nombre": nombre, "texto": texto})
            return jsonify({"status": "ok"}), 200
        return jsonify({"error": "Datos incompletos"}), 400
    else:
        return jsonify(comentarios_en_memoria)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
