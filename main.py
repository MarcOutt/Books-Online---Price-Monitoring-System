##########################################################
#                                                        #
#                      BOOKS ONLINE                      #
#                                                        #
##########################################################
import shutil

import requests
from bs4 import BeautifulSoup
import csv
from pathlib import Path

BASE_URL = "http://books.toscrape.com/"
CATALOGUE_URL = "http://books.toscrape.com/catalogue/"


def nettoyer_text(texte):
    """ Permet d'interpreter le symbole de la livre'

    Args:
        texte : texte à nettoyer

    Returns:
        str : texte nettoyé

    """
    return texte.replace("Â£", "£")


def nettoyer_url(url):
    """ Permet de supprimer les points et les slashs en trop

    Args:
        url : url récupérée sur le site

    Returns:
        str : url nettoyée
    """
    return url.replace("../../../", "")


def creation_fichier_principal():
    dossier_books_to_scraps = Path.cwd() / "Books_to_scraps"
    if not Path(dossier_books_to_scraps).exists():
        dossier_books_to_scraps.mkdir()
    return dossier_books_to_scraps


def zip_dossier():
    filename = "books_to_scraps"
    format = "zip"
    directory = dossier_principal
    shutil.make_archive(filename, format, directory)
    print("Formatage du dossier complété")


def initialisation_bs(url_site):
    """ Initialisation de beautifulSoup

    Args:
        url_site : url_site

    Returns :
            soup : initialisation de bs4

    """
    response = requests.get(url_site)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup



def extraire_liste_livres(url_categorie, categorie):
    """ extrait la liste des livres

    Args:
        url_categorie : url des catégories
        categorie: nom de la catégorie

    Returns:
        liste : toute la liste et les infos des livres d'une catégorie

    """
    soup = initialisation_bs(url_categorie)
    section_livre = soup.find("section")
    ol_livres = section_livre.find("ol", class_="row")
    li_livres = ol_livres.find_all("li")
    liste = []
    dossier_categorie = dossier_principal / categorie
    if not Path(dossier_categorie).exists():
        dossier_categorie.mkdir()

    for li in li_livres:
        # récupérer l'url du livre
        div_img_container = li.find("div", class_="image_container")
        livre_li = div_img_container.find("a")
        href = livre_li["href"]
        href_nettoye = nettoyer_url(href)
        livre_url = CATALOGUE_URL + href_nettoye

        # récupérer les infos du livre
        infos_livre = extraire_infos_livre(livre_url, dossier_categorie)

        # ajout des éléments dans une liste
        liste.append({"infos_livre": infos_livre})
    return liste




def extraire_url_categories(url):
    """ permet de récupérer les urls des catégories

    Args:
        url: url accueil du site

    Returns:
        rien
    """
    soup = initialisation_bs(url)
    div_container_fluid = soup.find("div", class_="container-fluid")
    div_side_categories = div_container_fluid.find("div", class_="side_categories")
    ul_nav = div_side_categories.find("ul", class_="nav")
    ul = ul_nav.find("ul")
    li = ul.find_all("li")

    for categorie in li:
        a = categorie.find("a")
        categorie = a.text
        categorie_nettoye = categorie.replace(' ', "")
        categorie_nettoye_2 = categorie_nettoye.replace('\n', "")
        href = a["href"]
        lien = BASE_URL + href
        print("Téléchargement en cours de la catégorie: " + categorie_nettoye_2)
        categorie_scraper = scrape_page(lien, liste, categorie_nettoye_2)
    print("Téléchargement terminé")


def menu_principal():
    """ choix pour lancer les programmes

    Returns:
            rien
    """
    print(""" 

            SYSTEME DE SURVEILLANCE DES PRIX

                        MENU

        1 - EXTRAIRE LES LIVRES PAR CATEGORIE
        2 - CREER UN DOSSIER ZIP DE L'EXTRACTION
        3 - QUITTER L'APPLICATION

        """)

    user = input("Veuillez faire votre choix: ")
    try:
        user_int = int(user)
        if user_int == 1:
            extraire_url_categories(BASE_URL)
            menu_principal()
        elif user_int == 2:
            zip_dossier()
            menu_principal()
        elif user_int == 3:
            print("Au revoir")
            exit()
        else:
            print("Veuillez entrer un nombre entre 1 et 3")
    except ValueError:
        print("Veuillez mettre un nombre entre 1 et 3")


liste = []
dossier_principal = creation_fichier_principal()
menu_principal()
