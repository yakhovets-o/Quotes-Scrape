from selenium.webdriver.common.by import By


class LocatorsQuotes:
    QUOTES: tuple[str, str] = (By.CLASS_NAME, "quote")
    TEXT: tuple[str, str] = (By.CLASS_NAME, "text")
    AUTHOR: tuple[str, str] = (By.CLASS_NAME, "author")
    TAGS: tuple[str, str] = (By.CLASS_NAME, "tags")


class LocatorsLogin:
    LOGIN_BUTTON: tuple[str, str] = (By.LINK_TEXT, "Login")
    USERNAME: tuple[str, str] = (By.ID, 'username')
    PASSWORD: tuple[str, str] = (By.ID, 'password')
    SUBMIT: tuple[str, str] = (By.XPATH, "//input[@value='Login']")
    LOGOUT: tuple[str, str] = (By.LINK_TEXT, "Logout")
