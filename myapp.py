from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired,  Length, Regexp
from config import Configuration


from math import ceil

app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
print(f"app.config['SQLALCHEMY_DATABASE_URI'] = {app.config['SQLALCHEMY_DATABASE_URI']} ",
      f"app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = {app.config['SQLALCHEMY_TRACK_MODIFICATIONS']} ",
      f"app.config['DEBUG'] = {app.config['DEBUG']}",
      f"app.config['SECRET_KEY'] = {app.config['SECRET_KEY']}",
      sep='\n')

# для переключения меню
menu = [{'name': "Главная", 'url': 'index'},
        {'name': "Найти", 'url': 'myfind'},
        {'name': "Города", 'url': 'catalog_city'},
        {'name': "Страны", 'url': 'catalog_country'}]


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<country {self.id} - {self.name}>"


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    town = db.Column(db.String(100), unique=True, nullable=True)
    popul = db.Column(db.Integer, unique=True, nullable=True)

    def __init__(self, town, popul, country_id):
        self.town = town
        self.popul = popul
        self.country_id = country_id

    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    pr = db.relationship('Country', backref=db.backref('City', lazy='dynamic'))

    def __repr__(self):
        return f"<city {self.id}>"


class CountryForm(FlaskForm):
    """
    Валидаторы:
    DataRequired() - проверяет, заполнил ли пользователь поле?
    Length() - проверяет количество введённых символов от min до max
    Regexp() - проверяет поле с помощью регулярок
    """
    m = ["Поле не заполнено!", f"Поле может содержать от 3 до 50 символов.", " Разрешенные символы - 'А-Я' и 'а-я'"]
    name = StringField('Страна:', validators=[DataRequired(message=m[0]),
                                            Length(min=3, max=50, message=m[1]),
                                            Regexp(r'[а-яА-ЯЁё]', flags=0, message=m[2])])
    submit = SubmitField('Добавить')



class CityForm(FlaskForm):
    m = ["Поле не заполнено!", "Поле может содержать от 3 до 50 символов.", " Разрешенные символы - 'А-Я' и 'а-я'",
         "Поле может содержать от 1 до 5 символов."," Разрешенные символы - '1-9' и '0'"]
    name = StringField('Город:', validators=[DataRequired(message=m[0]),
                                            Length(min=3, max=50, message=m[1]),
                                            Regexp(r'[а-яА-ЯЁё]', flags=0, message=m[2])])
    popul = StringField('Население, тыс.:', validators=[DataRequired(message=m[0]),
                                            Length(min=1, max=5, message=m[3]),
                                            Regexp(r'[1-9]', flags=0, message=m[4])])
    cntry = StringField('Страна:', validators=[DataRequired(message=m[0]),
                                             Length(min=3, max=50, message=m[1]),
                                             Regexp(r'[а-яА-ЯЁё]', flags=0, message=m[2])])
    submit = SubmitField('Добавить')

class FindCityForm(FlaskForm):
    """
    для страницы поиска поиска
    """
    m = ["Поле не заполнено!", f"Поле может содержать от 3 до 50 символов.", " Разрешенные символы - 'А-Я' и 'а-я'"]

    name = StringField('Город:', validators=[DataRequired(message=m[0]),
                                              Length(min=3, max=50, message=m[1]),
                                              Regexp(r'[а-яА-ЯЁё]', flags=0, message=m[2])])
    submit = SubmitField('Найти')

#создать базу с нуля
#db.create_all()


@app.route("/", methods=['GET'])
@app.route("/index", methods=['GET'])
def index():
    res = []
    col = 0
    try:
        res = db.session.query(Country, City).join(Country, Country.id == City.country_id).order_by(Country.name).all()
        col = ceil(len(res) / 4)
    except:
        flash("Ошибка доступа к БД.")
    return render_template("index.html",
                           title="Главная",
                           tab_all=res,
                           col=col,
                           menu=menu)


