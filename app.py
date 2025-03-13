from flask import Flask, render_template, request, jsonify
from services.mongo_service import MongoService

app = Flask(__name__)
mongo_service = MongoService()

@app.route("/")
def index():
    """Affiche la page principale."""
    return render_template("index.html")

@app.route("/api/get_product", methods=["GET"])
def get_product():
    """Retourne un produit commun OFF & FDC."""
    product = mongo_service.get_next_matching_product()
    return jsonify(product) if product else jsonify({"error": "No matching product found"})

@app.route("/api/merge", methods=["POST"])
def merge_product():
    """Sauvegarde un produit fusionné et passe au suivant."""
    data = request.json
    mongo_service.save_merged_product(data)
    return jsonify({"message": "Merged product saved successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
