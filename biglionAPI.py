from fastapi import FastAPI

from models.models import session, City, Category, Link

app = FastAPI()


@app.get("/city")
def hello():
    city = session.query(City).all()
    city_data = []
    for el in city:
        city_data.append(el.city)
    return city_data


@app.get("/category")
def hello():
    category = session.query(Category).all()
    category_data = []
    for el in category:
        category_data.append(el.cat)
    return category_data


@app.post("/link")
def hello(city: str, cat: str):
    link = session.query(Link).all()
    link_data = {}
    for el in link:
        if el.city_link.city == city and el.category_link.cat == cat:
            link_data[el.name_link] = el.img_link, el.name_sale
    return link_data