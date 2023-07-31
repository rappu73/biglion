from sqlalchemy.exc import IntegrityError
from models.models import City, session, Category, Link


# Добавляем город в таблицу
def add_city(city):
    city_name = City(city=city)
    session.add(city_name)

    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()  # откатываем session.add(user)
        return False


# Добавляем категорию в таблицу
def add_category(category):
    category_name = Category(cat=category)

    session.add(category_name)

    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()  # откатываем session.add(user)
        return False


# Добавляем ссылки в таблицу
def add_link(link, city, cat):
    city = session.query(City).filter(City.city == city).first()
    cat = session.query(Category).filter(Category.cat == cat).first()

    link_name = Link(name_link=link, city_id=city.id, cat_id=cat.id)
    session.add(link_name)

    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()  # откатываем session.add(user)
        return False


# Удаляем ссылки из таблицы
def del_link(city, cat):
    city = session.query(City).filter(City.city == city).first()
    cat = session.query(Category).filter(Category.cat == cat).first()
    link_name = session.query(Link).filter(Link.city_id == city.id, Link.cat_id == cat.id)
    for el in link_name:
        session.delete(el)

    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()  # откатываем session.add(user)
        return False


# def select_user(id):
#     user = session.query(City).filter(City.id == id).first()
#     print(user.city)

