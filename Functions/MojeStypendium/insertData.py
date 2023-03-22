import mysql.connector
import MySQLdb

def createdb():
    conn = mysql.connector.connect(host='localhost', port='3306', user='root', password='Bednarek')
    cursor = conn.cursor()

    try:
        query = 'CREATE DATABASE IF NOT EXISTS `programy`'
        cursor.execute(query)
        conn.commit()
        conn.close()
    except(MySQLdb.Error, MySQLdb.Warning) as e:
        print('Błąd na etapie tworzenia bazy danych')
        print(e)

    conn = mysql.connector.connect(host='localhost', port='3306', user='root', password='Bednarek', database='programy')
    cursor = conn.cursor()

    try:
        query = "CREATE TABLE lista_programow (id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, kategoria varchar(20) NOT NULL, img varchar(100) NOT NULL, tytul varchar(65535) NOT NULL, organizator varchar(65535) NOT NULL, tematyka varchar(50) NOT NULL, zasieg varchar(50) NOT NULL, odbiorcy varchar(50) NOT NULL, termin varchar(50), link varchar(65535) NOT NULL, opis varchar(65535) NOT NULL,sortowanie varchar(10))"

        cursor.execute(query)
        conn.commit()
        conn.close()
    except(MySQLdb.Error, MySQLdb.Warning) as e:
        print('Błąd na etapie tworzenia tabeli lista_programow')
        print(e)
    finally:
        conn.close()



def dodajStypendiumMojeStypendia(kategoria:str, img: str, tytul: str, organizator: str, tematyka: str, zasieg: str, odbiorcy: str, termin: str, link: str, opis:str,sortowanie:str):
    conn = mysql.connector.connect(host='localhost', port='3306', user='root', password='Bednarek', database='programy')
    cursor = conn.cursor()
    try:
        query = "INSERT INTO lista_programow (wyroznione, kategoria, img, tytul, organizator, tematyka, zasieg, odbiorcy, termin, link, opis, kod, sortowanie) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (kategoria, img, tytul, organizator, tematyka, zasieg, odbiorcy, termin, link, opis,sortowanie)
        cursor.execute(query, values)
        conn.commit()
    except(MySQLdb.Error, MySQLdb.Warning) as e:
        print("Błąd na etapie dodawania stypendiów z witryny mojestypendium")
        print(e)
    finally:
        conn.close()

def dodajStazMojeStypendia(kategoria:str, img:str, tytul: str, organizator: str, tematyka: str, zasieg: str, odbiorcy:str, link: str, opis:str):
    conn = mysql.connector.connect(host='localhost', port='3306', user='root', password='Bednarek', database='programy')
    cursor = conn.cursor()
    try:
        query = "INSERT INTO lista_programow (wyroznione, kategoria, img, tytul, organizator, tematyka, zasieg, odbiorcy, link, opis, kod) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (kategoria, img, tytul, organizator, tematyka, zasieg, odbiorcy, link, opis)
        cursor.execute(query, values)
        conn.commit()
    except(MySQLdb.Error, MySQLdb.Warning) as e:
        print("Błąd na etapie dodawania stazów z witryny mojestypendium")
        print(e)

# def dodajVaqat(kategoria:str, img:str, tytul:str, organizator: str, tematyka: str, zasieg: str, odbiorcy: str, termin: str, opis: str, sortowanie:str):
#
#     conn = mysql.connector.connect(host='localhost', port='3306', user='root', password='Bednarek', database='programy')
#     cursor = conn.cursor()
#     try:
#         query = "INSERT INTO lista_programow (wyroznione, kategoria, img, tytul, organizator, tematyka, zasieg, odbiorcy, termin, link, opis, kod, sortowanie) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
#         values = (kategoria, img, tytul, organizator, tematyka, zasieg, odbiorcy, termin, link, opis, sortowanie)
#         cursor.execute(query, values)
#         conn.commit()
#     except(MySQLdb.Error, MySQLdb.Warning) as e:
#         print("Błąd na etapie dodawania konkursów z witryny mojestypendium")
#         print(e)
#     finally:
#         conn.close()

def dodajKonkursMojeStypendia(kategoria:str, img: str, tytul: str, organizator: str, tematyka: str, zasieg: str, odbiorcy: str, termin: str, link: str, opis:str,sortowanie:str):

    conn = mysql.connector.connect(host='localhost', port='3306', user='root', password='Bednarek', database='programy')
    cursor = conn.cursor()
    try:
        query = "INSERT INTO lista_programow (wyroznione, kategoria, img, tytul, organizator, tematyka, zasieg, odbiorcy, termin, link, opis, kod, sortowanie) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
        values = (kategoria, img, tytul, organizator, tematyka, zasieg, odbiorcy, termin, link, opis,sortowanie)
        cursor.execute(query, values)
        conn.commit()
    except(MySQLdb.Error, MySQLdb.Warning) as e:
        print("Błąd na etapie dodawania konkursów z witryny mojestypendium")
        print(e)
    finally:
        conn.close()

# def dodajWydarzenieEuroDesk(kategoria:str, img: str, tytul: str, organizator: str, tematyka: str, zasieg: str, odbiorcy: str, termin: str, link: str, opis:str):
#     try:
#         query = "INSERT INTO lista_programow (wyroznione, kategoria, img, tytul, organizator, tematyka, zasieg, odbiorcy, termin, link, opis, kod) values(%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
#         values = (kategoria, img, tytul, organizator, tematyka, zasieg, odbiorcy, termin, link, opis)
#         cursor.execute(query, values)
#         conn.commit()
#     except(MySQLdb.Error, MySQLdb.Warning) as e:
#         print("Błąd na etapie dodawania konkursów z witryny mojestypendium")
#         print(e)

# def dodajStazPracuj(wyroznione:str, kategoria:str, img: str, tytul: str, organizator: str, tematyka: str, zasieg: str, termin: str, link: str, opis:str, kod:str):
#     conn = mysql.connector.connect(host='localhost', port='3306', user='root', password='Bednarek', database='programy')
#     cursor = conn.cursor()
#     try:
#         query = "INSERT INTO lista_programow (wyroznione, kategoria, img, tytul, organizator, tematyka, zasieg, odbiorcy, termin, link, opis, kod) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#         values = (wyroznione, kategoria, img, tytul, organizator, tematyka, zasieg, odbiorcy, termin, link, opis, kod)
#         cursor.execute(query, values)
#         conn.commit()
#     except(MySQLdb.Error, MySQLdb.Warning) as e:
#         print("Błąd na etapie dodawania konkursów z witryny mojestypendium")
#         print(e)