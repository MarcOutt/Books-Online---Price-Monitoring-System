import codecs
import shutil

import requests
from bs4 import BeautifulSoup
import csv
from pathlib import Path

BASE_URL = "http://books.toscrape.com/"
CATALOGUE_URL = "http://books.toscrape.com/catalogue/"
response = requests.get(BASE_URL)
SOUP = BeautifulSoup(response.text, "html.parser")


def zip_dossier():
    filename = "books_to_scraps"
    format = "zip"
    directory = dossier_principal
    shutil.make_archive(filename, format, directory)
    print("Formatage du dossier complété")


def creation_fichier_principal():
    dossier_books_to_scraps = Path.cwd() / "Books_to_scraps"
    if not Path(dossier_books_to_scraps).exists():
        dossier_books_to_scraps.mkdir()
    return dossier_books_to_scraps


def enregistrer_fichier_csv(livres, nom_du_fichier):

    fichier_csv = nom_du_fichier + ".csv"
    data_file = dossier_principal / fichier_csv
    data_file.touch()
    try:
        liste_livres = livres[1]
    except IndexError:
        liste_livres = livres[0]
    header = []
    for key in liste_livres.keys():
        header.append(key)

    with codecs.open(data_file, 'a', encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()
        for livre in livres:
            writer.writerow(livre)


class Ressources_en_ligne:

    def __init__(self):
        pass


    def extraire_url_categories(self):
        """ permet de récupérer les urls des catégories
        Returns:
            rien
        """
        div_container_fluid = SOUP.find("div", class_="container-fluid")
        div_side_categories = div_container_fluid.find("div", class_="side_categories")
        ul_nav = div_side_categories.find("ul", class_="nav")
        ul = ul_nav.find("ul")
        li = ul.find_all("li")
        liste_categories_et_urls = []
        for categorie in li:
            liste_categorie = []
            a = categorie.find("a")
            categorie = a.text
            categorie_nettoye = categorie.replace(' ', "")
            categorie_nettoye_2 = categorie_nettoye.replace('\n', "")
            href = a["href"]
            lien = BASE_URL + href
            liste_categorie.append(categorie_nettoye_2)
            liste_categorie.append(lien)
            liste_categories_et_urls.append(liste_categorie)
        return liste_categories_et_urls


class Categorie:
    def __init__(self, nom, url_categorie):
        self.nom = nom
        self.url = url_categorie
        self.liste_livres_urls = []

    def extraire_liste_livres(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        section_livre = soup.find("section")
        ol_livres = section_livre.find("ol", class_="row")
        li_livres = ol_livres.find_all("li")
        for li in li_livres:
            # récupérer l'url du livre
            div_img_container = li.find("div", class_="image_container")
            livre_li = div_img_container.find("a")
            href = livre_li["href"]

            href_nettoye = href.replace("../../../", "")
            livre_url = CATALOGUE_URL + href_nettoye
            # ajout des éléments dans une liste
            self.liste_livres_urls.append(livre_url)
        li_next = section_livre.find("li", class_="next")
        if li_next is not None:
            a = li_next.find("a")
            href = a["href"]
            u = self.url.split("/")[-1]
            url2 = self.url.replace(u, "")
            self.url = url2 + href
            self.extraire_liste_livres()
        return self.liste_livres_urls


class Livres:
    def __init__(self):
        self.titre = ""
        self.category = ""
        self.image_url = ""
        self.review_rating = ""
        self.product_description = ""
        self.universal_product_code = ""
        self.price_including_tax = ""
        self.price_excluding_tax = ""
        self.number_available = ""
        self.number_review = ""


    def extraire_infos_livre(self, url_livre):
        """ extrait les infos des livres
        Args:
            url_livre : url d'un livre
        Returns:
                livres : la liste des infos des livres
        """
        response = requests.get(url_livre)
        soup = BeautifulSoup(response.text, "html.parser")
        # récupérer le titre
        self.titre = soup.find("h1").text

        # catégorie livre
        ul_breadcrumb = soup.find("ul", class_="breadcrumb")
        ul_breadcrumb_li = ul_breadcrumb.find_all("a")
        self.category = ul_breadcrumb_li[2].text

        # review rating
        div_col_product_main = soup.find("div", class_="col-sm-6 product_main")
        self.review_rating = div_col_product_main.find("p", class_="star-rating")
        if self.review_rating == div_col_product_main.find("p", class_="star-rating One"):
            self.review_rating = "1 étoile"
        if self.review_rating == div_col_product_main.find("p", class_="star-rating Two"):
            self.review_rating = "2 étoiles"
        if self.review_rating == div_col_product_main.find("p", class_="star-rating Three"):
            self.review_rating = "3 étoiles"
        if self.review_rating == div_col_product_main.find("p", class_="star-rating Four"):
            self.review_rating = "4 étoiles"
        if self.review_rating == div_col_product_main.find("p", class_="star-rating Five"):
            self.review_rating = "5 étoiles"

        # description du livre
        article_product_page = soup.find("article", class_="product_page")
        product_description = article_product_page.find("p", recursive=False)
        if product_description:
            self.product_description = article_product_page.find("p", recursive=False).text
        else:
            self.product_description = "non renseignée"
        # url image
        div_item = soup.find("div", class_="item")
        img_item = div_item.find("img")
        img_src = img_item["src"]
        self.img_url = BASE_URL + img_src

        # récupérer infos livre
        product_info = soup.find("table", class_="table table-striped")
        product_info_td = product_info.find_all("td")

        # UPC
        self.universal_product_code = product_info_td[0].text

        # TVA
        self.price_including_tax = product_info_td[3].text

        # HT
        self.price_excluding_tax = product_info_td[2].text

        # disponibilité
        self.number_available = product_info_td[5].text

        # review
        self.number_review = product_info_td[6].text

        infos_livre = {
            "title": self.titre,
            "category": self.category,
            "image_url": self.img_url,
            "review_rating": self.review_rating,
            "product_description": self.product_description,
            "universal_product_code": self.universal_product_code,
            "price_including_tax": self.price_including_tax,
            "price_excluding_tax": self.price_excluding_tax,
            "number_available": self.number_available,
            "number_review": self.number_review
        }
        return infos_livre


def menu_principal():
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

            site = Ressources_en_ligne()

            livre = Livres()
            categories = site.extraire_url_categories()
            for infos in categories:
                print(f"téléchargement en cours de la catégorie {infos[0]}")
                categorie = Categorie(infos[0], infos[1])
                url_livres = categorie.extraire_liste_livres()
                liste_infos_livres = []
                for url in url_livres:
                    infos_livre = livre.extraire_infos_livre(url)
                    liste_infos_livres.append(infos_livre)
                enregistrer_fichier_csv(liste_infos_livres, livre.category)
                print(f"Téléchargement terminé de la catégorie {infos[0]}\n")
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


dossier_principal = creation_fichier_principal()
menu_principal()