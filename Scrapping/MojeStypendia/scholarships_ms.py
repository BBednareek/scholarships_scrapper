from asyncio import gather
from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag
from datetime import datetime
from typing import List, Dict, Optional, Any, Coroutine

from utils.error_handler import error_handler


class MojeStypendiaScraper:
    """
    Asynchronous scraper for collecting scholarship data from MojeStypendia.
    """

    DOMESTIC_BASE_URL = "https://www.mojestypendium.pl/znajdz-stypendium/page/{}/?grupa_docelowa_45=studenci"
    FOREIGN_BASE_URL = "https://www.mojestypendium.pl/znajdz-stypendium-zagraniczne/page/{}/?grupa_docelowa_45=studenci"

    @staticmethod
    def build_url(base_url: str, page_number: int) -> str:
        """
        Builds the URL for a specific scholarship listing page.

        Args:
            base_url (str): The base URL of the scholarship listing page.
            page_number (int): Page index.

        Returns:
            str: URL to the specific page.
        """
        return base_url.format(page_number)

    @error_handler("fetch")
    async def fetch_html(self, session: ClientSession, url: str) -> str:
        """
        Fetches HTML content from the provided URL asynchronously.

        Args:
            session (ClientSession): Open HTTP session.
            url (str): Target URL.

        Returns:
            str: Raw HTML response.
        """
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()

    @staticmethod
    def parse_html_to_soup(html: str) -> BeautifulSoup:
        """
        Parses HTML into a BeautifulSoup object.

        Args:
            html (str): Raw HTML content.

        Returns:
            BeautifulSoup: Parsed document object.
        """
        return BeautifulSoup(html, 'html.parser')

    @staticmethod
    def extract_scholarship_blocks(soup: BeautifulSoup) -> List[Tag]:
        """
        Extracts all scholarship DOM containers from the parsed HTML.

        Args:
            soup (BeautifulSoup): Parsed HTML document.

        Returns:
            List[Tag]: List of scholarship block tags.
        """
        return soup.find_all('div', class_='row large-up-2 list-open')

    @staticmethod
    @error_handler("convert")
    def parse_date(date_str: str) -> Optional[str]:
        """
        Parses date string to 'YYYY.MM.DD' format.

        Args:
            date_str (str): Date in format 'DD.MM.YYYY'.

        Returns:
            Optional[str]: Reformatted date string or None.
        """
        dt: datetime = datetime.strptime(date_str.strip(), "%d.%m.%Y")
        return dt.strftime("%Y.%m.%d")

    @error_handler("convert")
    def parse_scholarship_block(self, block: Tag, location: str) -> Dict[str, str]:
        """
        Parses an individual scholarship listing block into a dictionary.

        Args:
            block (Tag): HTML tag containing one scholarship's data.
            location (str): determines whether the scholarship is domestic or foreign.

        Returns:
            Dict[str, str]: Structured scholarship info.
        """
        raw_date: str = block.find('span', class_='content').find_next('span', class_='').text.strip()
        return {
            "from": "MojeStypendia",
            "title": block.find('h2', class_='title').text.strip(),
            "organizer": block.find('p', class_='organizator-title').text.strip(),
            "targetGroup": block.find_all('span', class_='taxonomy-list w2')[0].text.strip(),
            "deadline": self.parse_date(raw_date),
            "link": block.find('a', class_='hide-for-large anchor')['href'],
            "path": "assets/images/stypendium.svg",
            "location": location
        }

    @error_handler("fetch")
    async def determine_page_count(self, session: ClientSession, base_url: str) -> int:
        html: str = await self.fetch_html(session, self.build_url(base_url, 1))
        soup: BeautifulSoup = self.parse_html_to_soup(html)
        try:
            return int(list(soup.find(class_='page-numbers').next_siblings)[-4].text)
        except (AttributeError, IndexError, ValueError):
            return 1

    @error_handler("fetch")
    async def scrape_pages(self, session: ClientSession, base_url: str, location: str) -> List[Dict[str, str]]:
        """
    Iterates over all available pages under a given base URL, fetches scholarship data from each,
    and returns a flat list of parsed scholarship dictionaries.

    Args:
        session (ClientSession): Active aiohttp session for HTTP requests.
        base_url (str): URL template with `{}` placeholder for page numbers.
        location (str): Label for scholarship origin (e.g., "Polska", "Zagranica").

    Returns:
        List[Dict[str, Any]]: Aggregated list of scholarships from all pages.
    """

        total_pages: int = await self.determine_page_count(session, base_url)
        tasks: list[Coroutine[Any, Any, list[dict[str, Any]]]] = [
            self.scrape_single_page(session, self.build_url(base_url, page), location)
            for page in range(1, total_pages + 1)
        ]
        results: List = await gather(*tasks)

        return [item for sublist in results for item in sublist]

    @error_handler("fetch")
    async def scrape_single_page(self, session: ClientSession, url: str, location: str) -> List[Dict[str, Any]]:
        """
            Fetches and parses scholarship entries from a single MojeStypendia page.

            Args:
                session (ClientSession): Active aiohttp session for HTTP requests.
                url (str): Fully constructed URL of the page to scrape.
                location (str): Scholarship location tag to be embedded in the result.

            Returns:
                List[Dict[str, Any]]: List of scholarship dictionaries from the specified page.
            """

        html: str = await self.fetch_html(session, url)
        soup: BeautifulSoup = self.parse_html_to_soup(html)
        blocks: List[Tag] = self.extract_scholarship_blocks(soup)
        return [self.parse_scholarship_block(block, location) for block in blocks]

    @error_handler("fetch")
    async def fetch_all(self) -> List[Dict[str, str]]:
        """
    Fetches all domestic and foreign scholarships from MojeStypendia.pl in parallel.

    Returns:
        List[Dict[str, Any]]: Combined list of all parsed scholarships with location metadata.
    """
        async with ClientSession() as session:
           domestic_data, foreign_data = await gather(
               self.scrape_pages(session, self.DOMESTIC_BASE_URL, "Polska"),
               self.scrape_pages(session, self.FOREIGN_BASE_URL, "Zagranica"),
        )
        return domestic_data + foreign_data