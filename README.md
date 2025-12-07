# Парсер Quotes to Scrape

Python-скрипт для автоматизации работы с сайтом https://quotes.toscrape.com. Включает авторизацию, сбор цитат с рандомных страниц и поиск по автору.


Структура проекта
```
├── config.json                     # Конфигурационный файл
├── main.py                         # Основной скрипт
├── logger_conf/                    # Конфигурация логгера
│   ├── logger_conf.py
│   └── script.log                  # Файл логов
├── modules/                        # Основные модули
│   ├── browser.py                  # Работа с браузером
│   ├── client.py                   # Клиент 
│   ├── parser.py                   # Парсинг данных
│   └── storage.py                  # Сохранение данных
├── utils/                          # Вспомогательные утилиты
│   ├── config.py                   # Загрузка конфигурации
│   ├── errors.py                   # Пользовательские исключения
│   └── locators.py                 # CSS-локаторы
├── quotes/                         # Выходные данные
│   ├── output.json                 # Все собранные цитаты
│   └── author_quotes.json          # Цитаты конкретного автора
├── requirements.txt                # Зависимости Python
└── README.md                       # Документация
```
---

### Основные возможности
- Сбор данных с пагинированных страниц
- Поиск по автору через CLI с выводом в консоль и файл
- Обработка ошибок с автоматическим восстановлением
- Логирование всех операций в структурированном формате
- Гибкая конфигурация через JSON-файл

---

Установка Linux

