from Scrapping.MojeStypendia.scholarships import scholarshipsMS
from Scrapping.EuroDesk.scholarships import scholarshipsED
from Firebase.push_data import push_data

if __name__ == "main":
    scholarshipsMS()
    scholarshipsED()
    push_data()