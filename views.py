import tkinter as tk


class Interface:
    def __init__(self, web_scraper):
        self.web_scraper = web_scraper

    def executer_web_scraping(self):
        self.web_scraper.book_scraping()

    def show_interface(self):
        root = tk.Tk()
        root.title("Application de Web Scraping")
        root.geometry("600x400")

        # Ajoute un fond blanc à la fenêtre principale
        root.configure(bg="white")

        # Charge une image/logo (assurez-vous d'avoir l'image dans le même répertoire)
        logo_image = tk.PhotoImage(file="books_online.png")

        # Diminue la taille du logo sans rogner l'image (ici, on divise par 2)
        logo_image = logo_image.subsample(2)

        # Crée un Label pour afficher l'image du logo
        logo_label = tk.Label(root, image=logo_image, bg="white")
        logo_label.pack(padx=20, pady=20)

        label = tk.Label(root,
                         text="Logiciel de surveillance des Prix pour le site Books to Scrape",
                         bg="white",
                         font=("Helvetica", 12))
        label.pack(padx=20, pady=20)

        btn_scraping = tk.Button(root,
                                 text="Lancer le Web Scraping",
                                 bg='blue',
                                 activebackground="red",
                                 command=self.executer_web_scraping)
        btn_scraping.pack(padx=10, pady=10)

        root.mainloop()

