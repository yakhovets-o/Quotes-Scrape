import logging
from typing import TYPE_CHECKING

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException

from utils.config import ScraperConfig
from utils.locators import LocatorsLogin
from utils.errors import ClientError
from .browser import Browser

if TYPE_CHECKING:
    from utils.config import ScraperConfig

logger = logging.getLogger(__name__)


class Client:
    def __init__(self, browser: Browser, config: ScraperConfig) -> None:
        self.browser = browser
        self.driver = browser.driver
        self.wait = browser.wait

        self.main_url = config.website.base_url
        self.username = config.user.username
        self.password = config.user.password
        logger.info(f"Клиент инициализирован")

    def login(self) -> None:
        """Логин на сайте"""

        logger.info("Начало процедуры логина")

        try:
            logger.info("Открываем главную страницу: %s", self.main_url)
            self.browser.get(self.main_url)

            self._fill_login_form()

            logger.info("Логин выполнен успешно")
            self._is_logged_in()
        except TimeoutException as e:
            logger.error("Таймаут при выполнении логина: %s", e)
            raise ClientError(f"Таймаут при выполнении логина: {e}")

        except NoSuchElementException as e:
            logger.error("Элемент не найден при логине: %s", e)
            raise ClientError(f"Элемент не найден: {e}")

        except WebDriverException as e:
            logger.error("Ошибка WebDriver при логине: %s", e)
            raise ClientError(f"Ошибка WebDriver: {e}")

        except Exception as e:
            logger.error("Неожиданная ошибка при логине: %s", e)
            raise ClientError(f"Неожиданная ошибка: {e}")

    def _is_logged_in(self) -> bool:
        """Проверка что пользователь залогинен по наличию ссылки Logout."""
        try:
            logout_elements = self.browser.wait.until(EC.element_to_be_clickable(LocatorsLogin.LOGOUT))
            if logout_elements:
                logger.info(f"Пользователь залогинен")
                return True
            return False
        except TimeoutException as e:
            logger.error("Таймаут при выполнении логина:  %s", e)
            raise ClientError(f"Таймаут при проверке ссылки Logout")

        except WebDriverException as e:
            logger.error("Ошибка WebDriver на странице %s", self.driver.current_url)
            raise ClientError(f"Ошибка загрузки страницы {self.driver.current_url}")

    def _fill_login_form(self) -> None:
        """Заполнение формы логина."""

        logger.info("Ожидание кнопки логина...")
        login_button = self.browser.wait.until(EC.element_to_be_clickable(LocatorsLogin.LOGIN_BUTTON))
        login_button.click()

        logger.info("Заполнение поля username...")
        username_field = self.wait.until(EC.visibility_of_element_located(LocatorsLogin.USERNAME))
        username_field.clear()
        username_field.send_keys(self.username)
        logger.info(f"Введен username: {self.username}")

        logger.info("Заполнение поля password...")
        password_field = self.wait.until(EC.visibility_of_element_located(LocatorsLogin.PASSWORD))
        password_field.clear()
        password_field.send_keys(self.password)
        logger.info("Введен пароль")

        l_button = self.driver.find_element(*LocatorsLogin.SUBMIT)
        l_button.click()
