web-lib
====
Тестовое web-приложение по управлению электронной библиотекой.

Установка зависимостей:
```
pip install -r requirements.txt
```

Создание таблиц в БД:
```python
>>> from web-lib.database import init_db
>>> init_db()
```
или
```
$ sqlite3 sqlite.db < init.sql
```

Наполнение таблиц начальными данными:
```
$ sqlite3 sqlite.db < data.sql
```

Увы, не знаком с docker. А познакомиться нужно время.
посчитал, что sqlite будет проще использовать в данном решении. 
