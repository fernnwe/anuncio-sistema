from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

COMENTARIOS_PATH = 'comentarios.json'

# Función para leer los comentarios desde el archivo JSON
def leer_comentarios():
    if not os.path.exists(COMENTARIOS_PATH):
        return []  # Si no existe el archivo, devuelve una lista vacía
    with open(COMENTARIOS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

# Función para guardar un nuevo comentario en el archivo JSON
def guardar_comentario(nombre, texto):
    comentarios = leer_comentarios()
    comentarios.insert(0, {"nombre": nombre, "texto": texto})  # Inserta el comentario al principio
    with open(COMENTARIOS_PATH, 'w', encoding='utf-8') as f:
        json.dump(comentarios, f, ensure_ascii=False, indent=2)  # Guarda los comentarios en el archivo

@app.route('/')
def index():
    return render_template('index.html')  # Renderiza la página principal

@app.route('/api/comentarios', methods=['GET', 'POST'])
def comentarios():
    if request.method == 'POST':
        data = request.get_json()  # Obtiene los datos JSON del cuerpo de la solicitud
        nombre = data.get('nombre')
        texto = data.get('texto')
        if nombre and texto:
            guardar_comentario(nombre, texto)  # Guarda el comentario si tiene nombre y texto
            return jsonify({"status": "ok"}), 200
        return jsonify({"error": "Datos incompletos"}), 400  # Retorna error si falta algún dato
    else:
        return jsonify(leer_comentarios())  # Retorna la lista de comentarios

# 🔧 Esto es lo que Render necesita para que tu app funcione:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Obtiene el puerto desde la variable de entorno
    app.run(host='0.0.0.0', port=port)  # Ejecuta la aplicación en el puerto adecuado
