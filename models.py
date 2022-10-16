import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60), unique=True, nullable=False)
    book = relationship('Book', back_populates='publisher')

    def __str__(self):
        return f'{self.id}:{self.name}'


class Book(Base):
    __tablename__ = 'book'
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=100), unique=False, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id', nullable=False))
    stocks = relationship('Stock', back_populates='book')
    publisher = relationship('Publisher', back_populates='book')

    def __str__(self):
        return f'{self.id}:{self.title}'


class Stock(Base):
    __tablename__ = 'stock'
    id = sq.Column(sq.Integer, primary_key=True)
    count = sq.Column(sq.Integer, nullable=False)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id', nullable=False))
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id', nullable=False))
    sales = relationship('Sale', back_populates='stock')
    book = relationship('Book', back_populates='stocks')
    shop = relationship('Shop', back_populates='stocks')

    def __str__(self):
        return f'{self.id}, {self.id_book}'


class Shop(Base):
    __tablename__ = 'shop'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60), nullable=False, unique=False)
    stocks = relationship('Stock', back_populates='shop')

    def __str__(self):
        return f'{self.id}:{self.name}'


class Sale(Base):
    __tablename__ = 'sale'
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Integer, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=True)
    count = sq.Column(sq.Integer, nullable=True)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id', nullable=False))
    stock = relationship('Stock', back_populates='sales')

    def __str__(self):
        return f'{self.id}:{self.price}, {self.date_sale}'


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
