from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

COMENTARIOS_PATH = 'comentarios.json'

def leer_comentarios():
    if not os.path.exists(COMENTARIOS_PATH):
        return []
    with open(COMENTARIOS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_comentario(nombre, texto):
    comentarios = leer_comentarios()
    comentarios.insert(0, {"nombre": nombre, "texto": texto})
    with open(COMENTARIOS_PATH, 'w', encoding='utf-8') as f:
        json.dump(comentarios, f, ensure_ascii=False, indent=2)

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
            guardar_comentario(nombre, texto)
            return jsonify({"status": "ok"}), 200
        return jsonify({"error": "Datos incompletos"}), 400
    else:
        return jsonify(leer_comentarios())

# 🔧 Esto es lo que Render necesita para que tu app funcione:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
