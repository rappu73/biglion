from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy import create_engine, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import declarative_base
from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

metadata = MetaData()

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_NAME}@{DB_HOST}:{DB_PORT}/{DB_PASS}")

session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    city = Column(String)


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    cat = Column(String, nullable=False)


class Link(Base):
    __tablename__ = 'link'

    id = Column(Integer, primary_key=True)
    name_link = Column(String, nullable=False)
    img_link = Column(String, nullable=False)
    name_sale = Column(String, nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"))
    cat_id = Column(Integer, ForeignKey("category.id"))
    city_link = relationship("City", backref="city_link")
    category_link = relationship("Category", backref="category_link")





