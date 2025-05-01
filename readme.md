# 📌 Completing the Open Food Facts database with Food Data Central<br>📌 Complétion BD Open Food Facts avec Food Data Central

## Languages
- [English](#english)
- [Français](#français)


---

---

## English


## 🧑‍💻 Authors
- Estrella Paoli
- David Dionne-Pelletier
- Zack Dufresne
- Nicolas Halim
- Christian Willy Fosso Teubou

## 📖 Description
This project aims to **create an enriched database from Open Food Facts**, then **complete the data** with data from the Branded database of **Food Data Central**.

The data is imported, cleaned and stored in a **MongoDB database**, with everything orchestrated via **Docker Compose**.

---
## 📃 Documentation

### JSON files

This project includes two JSON files, each providing information on different datasets:
- *off_csv_fields_descriptions.json*: information on the dataset used in csv format from Open Food Facts
- *fdc_fields_descriptions.json*: information on the dataset used from Food Data Central


Each JSON file includes a list of the fields present in the dataset and gives the following information for each field:
- *name*: the name of the field
- *schema*: the type of data contained by the field
- *desc*: the description of the values contained by the field
- *sources*: the sources from which the information on the field was obtained
- *comment* (optional): a comment giving additional information when necessary

### Datasets analysis functions

In the *scripts/analysis* directory there are several files for analyzing and understanding the datasets used:
- *datasets_analyzer.py*: analyzes the data types observed in each field and which fields may be empty for each dataset (Open Food Facts csv, Open Food Facts jsonl, Food Data Central)
- *fields_information_describer.py*: provides information on the fields in the requested dataset, using the JSON field documentation files
- *fields_type_analyzer.py*: functions used by datasets_analyzer.py

---
## 🚀 Quick start

The entire app is **started via Docker Compose**.

📌 **Launch the app** :
```bash
docker compose up -d --build
```
- This command **builds and starts** the Docker containers.
- The **import Python scripts** is executed after the MongoDB start.

📌 **Monitor import script logs** :
```bash
docker logs -f openfoodfacts-python
```
- Allows to view the progress of data download and import.

📌 **Connect to MongoDB from the command line** :
```bash
docker exec -it openfoodfacts-mongo mongosh
```
- Opens a **MongoDB console** to explore the database.

---

## 🛠️ Useful commands

📌 **Properly restart containers** :
```bash
docker compose down && docker compose up -d --build
```
- Stops and rebuilds containers.

📌 **List currently running containers** :
```bash
docker ps
```
- Checks that **`openfoodfacts-mongo`** and **`openfoodfacts-python`** are running correctly.

📌 **Check that the data is imported into MongoDB** :
```bash
docker exec -it openfoodfacts-mongo mongosh
```
Then in the **MongoDB** console:
```bash
show dbs
use openfoodfacts
show collections
db.products.count()
db.products.findOne()
```

### Connect to MongoDB via MongoDB Compass
To connect to the database with MongoDB Compass, use the following connection string:
```
mongodb://localhost:37017/
```

---

## ⚙️ Development

📌 **Install dependencies locally** (outside Docker) :
```bash
pip install -r requirements.txt
```

📌 **Run import script manually** (if required) :
```bash
python ./scripts/collection_import.py
```

---

## 🧪 Run tests

### 📌 Installing test dependencies
If you haven't already done so, make sure you install the required dependencies in a Python virtual environment.

1️⃣ **Create and activate the virtual environment** :
```bash
# On Linux/macOS
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```
2️⃣ **Install dependencies** :
```bash
pip install -r requirements.txt
```

---
## ✅ Run Pytest tests

### 📌 Run all the tests :
```bash
pytest tests/
```
---

## 📜 License

---

---

## Français


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
- *off_csv_fields_descriptions.json* : informations sur le dataset utilisé en format csv d'Open Food Facts
- *fdc_fields_descriptions.json* : informations sur le dataset utilisé de Food Data Central


Chaque fichier JSON comprend la liste des champs présents dans le dataset et donne les informations suivantes pour chaque champ :
- *name* : le nom du champ
- *schema* : le type de données contenu par le champ
- *desc* : la description des valeurs contenues par le champ
- *sources* : les sources depuis lesquelles les informations sur le champ ont été obtenues
- *comment* (optionnel) : un commentaire qui donne des informations supplémentaires quand cela est nécessaire


### Fonctions d'analyse des datasets

Dans le répertoire *scripts/analysis*, il y a plusieurs fichiers servant à l'analyse et à la compréhension des datasets utilisés :
- *datasets_analyzer.py* : analyse les types des données observés dans chaque champ et quels champs peuvent être vides pour chaque dataset (Open Food Facts csv, Open Food Facts jsonl, Food Data Central)
- *fields_information_describer.py* : donne des informations sur les champs du dataset demandé en utilisant les fichiers JSON de documentation des champs
- *fields_type_analyzer.py* : fonctions utilisées par datasets_analyzer.py

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
```bash
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
python ./scripts/collection_import.py
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
## ✅ Lancer les tests Pytest

### 📌 Exécuter tous les tests :
```bash
pytest tests/
```
---

## 📜 Licence

