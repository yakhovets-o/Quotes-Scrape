import logging
from random import sample
from typing import TYPE_CHECKING

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, WebDriverException

from utils.config import ScraperConfig
from utils.errors import ParserError, QuoteStorageError
from utils.locators import LocatorsQuotes
from .storage import QuoteStorage
from .browser import Browser

if TYPE_CHECKING:
    from utils.config import ScraperConfig

logger = logging.getLogger(__name__)


class Parser:
    def __init__(self, browser: Browser, storage: QuoteStorage, config: ScraperConfig) -> None:
        self.browser = browser
        self.driver = browser.driver
        self.wait = browser.wait
        self.storage = storage

        self.page_count = config.behavior.pages_to_scrape
        self.total_page = config.behavior.max_page
        self.main_url = config.website.base_url
        self.url_page = config.website.url_page

        logger.info("Парсер инициализирован")

    @staticmethod
    def _parse_single_quote(quote: WebElement) -> dict:
        """Парсинг одной цитаты"""

        try:
            text = quote.find_element(*LocatorsQuotes.TEXT).text
            author = quote.find_element(*LocatorsQuotes.AUTHOR).text
            tags = quote.find_element(*LocatorsQuotes.TAGS).text.replace("Tags: ", "").split(" ")

            return {"quote": text, "author": author, "tags": tags}
        except Exception as e:
            logger.error("Ошибка парсинга цитаты: %s", e)
            raise ParserError(f"Не удалось спарсить цитату  {quote}")

    def parse_random_pages(self, page_count: int = None) -> None:
        """Парсинг рандомных страниц"""

        if page_count is None:
            page_count = self.page_count

        logger.info("Количество страниц для парсинга %d", page_count)
        if page_count > self.total_page:
            logger.warning("Запрошено %d страниц, но доступно только %d."
                           "Будет использовано максимальное количество.",
                           page_count, self.total_page)

            page_count = self.total_page

        if page_count <= 0:
            logger.warning(
                "Количество страниц должно быть положительным числом."
                "Будет использовано максимальное количество страниц %d",
                self.total_page)

            page_count = self.total_page

        quotes_lst = []

        try:
            for page in sample(range(1, self.total_page + 1), page_count):
                self.browser.get_with_retry(self.url_page.format(self.main_url, page))

                quotes = self.wait.until(EC.presence_of_all_elements_located(LocatorsQuotes.QUOTES))
                for quote in quotes:
                    quote_dict = self._parse_single_quote(quote)
                    quotes_lst.append(quote_dict)
        except TimeoutException as e:
            logger.error("Таймаут при парсинге страницы %d: %s", page, e)
            raise ParserError(f"Таймаут при парсинге страницы {page}")

        except WebDriverException as e:
            logger.error("Ошибка WebDriver на странице %d: %s", page, e)
            raise ParserError(f"Ошибка загрузки страницы {page}")

        except Exception as e:
            logger.error("Неизвестная ошибка при парсинге страницы %d: %s", page, e)
            raise ParserError(f"Неизвестная ошибка при парсинге страницы {page}")

        try:
            logger.info("Сохранение %d цитат в хранилище", len(quotes_lst))
            self.storage.save(quotes=quotes_lst)
            logger.info("Парсинг успешно завершен")
        except Exception as e:
            logger.error("Ошибка при сохранении данных: %s", e)
            raise QuoteStorageError(f"Ошибка при сохранении данных: {e}")
