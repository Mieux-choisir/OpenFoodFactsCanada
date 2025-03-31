# 📌 Complétion BD Open Food Facts avec Food Data Central

## 🧑‍💻 Auteurs
- Estrella Paoli
- David Dionne-Pelletier
- Zack Dufresne
- Nicolas Halim
- Christian Willy Fosso Teubou

## 📖 Description
Ce projet a pour but de **créer une base de données enrichie à partir d'Open Food Facts**, puis de **compléter les données** avec celles de la base Branded de **Food Data Central**.

Les données sont importées, nettoyées et stockées dans une **base MongoDB**, le tout étant orchestré via **Docker Compose**.

---
## 📃 Documentation

### Fichiers JSON

Ce projet comprend deux fichiers JSON, chacun fournissant des informations sur des datasets différents :
- off_csv_fields_descriptions.json : informations sur le dataset utilisé en format csv d'Open Food Facts
- fdc_fields_descriptions.json : informations sur le dataset utilisé de Food Data Central


Chaque fichier JSON comprend la liste des champs présents dans le dataset et donne les informations suivantes pour chaque champ :
- name : le nom du champ
- schema : le type de données contenu par le champ
- desc : la description des valeurs contenues par le champ
- sources : les sources depuis lesquelles les informations sur le champ ont été obtenues
- comment (optionnel) : un commentaire qui donne des informations supplémentaires quand cela est nécessaire


### Fonctions d'analyse des datasets

Dans le répertoire scripts/analysis il y a plusieurs fichiers servant à l'analyse et à la compréhension des datasets utilisés :
- datasets_analyzer.py : analyse les types des données observés dans chaque champ et quels champs peuvent être vides pour chaque dataset (Open Food Facts csv, Open Food Facts jsonl, Food Data Central)
- fields_informations_describer.py : donne des informations sur les champs du dataset demandé en utilisant les fichiers JSON de documentation des champs
- fields_type_analyzer.py : fonctions utilisées par datasets_analyzer.py

---
## 🚀 Démarrage rapide

L’ensemble de l’application est **démarré via Docker Compose**.

📌 **Lancer l’application** :
```bash
docker compose up -d --build
```
- Cette commande **construit et démarre** les conteneurs Docker.
- Le **script d'import Python** est exécuté après le démarrage de MongoDB.

📌 **Suivre les logs du script d’importation** :
```bash
docker logs -f openfoodfacts-python
```
- Permet de voir la progression du téléchargement et de l'importation des données.

📌 **Se connecter à MongoDB en ligne de commande** :
```bash
docker exec -it openfoodfacts-mongo mongosh
```
- Permet d'ouvrir une **console MongoDB** pour explorer la base de données.

---

## 🛠️ Commandes utiles

📌 **Redémarrer proprement les conteneurs** :
```bash
docker compose down && docker compose up -d --build
```
- Arrête et reconstruit les conteneurs.

📌 **Lister les conteneurs en cours d'exécution** :
```bash
docker ps
```
- Vérifie que **`openfoodfacts-mongo`** et **`openfoodfacts-python`** sont bien lancés.

📌 **Vérifier que les données sont bien importées dans MongoDB** :
```bash
docker exec -it openfoodfacts-mongo mongosh
```
Puis, dans la console **MongoDB** :
```js
show dbs
use openfoodfacts
show collections
db.products.count()
db.products.findOne()
```

### Connexion à MongoDB via MongoDB Compass
Pour se connecter à la base de données avec MongoDB Compass, utilisez la chaîne de connexion suivante :
```
mongodb://localhost:37017/
```

---

## ⚙️ Développement

📌 **Installer les dépendances localement** (en dehors de Docker) :
```bash
pip install -r requirements.txt
```

📌 **Exécuter le script d’import manuellement** (si besoin) :
```bash
python ./scripts/import.py
```

---

## 🧪 Exécuter les tests

### 📌 Installation des dépendances pour les tests
Si ce n'est pas encore fait, assurez-vous d'installer les dépendances requises dans un environnement virtuel Python.

1️⃣ **Créer et activer l’environnement virtuel** :
```bash
# Sous Linux/macOS
python -m venv venv
source venv/bin/activate

# Sous Windows
python -m venv venv
venv\Scripts\activate
```
2️⃣ **Installer les dépendances** :
```bash
pip install -r requirements.txt
```
---

### 🌐 Lancer l’interface Web de fusion des produits

Une fois les données importées, tu peux lancer une **interface utilisateur locale** pour comparer et fusionner 
les produits communs entre Open Food Facts et Food Data Central.

📌 **Lancer l’interface Flask localement** :

```bash
python app.py
```
Cela démarre un serveur Flask à l'adresse :

👉 http://127.0.0.1:5000

---
## ✅ Lancer les tests Pytest

### 📌 Exécuter tous les tests :
```bash
pytest tests/
```
---

## 📜 License

