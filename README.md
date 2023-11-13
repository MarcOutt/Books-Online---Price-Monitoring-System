# Books Online - Système de Surveillance des Prix

![Python Version](https://img.shields.io/badge/Python-3.7-blue.svg)
![BeautifulSoup Version](https://img.shields.io/badge/BeautifulSoup-4.11-green.svg)
![Requests Version](https://img.shields.io/badge/Requests-2.28.1-orange.svg)

## Table des matières
---------------------

* [Introduction](#introduction)
* [Exigences du système de surveillance des prix](#exigences-du-système-de-surveillance-des-prix)
* [Pré-requis](#pré-requis)
* [Installation](#installation)
* [Utilisation](#utilisation)


## Introduction
----------------

Cette application de Web Scraping est conçue pour extraire des informations à partir d'un site Web de livres en ligne appelé "Books to Scrape".L'application permet de récupérer des informations sur les livres tels que le titre, le prix, la disponibilité, etc., et offre également la possibilité d'enregistrer les données collectées dans un fichier CSV ou de les compresser dans un fichier ZIP.


## Exigences du système de surveillance des prix
-----------------------------------------------

Le projet a été conçu pour satisfaire aux exigences suivantes :

* Extraire les informations d'une page produit spécifique, y compris l'URL, l'UPC, le titre, les prix, la disponibilité, la description, la catégorie, la note de la revue et l'URL de l'image.
* Récupérer les informations de tous les livres d'une catégorie et les enregistrer dans un fichier CSV.
* Extraire les informations de tous les livres de toutes les catégories du site et les enregistrer dans des fichiers CSV distincts pour chaque catégorie.
* Télécharger et enregistrer le fichier image de chaque page produit visitée.

## Pré-requis
-------------

Avant de pouvoir utiliser le projet Books Online, assurez-vous de disposer des éléments suivants :

* Python 3 installé sur votre système : [Téléchargement Python 3](https://www.python.org/downloads/)
* Git installé sur votre système : [Téléchargement Git](https://git-scm.com/book/fr/v2/D%C3%A9marrage-rapide-Installation-de-Git)
* Bibliothèques Python : tkinter, requests, beautifulsoup4 : elles seront installées avec le fichier requirements.txt

## Installation
------------------

1. Téléchargez le projet sur votre répertoire local : 
```
git clone https://github.com/MarcOutt/Books-Online---Price-Monitoring-System.git
```

2. Mettez en place un environnement virtuel :
   * Créez l'environnement virtuel: `python -m venv venv`
   * Activez l'environnement virtuel :
       * Windows : `venv\Scripts\activate.bat`
       * Unix/MacOS : `source venv/bin/activate`

3. Installez les dépendances du projet :

```
pip install -r requirements.txt
```
## Comment exécuter l'application

1. Téléchargez le code source du projet sur votre machine.

2. Assurez-vous que les dépendances requises sont installées comme indiqué ci-dessus.

3. Placez l'image "books_online.png" dans le même répertoire que le code source de l'application. Cette image sera utilisée comme logo pour l'interface graphique.

4. Exécutez le fichier "main.py" pour lancer l'application.

## Utilisation de l'application

Lorsque vous lancez l'application, vous verrez une fenêtre avec un logo et un bouton "Lancer le Web Scraping".

- Cliquez sur le bouton "Lancer le Web Scraping" pour commencer à extraire les informations des livres à partir du site "Books to Scrape". Une barre de progression indiquera l'avancement du processus de scraping.

- Une fois le scraping terminé, une nouvelle fenêtre s'ouvrira avec les informations des livres affichées sous forme de texte.

- Vous aurez également la possibilité d'enregistrer les informations des livres dans un fichier CSV en cliquant sur le bouton "Enregistrer en CSV". Si aucun livre n'a été trouvé lors du scraping, un message d'erreur s'affichera.

- Pour compresser les informations des livres dans un fichier ZIP, cliquez sur le bouton "Enregistrer en ZIP". Encore une fois, si aucun livre n'a été trouvé, un message d'erreur s'affichera.

- Vous pouvez également consulter la console pour afficher les messages et les erreurs pendant l'exécution de l'application.

## Personnalisation

Vous pouvez personnaliser l'application en remplaçant l'image "books_online.png" par un logo de votre choix.

Vous pouvez également modifier le code pour ajouter de nouvelles fonctionnalités, personnaliser l'interface graphique ou étendre les capacités de scraping.
