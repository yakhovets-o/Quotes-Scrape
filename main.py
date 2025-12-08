import click
import logging.config
from logger_conf.logger_conf import get_logg_conf
from pathlib import Path


from modules.storage import QuoteStorage
from modules.browser import Browser
from modules.client import Client
from modules.parser import Parser
from utils.config import ScraperConfig


def setup_logging():
    """Настройка логов"""

    logging.config.dictConfig(get_logg_conf())


def load_config():
    """Загрузка конфига"""

    config_path = Path(__file__).parent / "config.json"
    return ScraperConfig.load_from_json(config_path)


@click.command()
@click.option('--pages', '-p', type=int, help='Количество страниц для парсинга')
@click.option('--output', '-o', type=click.Path(), help='Путь к выходному файлу')
@click.option('--author', '-a', type=str, help='Поиск цитат конкретного автора')
def main(pages, output, author):
    setup_logging()
    logger = logging.getLogger(__name__)
    config = load_config()

    logger.info("Приложение запущено")

    if output:
        config.set_all_quotes_path(output)
        logger.info(f"Выходной файл изменен на: {output}")
        return

    storage = QuoteStorage(config)
    browser = Browser(config)
    client = Client(browser, config)
    parser = Parser(browser, storage, config)


    if author:
        storage.get_quotes_by_author(author=author)
    else:
        if pages:
            parser.parse_random_pages(page_count=pages)
        else:
            logger.info(f"Парсинг страниц по умолчанию")
            parser.parse_random_pages()

if __name__ == '__main__':
    main()
