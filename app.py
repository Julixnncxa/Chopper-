from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# CORS permite que Botpress (que está en la web) hable con tu PC (que es local)
CORS(app) 

# --- INVENTARIO DE CHOPPER ---
inventario_juegos = {
    "elden ring": {"stock": 5, "precio": 59.99, "genero": "RPG"},
    "zelda": {"stock": 2, "precio": 69.99, "genero": "Aventura"},
    "mario kart 8": {"stock": 10, "precio": 49.99, "genero": "Carreras"},
    "fifa 24": {"stock": 0, "precio": 30.00, "genero": "Deportes"},
    "spiderman 2": {"stock": 3, "precio": 69.99, "genero": "Acción"}
}

@app.route('/chopper/stock', methods=['POST'])
def gestionar_inventario():
    try:
        data = request.json
        # Verificamos que Botpress envíe el campo 'juego'
        if not data or 'juego' not in data:
            return jsonify({"respuesta_chopper": "¡Oh! Olvidé qué juego estábamos buscando... ¿podrías repetirlo, por favor? 🦌"}), 400

        juego_cliente = data.get("juego").lower().strip()
        
        if juego_cliente in inventario_juegos:
            info = inventario_juegos[juego_cliente]
            stock = info["stock"]
            precio = info["precio"]
            
            if stock > 0:
                msg = f"¡Excelente elección! 🦌✨ He revisado mis registros y tenemos {stock} unidades de {juego_cliente.title()}. ¡El precio es de ${precio}! ¿Te gustaría que te ayude con la compra?"
            else:
                msg = f"¡Oh no! 😰 Mis disculpas, pero el stock de {juego_cliente.title()} se ha agotado. ¡Parece que voló muy rápido! ¿Quieres que busque algo similar por ti?"
            
            return jsonify({
                "success": True,
                "respuesta_chopper": msg,
                "disponible": stock > 0
            })
        else:
            return jsonify({
                "success": False,
                "respuesta_chopper": f"¡Gomen nasai! 🦌 No encuentro '{juego_cliente}' en mi bitácora. ¿Estás seguro de que se escribe así, gran jugador?"
            })
            
    except Exception as e:
        return jsonify({"error": str(e), "respuesta_chopper": "¡Aaaah! Se me cayó el estetoscopio... algo salió mal en mi sistema. 🦌🚑"}), 500

@app.route('/', methods=['GET'])
def home():
    return "¡El consultorio de Chopper está abierto! Servidor funcionando. 🦌🎮"

if __name__ == '__main__':
    # Importante: host='0.0.0.0' permite conexiones externas
    app.run(host='0.0.0.0', port=5000, debug=True)