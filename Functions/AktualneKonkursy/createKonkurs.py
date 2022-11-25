import mysql.connector

conn = mysql.connector.connect(host='localhost', port='3306', user='root', password='', database='baza_danych')
cursor = conn.cursor()

def appendKonkurs(tytul:str, organizator:str, termin:str, link:str, tekst:str, grupa_docelowa:str, rodzaj:str):
    try:
        query = "INSERT INTO konkursy (tytul, organizator, rodzaj, grupa_docelowa, termin, link, opis) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (tytul, organizator, rodzaj, grupa_docelowa, termin, link, tekst)
        cursor.execute(query, values)
        conn.commit()
    except:
        print("Błąd")