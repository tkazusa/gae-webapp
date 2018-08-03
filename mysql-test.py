# -*- encoding: UTF-8 -*-
import sqlalchemy as sa

username = 'root'
password = 'passward'
host = 'localhost'
dbname = 'test'


# Connect to my sql
url = 'mysql+mysqldb://{username}:{password} \
       @{host}/{dbname}?charset=utf8'.format(username=username,
                                             password=password,
                                             host=host,
                                             dbname=dbname)
engine = sa.create_engine(url, echo=True)
engine.execute('DROP TABLE IF EXISTS items')


# Create table
engine.execute('''
    CREATE TABLE IF NOT EXISTS items (
    item_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name TEXT,
    price INTEGER
    )
    ''')


# Insert data
ins = "INSERT INTO items (name, price) VALUE (%s, %s)"
data = [("Banana", 300), ("Mango", 640), ("Kiwi", 280)]
for d in data:
    engine.execute(ins, d)

rows = engine.execute('SELECT * FROM  items')

# Show
for row in rows:
    print(row)