@app.route("/catalog", methods=['GET', 'POST'])
def catalog_country():
    """
    Функция отправляет в браузер, форму для ввода наименований стран и ответ на запрос от БД (вывод списка стран).
    Создаёт объект form класса CountryForm. Метод form.validate_on_submit() выполняет всю обработку формы.

    Когда браузер отправляет запрос GET для получения веб-страницы с формой, этот метод возвращает False,
    поэтому в этом случае функция пропускает оператор if и переходит к отображению шаблона в последней строке функции.
    В случае исключения откат БД к исходному состоянию при помощи метода rollback()
    :return:
    """
    form = CountryForm()
    col = 0
    try:
        res = Country.query.order_by(Country.name).all()
        col = ceil(len(res) / 3)
    except:
        res = []
        flash("Ошибка доступа к БД.")
    if form.validate_on_submit():
        try:
            text = request.form['name'].capitalize()
            if Country.query.filter_by(name=text).first()==None:
                db.session.add(Country(text))
                db.session.commit()
                flash(f" Добавлена запись - {text}")
            else:
                flash(f" Запись '{text}' существует!")
        except:
            db.session.rollback()
            flash("Ошибка записи в БД")
        return redirect(url_for('add_country'))
    return render_template("catalog.html", title="Страны",
                           country_all=res,
                           col=col,
                           menu=menu,
                           form=form)


@app.route("/addcountry", methods=['GET', 'POST'])
def add_country():
    return redirect(url_for('catalog_country'))


@app.route("/catalogcity", methods=['GET', 'POST'])
def catalog_city():
    """
    Функция отправляет в браузер, форму для ввода наименования города и ответ на запрос от БД (вывод списка городовб
    населения).
    Создаёт объект form класса CityForm. Метод form.validate_on_submit() выполняет всю обработку формы.

    Когда браузер отправляет запрос GET для получения веб-страницы с формой, этот метод возвращает False,
    поэтому в этом случае функция пропускает оператор if и переходит к отображению шаблона в последней строке функции.
    Когда браузер отправляет запрос POST в результате нажатия пользователем кнопки submit, form.validate_on_submit()
    собирает все данные, запускает все валидаторы, прикрепленные к полям, и если все в порядке, вернет True

    В случае исключения откат БД к исходному состоянию при помощи метода rollback()
    Используется запрос Country.query.order_by(Country.name).all(), для определения id страны, т.к. форма выводит
    название страны.
    :return:
    """
    form = CityForm()
    col = 0
    try:
        res = City.query.order_by(City.town).all()
        col = ceil(len(res) / 4)
    except:
        res = []
        flash("Ошибка доступа к БД.")
    #country_all = Country.query.order_by(Country.name).all()
    country_id = 0
    if form.validate_on_submit():
        try:
            name = request.form['name'].capitalize()
            popul = request.form['popul']
            cntry = request.form['cntry'].capitalize()
            what_country = Country.query.filter_by(name=cntry).first()
            #Проверка существования страны, в таблице Country
            if what_country == None:
                flash(f"Страны '{cntry}' нет в базе!")
            else:
                db.session.add(City(name, popul, what_country.id))
                db.session.commit()
                flash(f" Добавлена запись - {form.name.data}")
        except:
            db.session.rollback()
            flash("Ошибка записи в БД")
        return redirect(url_for('add_city'))
    return render_template("catalogcity.html", title="Города",
                           city_all=res,
                           col=col,
                           form=form,
                           menu=menu)


@app.route("/addcity", methods=['GET', 'POST'])
def add_city():
    return redirect(url_for('catalog_city'))

@app.route("/find", methods=['GET', 'POST'])
def myfind():
    form = FindCityForm()
    q = []
    q_1_mill = City.query.filter(City.popul < 1000).order_by(City.popul).all()
    if form.validate_on_submit():
        try:
            name = request.form['name'].capitalize()
            q = City.query.filter(City.town == name).all()
            if len(q) == 0:
                flash(f" Город {name} отсутствует в базе!")
            else:
                #print(q[0].town, q[0].popul, q[0].pr.name )
                return render_template("find.html", title="Найти", form=form, q=q, menu=menu, q_1_mill=q_1_mill)
        except:
            flash(" Ошибка доступа к БД")
        return redirect(url_for('find_city'))
    #print(q[0].town, q[0].popul, q[0].pr.name)
    return render_template("find.html",
                           title="Найти",
                           form=form,
                           q=q,
                           menu=menu,
                           q_1_mill=q_1_mill)


@app.route("/findcity", methods=['GET', 'POST'])
def find_city():
    return redirect(url_for('myfind'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title="ERROR404"), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run()
