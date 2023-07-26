from views import Interface
from models import WebScraper


def main():
    interface = Interface()
    web_scraper_instance = WebScraper(interface)
    interface.set_web_scraper(web_scraper_instance)
    interface.show_interface()


if __name__ == "__main__":
    main()
