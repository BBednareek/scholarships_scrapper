import mysql.connector

conn = mysql.connector.connect(host='localhost', port='3306', user='root', password='', database='baza_danych')
cursor = conn.cursor()

query = "SHOW TABLES LIKE 'stypendia'"
cursor.execute(query)
result = cursor.fetchall()

if result:
    query = "DROP TABLE stypendia"
    cursor.execute(query)
    conn.commit()

    query = "CREATE TABLE stypendia (id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, tytul varchar(500) NOT NULL, organizator varchar(100) NOT NULL, rodzaj varchar(50) NOT NULL, zasieg varchar(50) NOT NULL, grupa_docelowa varchar(100) NOT NULL, termin varchar(20) NOT NULL, link varchar(1000) NOT NULL)"
    cursor.execute(query)
    conn.commit()
    def appendStypendia(tytul: str, organizator: str, rodzaj: str, zasieg: str, grupa: str, termin: str, link: str):
        try:
            query = "INSERT INTO stypendia (tytul, organizator, rodzaj, zasieg, grupa_docelowa, termin, link) values(%s, %s, %s, %s, %s, %s, %s)"
            values = (tytul, organizator, rodzaj, zasieg, grupa, termin, link)
            cursor.execute(query, values)
            conn.commit()
        except:
            print("Błąd")
else:
    query = "CREATE TABLE stypendia (id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, tytul varchar(500) NOT NULL, organizator varchar(100) NOT NULL, rodzaj varchar(50) NOT NULL, zasieg varchar(50) NOT NULL, grupa_docelowa varchar(100) NOT NULL, termin varchar(20) NOT NULL, link varchar(1000) NOT NULL)"
    cursor.execute(query)
    conn.commit()
    def appendStypendia(tytul: str, organizator: str, rodzaj: str, zasieg: str, grupa: str, termin: str, link: str):
        try:
            query = "INSERT INTO stypendia (tytul, organizator, rodzaj, zasieg, grupa_docelowa, termin, link) values(%s, %s, %s, %s, %s, %s, %s)"
            values = (tytul, organizator, rodzaj, zasieg, grupa, termin, link)
            cursor.execute(query, values)
            conn.commit()
        except:
            print("Błąd")