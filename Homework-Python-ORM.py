import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale

login = ''
password = ''
name_of_db = ''

DSN = f'postgresql://{login}:{password}@localhost:5432/{name_of_db}'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

name_of_publisher = input('Введите имя издателя: ')
for c in session.query(Shop).join(Stock.shop).join(Book.stocks).join(Publisher.book).filter(Publisher.name == name_of_publisher).all():
    print(c)
session.close()
