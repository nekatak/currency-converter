import sqlite3

conn = sqlite3.connect("currencies.db")

c = conn.cursor()

c.execute("""CREATE TABLE currencies
          (exchange_rate real, symbol text, date text)""")

conn.commit()

conn.close()
