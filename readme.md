# Complétion BD Open Food Facts avec Food Data Central

## Auteurs


## Description
Ce projet a pour but de créer une base de données d'intégration à partir d'Open Food Facts qui est ensuite complétée avec la base de données Branded de Food Data Central.\
Une fois cette base de données complète, elle pourra servir à compléter Open Food Facts.


## Démarrage
L'ensemble de l'application est démarré à l'aide de Docker Compose. Pour démarrer l'application, exécutez la commande suivante :
```
docker compose up -d --build
```

**Remarque** :\
Actuellement le script python ne semble pas être exécuté lors de l'exécution de la commande Docker Compose, il faut donc faire tourner le script python une fois la commande Docker Compose terminée avec la commande suivante :
```
pip install -r requirements.txt
python3 ./scripts/import.py
```



## Développement

### Démarrage des bases de données

1. Installez Docker
2. Démarrez les bases de données en utilisant la commande suivante :
```
docker compose up -d mongo cassandra 
```


## License
