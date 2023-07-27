import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter import ttk


class Interface:
    def __init__(self):
        self.web_scraper = None
        self.root = tk.Tk()
        self.root.title("Application de Web Scraping")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        self.text_area = None

    def set_web_scraper(self, web_scraper):
        self.web_scraper = web_scraper

    def executer_web_scraping(self):
        self.web_scraper.book_scraping()
        self.afficher_informations_livres()  # Appel de la méthode pour afficher les informations des livres

    def afficher_informations_livres(self):
        root = tk.Toplevel()  # Utilisez Toplevel pour afficher une nouvelle fenêtre
        root.title("Informations des Livres")

        # Créez une zone de texte pour afficher les informations des livres
        self.text_area = tk.Text(root, wrap=tk.WORD)
        self.text_area.pack()

        # Ajoutez les informations des livres dans la zone de texte
        for book_info in self.web_scraper.books:
            self.text_area.insert(tk.END, str(book_info) + "\n")

    def save_csv(self):
        if not self.web_scraper.books:
            self.print_message("Il n'y a pas de livre à enregistrer en CSV.")
            return

        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Fichiers CSV", "*.csv")])
        if not filename:
            self.print_message("L'enregistrement en CSV a été annulé.")
            return

        self.web_scraper.save_csv_folder(self.web_scraper.books, filename)
        self.print_message(f"Les livres ont été enregistrés en CSV sous le nom : {filename}.csv")

    def save_zip(self):
        if not self.web_scraper.books:
            self.print_message("Il n'y a pas de livre à zipper.")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP Files", "*.zip")])
        if not filename:
            self.print_message("Le zip a été annulé.")
            return
        if filename:
            self.web_scraper.zip_file(filename)
            self.print_message(f"Les livres ont été enregistrés en CSV sous le nom : {filename}.csv")

    def show_interface(self):
        ttk.Style().theme_use('clam')

        # Ajoute un fond blanc à la fenêtre principale
        self.root.configure(bg="white")

        # Charge une image/logo (assurez-vous d'avoir l'image dans le même répertoire)
        logo_image = tk.PhotoImage(file="books_online.png")

        # Diminue la taille du logo sans rogner l'image (ici, on divise par 2)
        logo_image = logo_image.subsample(2)

        # Crée un Label pour afficher l'image du logo
        logo_label = tk.Label(self.root, image=logo_image, bg="white")
        logo_label.pack(padx=20, pady=20)

        label = tk.Label(self.root,
                         text="Logiciel de surveillance des Prix",
                         bg="white",
                         font=("Times New Roman", 22, 'bold'))
        label.pack(padx=20, pady=20)

        btn_scraping = tk.Button(self.root,
                                 text="Lancer le Web Scraping",
                                 font=("Times New Roman", 16, 'bold'),
                                 bg='#4AA3A2',
                                 fg='white',
                                 activebackground="#4A919E",
                                 width=40,
                                 command=self.executer_web_scraping)
        btn_scraping.pack(padx=10, pady=10)

        # Créez une barre de téléchargement (progress bar)
        self.progress_bar = ttk.Progressbar(self.root,
                                            orient=tk.HORIZONTAL,
                                            length=490,
                                            mode='determinate',
                                            style="Custom.Horizontal.TProgressbar")
        self.progress_bar.pack(pady=10)

        # Appliquer le style personnalisé à la barre de progression
        style = ttk.Style()
        style.configure("Custom.Horizontal.TProgressbar",
                        troughcolor='white',
                        background='#4AA3A2',
                        thickness=50,
                        )

        btn_save_csv = tk.Button(self.root,
                                 text="Enregistrer en CSV",
                                 font=("Times New Roman", 16, 'bold'),
                                 bg='#CE6A6B',
                                 fg='white',
                                 activebackground="#EBACA2",
                                 width=40,
                                 command=self.save_csv)
        btn_save_csv.pack(padx=10, pady=10)

        btn_save_zip = tk.Button(self.root,
                                 text="Enregistrer en ZIP",
                                 font=("Times New Roman", 16, 'bold'),
                                 bg='orange',
                                 fg='white',
                                 activebackground="#F27438",
                                 width=40,
                                 command=self.save_zip)
        btn_save_zip.pack(padx=10, pady=10)

        self.message_label = tk.Label(self.root, text="", fg="red", bg='white')
        self.message_label.pack(pady=5)

        self.root.mainloop()

    def print_message(self, message):
        self.message_label.config(text=message, font=("Times New Roman", 12, 'bold'))

        if self.text_area:
            self.text_area.insert(tk.END, message + "\n")
            self.text_area.see(tk.END)

    # Méthode pour mettre à jour la barre de téléchargement avec le progrès
    def update_progress(self, progress):
        self.progress_bar['value'] = progress
        self.progress_bar.update()
