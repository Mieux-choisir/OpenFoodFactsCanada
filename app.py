# app.py
from flask import Flask, jsonify, request, render_template
from services.mongo_service import MongoService

app = Flask(__name__)
mongo_service = MongoService()

@app.route("/")
def index():
    """Affiche la page principale"""
    return render_template("index.html")

@app.route("/api/products", methods=["GET"])
def get_paginated_products():
    """Retourne les produits paginés pour Datatables.net Server-Side Processing"""
    collection = request.args.get("collection", "fdc_products")  # Collection par défaut
    start = int(request.args.get("start", 0))
    length = int(request.args.get("length", 10))
    search = request.args.get("search[value]", "").strip()
    order_column = int(request.args.get("order[0][column]", 0))
    order_dir = request.args.get("order[0][dir]", "asc")

    result = mongo_service.get_paginated_products(collection, start, length, search, order_column, order_dir)
    return jsonify(result)

@app.route("/api/merge", methods=["POST"])
def merge_product():
    """Sauvegarde le produit sélectionné"""
    merged_product = request.json
    mongo_service.save_merged_product(merged_product)
    return jsonify({"message": "Product merged successfully"}), 201

if __name__ == "__main__":
    app.run(debug=True)
