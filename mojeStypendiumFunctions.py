import psycopg2

hostname = '127.0.0.1'
database = 'baza_danych'
username ='root'
pwd = ''
port_id = 3306
conn = None
cursor = None

try:
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id
    )
    cursor = conn.cursor()

    create_table = '''CREATE TABLE IF NOT EXISTS kutas(
                                    id              int PRIMARY KEY AUTO_INCREMENT NOT NULL UNIQUE,
                                    tytul           varchar(250) NOT NULL UNIQUE,
                                    organizator     varchar(250) NOT NULL,
                                    rodzaj          varchar(50) NOT NULL,
                                    zasieg          varchar(50) NOT NULL,
                                    grupa_docelowa  varchar(50) NOT NULL,
                                    termin          varchar(10) NOT NULL)'''

    cursor.execute(create_table)

except Exception as error:
    print(error)

finally:
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()

def append_title(title, titles=[]):
    titles.append(title)

def append_organizator(organizator, organizatorzy=[]):
    organizatorzy.append(organizator)

def append_type(rodzaj, rodzaje=[]):
    rodzaje.append(rodzaj)

def append_range(zasieg, zasiegi=[]):
    zasiegi.append(zasieg)

def append_group(grupa, grupy=[]):
    grupy.append(grupa)

def append_deadline(termin, terminy=[]):
    terminy.append(termin)

def append_link(link, linki=[]):
    linki.append(link)

