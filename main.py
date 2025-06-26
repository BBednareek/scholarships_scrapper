from asyncio import gather, run
from typing import List, Dict, Any
from Scrapping.MojeStypendia.scholarships_ms import MojeStypendiaScraper
from Scrapping.EuroDesk.scholarships_ed import EuroDeskScraper
from Firebase.push_data import push_scholarship_data
from utils.error_handler import error_handler

@error_handler("fetch")
async def gather_all_scholarships() -> List[Dict[str, Any]]:
    """
    Asynchronously gathers scholarships from MojeStypendia and Eurodesk.

    Returns:
        List[Dict[str, Any]]: Combined list of all collected scholarships.
    """
    moje_stypendia = MojeStypendiaScraper()
    eurodesk = EuroDeskScraper()

    moje_stypendia_data: List[Dict[str, Any]]
    eurodesk_data: List[Dict[str, Any]]

    moje_stypendia_data, eurodesk_data = await gather(
        moje_stypendia.fetch_all(),
        eurodesk.fetch_eurodesk()
    )

    return moje_stypendia_data + eurodesk_data

def main() -> None:
    """
    Main entrypoint: scrapes data and pushes to Firestore, entirely in memory.
    """
    data: List[Dict[str, Any]] = run(gather_all_scholarships())
    push_scholarship_data(data)


if __name__ == "__main__":
    main()
