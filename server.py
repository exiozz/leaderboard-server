from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permet à Roblox d'appeler ton serveur

# Cache manuel des leaderboards
leaderboard_cache = {
    "elo": [],
    "wins": [],
    "donate": []
}

@app.route('/')
def home():
    return "Leaderboard Server is running! Use /api/leaderboard/elo, /api/leaderboard/wins, or /api/leaderboard/donate"

@app.route('/api/leaderboard/<type>')
def get_leaderboard(type):
    if type in leaderboard_cache:
        return jsonify(leaderboard_cache[type])
    return jsonify({"error": "Type invalide"}), 400

@app.route('/api/webhook/update', methods=['POST'])
def update_leaderboard():
    try:
        data = request.json
        if 'type' not in data or 'data' not in data:
            return jsonify({"error": "Format invalide"}), 400
        
        leaderboard_cache[data['type']] = data['data']
        print(f"✅ Mise à jour reçue pour {data['type']} : {len(data['data'])} entrées")
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({"status": "alive"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
