import orjson
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings


class WebsiteConfig(BaseSettings):
    """Конфигурация веб-сайта"""

    base_url: str = Field(default="https://quotes.toscrape.com")
    login_path: str = Field(default="/login")
    url_page: str = Field(default="{}/page/{}/")


class UserConfig(BaseSettings):
    """Конфигурация пользователя"""

    username: str = Field(default="admin")
    password: str = Field(default="admin")


class BehaviorConfig(BaseSettings):
    """Конфигурация поведения скрапера"""

    pages_to_scrape: int = Field(default=5, ge=1, le=10)
    use_random_pages: bool = Field(default=True)
    min_page: int = Field(default=1, ge=1)
    max_page: int = Field(default=10, ge=1)
    wait_timeout: int = Field(default=10, ge=1)
    retry_attempts: int = Field(default=3, ge=0)
    retry_delay: int = Field(default=2, ge=0)


class FilesConfig(BaseSettings):
    """Конфигурация файлов"""

    all_quotes: str = Field(default="output.json")
    quotes_author: str = Field(default="author_quotes.json")
    directory: Path = Field(default=Path("./quotes"))


class BrowserConfig(BaseSettings):
    """Конфигурация браузера"""

    headless: bool = Field(default=True)
    page_load_strategy: str = Field(default="normal")
    window_width: int = Field(default=1920, ge=800)
    window_height: int = Field(default=1080, ge=600)
    timeout: float = Field(default=10.0, ge=0.1)
    poll_frequency: float = Field(default=0.5, ge=0.01)


class ScraperConfig(BaseSettings):
    """Основная конфигурация скрапера"""

    website: WebsiteConfig
    user: UserConfig
    behavior: BehaviorConfig
    files: FilesConfig
    browser: BrowserConfig

    @classmethod
    def load_from_json(cls, json_path: Path):
        """Загрузка конфигурации из JSON файла"""

        path = Path(json_path)

        if not path.exists():
            raise FileNotFoundError(f"Файл конфигурации не найден {json_path}")

        if path.suffix.lower() != '.json':
            raise ValueError(f"Файл должен быть формата json: {path.suffix}")

        json_text = path.read_text(encoding='utf-8')
        config_dict = orjson.loads(json_text)

        return cls.model_construct(
            website=WebsiteConfig.model_construct(**config_dict.get('website', {})),
            user=UserConfig.model_construct(**config_dict.get('user', {})),
            behavior=BehaviorConfig.model_construct(**config_dict.get('behavior', {})),
            files=FilesConfig.model_construct(**config_dict.get('files', {})),
            browser=BrowserConfig.model_construct(**config_dict.get('browser', {}))
        )

    @staticmethod
    def set_all_quotes_path(new_path: str, config_path: Path = Path("config.json")) -> None:
        """Новый путь для файла all_quotes"""

        if not new_path:
            raise ValueError("Имя файла не может быть пустым")

        new_filename = f"{new_path}.json" if not new_path.endswith('.json') else new_path

        config_data = orjson.loads(config_path.read_text(encoding='utf-8'))

        config_data['files']['all_quotes'] = new_filename

        config_path.write_bytes(orjson.dumps(config_data, option=orjson.OPT_INDENT_2))
