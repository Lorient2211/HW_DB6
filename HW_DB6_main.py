import sqlalchemy
from sqlalchemy.orm import sessionmaker
from HW_DB6_models import create_tables, Publisher, Sale, Shop, Stock, Book
from passw import login, password, bd_name

DSN = 'postgresql://%s:%s@localhost:5432/%s' %(login, password, bd_name) #url строка подключения к источнику данных
engine = sqlalchemy.create_engine(DSN)   #абстракция для подключения к базе данных  #engine - объект который может подключиться к БД (движок)


create_tables(engine)  #создание таблиц


Session = sessionmaker(bind = engine)    #аналог курсора bind  связывает сессию с движком
session = Session()    #сама сессия

publisher1 = Publisher(name ='testname')
book1 = Book(title = "test_book1", publisher_id = 1)
book2 = Book(title = "test_book2", publisher_id = 1)
book3 = Book(title = "test_book3", publisher_id = 1)
shop1 = Shop(name = "test_shop_name1")
shop2 = Shop(name = "test_shop_name2")
stock1 = Stock(book_id = 1, shop_id = 1, count = 10)
stock2 = Stock(book_id = 2, shop_id = 2, count = 20)
stock3 = Stock(book_id = 3, shop_id = 1, count = 10)
sale1 = Sale(price = 100, sale_date = '10-10-2020', stock_id = 1, count = 1)
sale2 = Sale(price = 110, sale_date = '11-11-2020', stock_id = 2, count = 4)
sale3 = Sale(price = 120, sale_date = '12-11-2020', stock_id = 3, count = 5)
session.add(publisher1)
session.add_all([book1, book2, book3])
session.add_all([shop1, shop2])
session.add_all([stock1, stock2, stock3])
session.add_all([sale1, sale2,sale3])
session.commit()
#print(publisher1)
#print(sale3)


# выборка. тут всего 1 автор (testname)
pub_name = input('')
sale_things = {}
for q in session.query(Sale).join(Stock).join(Shop).join(Book).join(Publisher).filter(Publisher.name == (pub_name)):
    price = int(q.price)
    sale_date = q.sale_date
    count = int(q.count)
    sale_things[q.stock_id] = [sale_date, price * count]
#print(sale_things)

stock_book_shop_id = {}
for q in session.query(Stock).join(Book).join(Publisher).filter(Publisher.name == (pub_name)):
    stock_book_shop_id[q.id] = [q.book_id, q.shop_id]

for q in session.query(Book).join(Publisher).filter(Publisher.name == (pub_name)):
    for key, value in stock_book_shop_id.items():
        if value[0] == q.id:
            value[0] = q.title

for q in session.query(Shop).all():
    for key, value in stock_book_shop_id.items():
        if value[1] == q.id:
            value[1] = q.name
#print(stock_book_shop_id)

for key1, value1 in sale_things.items():
    for key2, value2 in stock_book_shop_id.items():
        if key1 == key2:
            value1 += value2
#print(sale_things)

#название книги | название магазина, в котором была куплена эта книга | стоимость покупки | дата покупки
for key, value in sale_things.items():
    print(f'{value[2]} | {value[-1]} | {value[1]} | {value[0]}')




session.close() #закрытие сессии