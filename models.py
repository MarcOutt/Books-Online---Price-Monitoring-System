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


class WebScraper:
    def __init__(self):
        self.main_folder = self.create_main_file()

    def create_main_file(self):
        dossier_books_to_scraps = Path.cwd() / "Books_to_scraps"
        if not Path(dossier_books_to_scraps).exists():
            dossier_books_to_scraps.mkdir()
        return dossier_books_to_scraps

    def zip_file(self):
        filename = "books_to_scraps"
        format = "zip"
        directory = self.main_folder
        shutil.make_archive(filename, format, directory)
        print("Formatage du dossier complété")

    def save_csv_folder(self, books, folder_name):

        csv_files = folder_name + ".csv"
        data_file = self.main_folder / csv_files
        data_file.touch()
        try:
            books_list = books[1]
        except IndexError:
            books_list = books[0]
        header = list(books_list.keys())
        with codecs.open(data_file, 'a', encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=header)
            writer.writeheader()
            for book in books:
                writer.writerow(book)

    def book_scraping(self):
        website = OnlineResource()

        categories = website.extract_url_categories()
        for info in categories:
            print(f"Téléchargement en cours de la catégorie {info[0]}")
            category = Category(info[0], info[1])
            books_url = category.extraire_liste_livres()
            books_info_list = []
            for url in books_url:
                book = Books()
                books_info = website.extract_book_info(url)
                books_info_list.append(books_info)
            self.save_csv_folder(books_info_list, info[0])
            print(f"Téléchargement terminé de la catégorie {info[0]}\n")
        print("Extraction des livres terminée.")


class OnlineResource:
    def extract_url_categories(self):
        """ permet de récupérer les urls des catégories
        Returns:
            rien
        """
        div_container_fluid = SOUP.find("div", class_="container-fluid")
        div_side_categories = div_container_fluid.find("div", class_="side_categories")
        ul_nav = div_side_categories.find("ul", class_="nav")
        ul = ul_nav.find("ul")
        li = ul.find_all("li")

        list_categories_and_urls = []
        for category in li:
            category_list = []
            a = category.find("a")
            category = a.text
            category_clean = category.replace(' ', "")
            category_clean_2 = category_clean.replace('\n', "")
            href = a["href"]
            link = BASE_URL + href
            category_list.append(category_clean_2)
            category_list.append(link)
            list_categories_and_urls.append(category_list)
        return list_categories_and_urls

    def extract_book_info(self, url_livre):
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
        elif self.review_rating == div_col_product_main.find("p", class_="star-rating Two"):
            self.review_rating = "2 étoiles"
        elif self.review_rating == div_col_product_main.find("p", class_="star-rating Three"):
            self.review_rating = "3 étoiles"
        elif self.review_rating == div_col_product_main.find("p", class_="star-rating Four"):
            self.review_rating = "4 étoiles"
        elif self.review_rating == div_col_product_main.find("p", class_="star-rating Five"):
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


class Category:
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


class Books:
    def __init__(self, titre=""):
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
