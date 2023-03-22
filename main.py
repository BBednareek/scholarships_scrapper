from Functions.MojeStypendium.insertData import *
from Scrapping.Scrapping.MojeStypendia.konkursy_z_mojestypendia import konkursy_mojestypendia
from Scrapping.MojeStypendia.stypendia_z_mojestypendia import stypendia_mojestypendia
from Scrapping.Scrapping.MojeStypendia.staze_z_mojestypendium import staz_mojestypendia

if __name__ == '__main__':
    createdb()

    konkursy_mojestypendia()
    stypendia_mojestypendia()
    staz_mojestypendia()

