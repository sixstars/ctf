from pysqlcipher import dbapi2 as sqlcipher
db = sqlcipher.connect('BOOKS.db')
db.execute("PRAGMA key='320b42d5771df37906eee0fff53c49059122eeaf'")
print db.execute('select * from sqlite_master').fetchall()
print db.execute('select * from books_table').fetchall()
