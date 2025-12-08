import orjson
import logging
from typing import TYPE_CHECKING

from utils.errors import QuoteStorageError
from utils.config import ScraperConfig

if TYPE_CHECKING:
    from src.utils.config import ScraperConfig


logger = logging.getLogger(__name__)


class QuoteStorage:
    def __init__(self, config: ScraperConfig) -> None:
        self.directory = config.files.directory
        self.directory.mkdir(exist_ok=True, parents=True)

        self.path_all_quotes = self.directory / config.files.all_quotes
        self.path_quotes_author = self.directory / config.files.quotes_author
        logger.info("Xранилище инициализированно")
        self._init_storage()

    def _init_storage(self) -> None:
        """Созадание json файла с пустым списком цитат, если файл не существует"""
        try:
            if not self.path_all_quotes.exists():
                self._write_quotes()
        except Exception as e:
            logger.error("Ошибка при инициализации хранилища: %s", e)
            raise QuoteStorageError(f"Не удалось инициализировать хранилище: {e}") from e

    def _init_storage_quotes_by_author(self) -> None:
        """Создание json файла с пустным списком цитат автора"""

        self._write_quotes(path_quotes_author=True)

    def _write_quotes(self, quotes=None, path_quotes_author=False) -> None:
        """Запись цитат в файл или очистка файла если ничего не передать
        запись цитат в файл конкретного автора если path_quotes_author True
        """

        path = self.path_all_quotes if not path_quotes_author else self.path_quotes_author
        quotes = quotes if quotes else []

        try:
            path.write_bytes(orjson.dumps(quotes, option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS))
            logger.info("Запись в файл: %s", path)

        except PermissionError as e:
            logger.error("Нет прав на запись в файл %s: %s", path, e)
            raise QuoteStorageError(f"Нет прав на запись: {path}") from e

        except orjson.JSONEncodeError as e:
            logger.error("Ошибка сериализации JSON: %s", e)
            raise QuoteStorageError(f"Ошибка формата данных: {e}") from e

        except Exception as e:
            logger.error("Неизвестная ошибка при записи в файл %s: %s", path, e)
            raise QuoteStorageError(f"Ошибка записи: {e}") from e

    def _read_quotes(self) -> list:
        """Загрузка  цитат"""

        try:
            return orjson.loads(self.path_all_quotes.read_bytes())
        except orjson.JSONDecodeError as e:
            logger.error("Файл поврежден (невалидный JSON): %s", self.path_all_quotes)
            raise QuoteStorageError(f"Файл поврежден: {self.path_all_quotes}") from e

    def _get_unique_quotes(self, quotes: list) -> list:
        """Получение только уникальных цитат"""

        try:
            all_quotes = self._read_quotes()
            quote_text = {quote.get("quote") for quote in all_quotes}
            new_quotes = []

            for quote in quotes:
                if quote.get("quote") not in quote_text:
                    new_quotes.append(quote)
            if new_quotes:
                logger.info(
                    "Найдено %d уникальных цитат из %d переданных",
                    len(new_quotes),
                    len(quotes)
                )
            else:
                logger.info("Новых уникальных цитат не найдено")

            all_quotes.extend(new_quotes)
            return all_quotes
        except Exception as e:
            logger.error("Ошибка при фильтрации уникальных цитат: %s", e)
            raise QuoteStorageError(f"Ошибка обработки цитат: {e}") from e

    def save(self, quotes: list) -> None:
        """Сохранение цитат"""

        if not isinstance(quotes, list):
            logger.error("Передан не список цитат: %s", type(quotes))
            raise ValueError("quotes должен быть списком")

        if not quotes:
            logger.info("Пустой список цитат, сохранение пропущено")
            return

        unique_quotes = self._get_unique_quotes(quotes=quotes)
        self._write_quotes(quotes=unique_quotes)
        logger.info(
            "Сохранено: %d цитат",
            len(unique_quotes)
        )

    def clear(self) -> None:
        """Очистка файла цитат"""

        self._write_quotes()
        logger.info("Файл цитат очищен: %s", self.path_all_quotes)

    def get_quotes_by_author(self, author: str) -> str:
        """Поиск цитат по имени автора"""

        self._init_storage_quotes_by_author()
        logger.info("Хранилище цитат автора очищены %s", self.path_quotes_author)

        if author is None or not isinstance(author, str):
            logger.warning("Передано некорректное имя автора: %s", author)
            return "Некорректное имя автора"

        if not author.strip():
            logger.warning("Передана пустая строка или пробелы вместо имени автора")
            return "Имя автора не может быть пустым"

        try:
            quotes_author = list(filter(lambda q: q.get("author") == author, self._read_quotes()))
            if not quotes_author:
                logger.info("Цитаты автора '%s' не найдены", author)
                return f"Цитаты автора '{author}' не найдены"

            self._write_quotes(quotes=quotes_author, path_quotes_author=True)
            logger.info("Цитаты автора записыны в файл %s", self.path_quotes_author)
            result_lines = []

            for i, quote in enumerate(quotes_author, 1):
                quote_text = quote.get("quote", "")
                if quote_text:
                    result_lines.append(f"{i}. {quote_text}")
            logger.info("Найдено %d цитат автора '%s'", len(quotes_author), author)
            return "\n".join(result_lines)

        except QuoteStorageError as e:
            logger.error("Ошибка при поиске цитат автора '%s': %s", author, e)
            return f"Ошибка при поиске цитат: {e}"
