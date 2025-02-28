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
## ✅ Lancer les tests Pytest

### 📌 Exécuter tous les tests :
```bash
pytest tests/
```
---

## 📜 License

