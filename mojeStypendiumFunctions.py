import mysql.connector

conn = mysql.connector.connect(host='localhost', port='3306', user='root', password='', database='baza_danych')
cursor = conn.cursor()

query = "DROP TABLE stypendia"
cursor.execute(query)
conn.commit()

query = "CREATE TABLE stypendia (id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, tytul varchar(500) NOT NULL, organizator varchar(100) NOT NULL, rodzaj varchar(50) NOT NULL, zasieg varchar(50) NOT NULL, grupa_docelowa varchar(100) NOT NULL, termin varchar(20) NOT NULL, link varchar(1000) NOT NULL)"
cursor.execute(query)
conn.commit()
def append_title(title, titles=[]):
    titles.append(title)
    for i in titles:
        try:
            query = "INSERT INTO stypendia (tytul) values(%s)"
            values = []
            values.append(titles.pop())
            cursor.execute(query, values)
            conn.commit()
        except:
            pass

def append_organizator(organizator, organizatorzy=[]):
    organizatorzy.append(organizator)
    for i in organizatorzy:
        try:
            query = "INSERT INTO stypendia (organizator) values(%s)"
            values = []
            values.append(organizatorzy.pop())
            cursor.execute(query, values)
            conn.commit()
        except:
            pass

def append_type(rodzaj, rodzaje=[]):
    rodzaje.append(rodzaj)
    for i in rodzaje:
        try:
            query = "INSERT INTO stypendia (rodzaj) values(%s)"
            values = []
            values.append(rodzaje.pop())
            cursor.execute(query, values)
            conn.commit()
        except:
            pass

def append_range(zasieg, zasiegi=[]):
    zasiegi.append(zasieg)
    for i in zasiegi:
        try:
            query = "INSERT INTO stypendia (zasieg) values(%s)"
            values = []
            values.append(zasiegi.pop())
            cursor.execute(query, values)
            conn.commit()
        except:
            pass

def append_group(grupa, grupy=[]):
    grupy.append(grupa)
    for i in grupy:
        try:
            query = "INSERT INTO stypendia (grupa_docelowa) values(%s)"
            values = []
            values.append(grupy.pop())
            cursor.execute(query, values)
            conn.commit()
        except:
            pass

def append_deadline(termin, terminy=[]):
    terminy.append(termin)
    for i in terminy:
        try:
            query = "INSERT INTO stypendia (termin) values(%s)"
            values = []
            values.append(terminy.pop())
            cursor.execute(query, values)
            conn.commit()
        except:
            pass

def append_link(link, linki=[]):
    linki.append(link)
    for i in linki:
        try:
            query = "INSERT INTO stypendia (link) values(%s)"
            values = []
            values.append(linki.pop())
            cursor.execute(query, values)
            conn.commit()
        except:
            pass

