# Ynov Basket

## I. Présentation
L'objectif du projet est de développer un site python-flask afin d'afficher les données de l'API [balldontlie](https://www.balldontlie.io/home.html#introduction)

## II. Prérequis
(installer python)
### A. Installer les packages python nécessaire

```
pip install -r requirements.txt
```
### B. Installer et configurer le service MySQL

L'installation et la configuration sont très bien expliqué dans ce [tutoriel](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04) (Linux) et pour [Windows](https://www.dataquest.io/blog/install-mysql-windows/).

### C. Création d'un fichier "credentials.txt"

Ce fichier est à mettre à la racine du projet, il sera utilisé pour établir la connexion entre le site web et la DB MySQL.  

Le fichier sera composé de 4 lignes :  
 - 1er ligne : le nom de la database utilisé
 - 2ème ligne : le nom d'utilisateur à utiliser
 - 3ème ligne : le mot de passe à utiliser
 - 4ème ligne : l'IP d'accès à la DB ('localhost' si la DB est sur la même machine que le site)

### D. Remplissage de la DB
Executez le script "setup_database.py"
```
python3 setup_database.py
```
Cela prendra un certains temps du au nombre de données, mais aussi aux "sleep" présent dans le script pour éviter de se faire bloquer par l'API.

## III. Lancement

Une fois tous les prérequis effectué, il suffit d'executez le script "app.py"

```
python3 app.py
```