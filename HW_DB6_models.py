import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


Base = declarative_base()    #спецкласс для регистрирования наследников

class Publisher(Base):
    __tablename__ = "publisher"


    id = sq.Column(sq.Integer, primary_key= True)
    name = sq.Column(sq.String(length=60), nullable= False)

    def __str__(self):
        return f'{self.id}: {self.name}'



class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key= True)
    title = sq.Column(sq.VARCHAR(length=60), nullable=False, unique= True)
    publisher_id = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable= False)

    publishers = relationship(Publisher, backref= "books")

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key= True)
    name = sq.Column(sq.String(length=60), nullable=False, unique= True)



class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key= True)
    book_id = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    shop_id = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    books = relationship(Book, backref="stockbook")
    shops = relationship(Shop, backref="stockshop")

class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key= True)
    price = sq.Column(sq.Integer, nullable= False)
    sale_date = sq.Column(sq.DATE, nullable= False)
    stock_id = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable= False)

    stocks = relationship(Stock, backref="sales")
    def __str__(self):
        return f'id={self.id}|price={self.price}|sale_date={self.sale_date}|stock_id={self.stock_id}|count={self.count}'



def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)