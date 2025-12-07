import time
import logging
from typing import TYPE_CHECKING

from fake_useragent import UserAgent

from utils.config import ScraperConfig
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException

from selenium import webdriver

if TYPE_CHECKING:
    from utils.config import ScraperConfig

logger = logging.getLogger(__name__)


class Browser:
    def __init__(self, config: ScraperConfig) -> None:
        self.timeout = config.browser.timeout
        self.poll_frequency = config.browser.poll_frequency
        self.retry_attempts = config.behavior.retry_attempts
        self.retry_delay = config.behavior.retry_delay

        options = Options()
        options.add_argument("--headless")
        options.add_argument(f"user-agent={UserAgent().random}")

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, self.timeout, self.poll_frequency)

        logger.info("Браузер инициализированно")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def get(self, url):
        self.driver.get(url)
        return self

    def get_with_retry(self, url: str) -> bool:
        """Открытие страницы с повторными попытками"""

        for attempt in range(1, self.retry_attempts + 1):
            try:
                self.driver.get(url)
                return True
            except WebDriverException as e:
                logger.error(f"Ошибка при загрузке {url} (попытка {attempt}/{self.retry_attempts}): {e}")
                if attempt < self.retry_attempts:
                    logger.info(f"Ждем {self.retry_delay} секунд...")
                    time.sleep(self.retry_delay)

        logger.error(f"Не удалось загрузить {url} после {self.retry_attempts} попыток")
        return False
