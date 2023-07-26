from views import Interface
from models import WebScraper


def main():
    web_scraper = WebScraper()
    interface = Interface(web_scraper)
    interface.show_interface()


if __name__ == "__main__":
    main()