* Клонируем проект [***Quotes-Scrape***](https://github.com/yakhovets-o/Quotes-Scrape)
* Установите виртуальное окружение:  ```python -m venv venv```
* Активируйте виртуальное окружение: ```source venv/bin/activate```
* Установите внешние библиотеки, выполнив: ```pip install -r requirements.txt```
---


### Основные команды CLI
* `python main.py`	 - Собрать цитаты со случайных страниц
* `python main.py --pages N` - 	Собрать с N страниц
* `python main.py --author "Имя"` - 	Найти цитаты автора
* `python main.py --output file.json` - 	Переопределяет файл

---

### Пример Логов

```
[2025-12-07 19:49:45] __main__ INFO: Приложение запущено
[2025-12-07 19:49:45] modules.storage INFO: Xранилище инициализированно
[2025-12-07 19:49:49] modules.browser INFO: Браузер инициализированно
[2025-12-07 19:49:49] modules.client INFO: Клиент инициализирован
[2025-12-07 19:49:49] modules.parser INFO: Парсер инициализирован
[2025-12-07 19:49:49] modules.storage INFO: Запись в файл: quotes/author_quotes.json
[2025-12-07 19:49:49] modules.storage INFO: Хранилище цитат автора очищены quotes/author_quotes.json
[2025-12-07 19:49:49] modules.storage INFO: Запись в файл: quotes/author_quotes.json
[2025-12-07 19:49:49] modules.storage INFO: Цитаты автора записыны в файл quotes/author_quotes.json
[2025-12-07 19:49:49] modules.storage INFO: Найдено 9 цитат автора 'J.K. Rowling'
[2025-12-07 19:49:49] modules.parser INFO: Количество страниц для парсинга 1
[2025-12-07 19:49:51] modules.parser INFO: Сохранение 10 цитат в хранилище
[2025-12-07 19:49:51] modules.storage INFO: Новых уникальных цитат не найдено
[2025-12-07 19:49:51] modules.storage INFO: Запись в файл: quotes/output.json
[2025-12-07 19:49:51] modules.storage INFO: Сохранено: 90 цитат
[2025-12-07 19:49:51] modules.parser INFO: Парсинг успешно завершен
```
---

### Пример файла `author_quotes.json`

```
[
  {
    "author": "J.K. Rowling",
    "quote": "“It is our choices, Harry, that show what we truly are, far more than our abilities.”",
    "tags": [
      "abilities",
      "choices"
    ]
  },
  {
    "author": "J.K. Rowling",
    "quote": "“Remember, if the time should come when you have to make a choice between what is right and what is easy, remember what happened to a boy who was good, and kind, and brave, because he strayed across the path of Lord Voldemort. Remember Cedric Diggory.”",
    "tags": [
      "integrity"
    ]
  }

 ```` 
### Пример файла `quotes.json`

```
[
  {
    "author": "Albert Einstein",
    "quote": "“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”",
    "tags": [
      "change",
      "deep-thoughts",
      "thinking",
      "world"
    ]
  },
  {
    "author": "J.K. Rowling",
    "quote": "“It is our choices, Harry, that show what we truly are, far more than our abilities.”",
    "tags": [
      "abilities",
      "choices"
    ]
  }]
```
---

### Логин на сайте 

```python
    client = Client(browser, config)
    client.login()
```

```
[2025-12-07 21:37:14] __main__ INFO: Приложение запущено
[2025-12-07 21:37:14] modules.storage INFO: Xранилище инициализированно
[2025-12-07 21:37:14] modules.browser INFO: Браузер инициализированно
[2025-12-07 21:37:14] modules.client INFO: Клиент инициализирован
[2025-12-07 21:37:14] modules.parser INFO: Парсер инициализирован
[2025-12-07 21:37:14] modules.client INFO: Начало процедуры логина
[2025-12-07 21:37:14] modules.client INFO: Открываем главную страницу: https://quotes.toscrape.com
[2025-12-07 21:37:16] modules.client INFO: Ожидание кнопки логина...
[2025-12-07 21:37:17] modules.client INFO: Заполнение поля username...
[2025-12-07 21:37:17] modules.client INFO: Введен username: admin
[2025-12-07 21:37:17] modules.client INFO: Заполнение поля password...
[2025-12-07 21:37:17] modules.client INFO: Введен пароль
[2025-12-07 21:37:17] modules.client INFO: Логин выполнен успешно
[2025-12-07 21:37:18] modules.client INFO: Пользователь залогинен
```
---

### Сбор данных

```python
    parser = Parser(browser, storage, config)
    parser.parse_random_pages(3)
```
```
[2025-12-07 21:40:22] __main__ INFO: Приложение запущено
[2025-12-07 21:40:22] modules.storage INFO: Xранилище инициализированно
[2025-12-07 21:40:23] modules.browser INFO: Браузер инициализированно
[2025-12-07 21:40:23] modules.client INFO: Клиент инициализирован
[2025-12-07 21:40:23] modules.parser INFO: Парсер инициализирован
[2025-12-07 21:40:23] modules.parser INFO: Количество страниц для парсинга 3
[2025-12-07 21:40:28] modules.parser INFO: Сохранение 30 цитат в хранилище
[2025-12-07 21:40:28] modules.storage INFO: Новых уникальных цитат не найдено
[2025-12-07 21:40:28] modules.storage INFO: Запись в файл: quotes/output.json
[2025-12-07 21:40:28] modules.storage INFO: Сохранено: 90 цитат
[2025-12-07 21:40:28] modules.parser INFO: Парсинг успешно завершен
```

---
 
### Пример команды CLI

```python
python main.py --pages 1
```

```
[2025-12-07 21:44:14] __main__ INFO: Приложение запущено
[2025-12-07 21:44:14] modules.storage INFO: Xранилище инициализированно
[2025-12-07 21:44:15] modules.browser INFO: Браузер инициализированно
[2025-12-07 21:44:15] modules.client INFO: Клиент инициализирован
[2025-12-07 21:44:15] modules.parser INFO: Парсер инициализирован
[2025-12-07 21:44:15] modules.parser INFO: Количество страниц для парсинга 1
[2025-12-07 21:44:17] modules.parser INFO: Сохранение 10 цитат в хранилище
[2025-12-07 21:44:17] modules.storage INFO: Новых уникальных цитат не найдено
[2025-12-07 21:44:17] modules.storage INFO: Запись в файл: quotes/output.json
[2025-12-07 21:44:17] modules.storage INFO: Сохранено: 90 цитат
[2025-12-07 21:44:17] modules.parser INFO: Парсинг успешно завершен
```



