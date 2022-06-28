<h1>town_db</h1>
<h3>Введение</h3>
Идея, поданая Ильёй Лагода , подключить Flask, настроить формы для работы со списком городов ({страна: [города]}), хранящимся в JSON файле, трансформировалась, в идёю создать базу городов на SQLite3, Flask и с использованием flask_sqlalchemy. В итоге, получился учебный проект, где был получен навык работы с микрофреймворком Flask, с СУБД SQLite3, c  HTML, CSS и JS фреймворком Bootstrap5.

<h3>Установка</h3>
<li>Устанавливаем Python 3 для своей системы, если не установлен.
 Для ОС Windows переходим по ссылке и устанавливаем - <a href="https://www.python.org/downloads/">Python.org</a>.
Для Ubunty/Debian Python должен быть установлен по умолчанию. Проверим в терминале версию: python -v </li>
<li> Установливаем систему управления пакетов pip, если, она не установлена.</li>
<li>Создаём виртуальное окружение с помощью venv, позволяющий создавать изолированные среды для отдельных проектов Python, решая тем самым проблему зависимостей и совместимости приложений разных версий.
В Ubunty/Debian: python3 -m venv /path/to/new/virtual/environment</li>
<li>Устанавливаем из файла зависимостей:
pip install -r requirements.txt</li>



<h3>Используемый материал</h3>
<ul>
<li><a href="https://flask-sqlalchemy.palletsprojects.com/en/2.x/">Flask-SQLAlchemy</a></li>
<li><a href="https://habr.com/ru/post/346306/">Хабр:Мега-Учебник Flask ( издание 2018 ) </a></li>
<li><a href="https://proproprogs.ru/flask">proproprogs.ru</a></li>
<li><a href="https://900913.ru/2021/01/03/example-database-and-python-3-sqlalchemy-orm/">Три примера работы с SQL базой данных в Python (sqlalchemy.orm)</a></li>
<li><a href="https://www.youtube.com/watch?v=lBOq1_blG_8">Flask: подключаем БД, настраиваем SqlAlchemy</a></li>
<li><a href="https://www.youtube.com/watch?v=Y_oyx36AdV0&list=PLlWXhlUMyooZr5R2u2Zwxt6Pw6iwBo5y5&index=1">Cоздание блога на Flask (уроки)</a></li>
</ul>