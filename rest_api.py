from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import pandas as pd

# Charger les données depuis le fichier CSV
DATA = pd.read_csv("index-egalite-fh 3(Données publiques Index Egapro).csv", encoding='ISO-8859-1')

# Nettoyer les noms de colonnes
DATA.columns = DATA.columns.str.strip()

# Créer l'application Flask
app = Flask(__name__)
CORS(app)

# Configuration Swagger
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "API EgaPro"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Servir le fichier Swagger
@app.route('/static/swagger.yaml')
def swagger_yaml():
    with open('swagger.yaml', 'r') as f:
        return f.read()

# Route principale pour vérifier que l'API est en ligne
@app.route('/')
def home():
    return jsonify({"message": "API REST EgaPro est en ligne !"})

# Route pour rechercher une entreprise par SIREN
@app.route('/api/egapro/<siren>', methods=['GET'])
def get_egapro_data(siren):
    result = DATA[DATA['SIREN'].astype(str) == siren]

    if not result.empty:
        entreprise = result.iloc[0]['Raison Sociale']
        region = result.iloc[0]['Région']
        departement = result.iloc[0]['Département']
        try:
            index = float(result.iloc[0]['Note Index'])
        except ValueError:
            index = None

        response = {
            "siren": siren,
            "entreprise": entreprise,
            "region": region,
            "departement": departement,
            "index": index
        }
        return jsonify(response)
    else:
        return jsonify({"error": "SIREN non trouvé"}), 404

# Lancer le serveur Flask
if __name__ == '__main__':
    app.run(debug=True, port=5000)
 