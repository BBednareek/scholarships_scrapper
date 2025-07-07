from typing import List, Dict, Optional
from aiohttp.client import ClientSession
from bs4 import BeautifulSoup, Tag, NavigableString
from datetime import datetime
from utils.error_handler import error_handler

class EuroDeskScraper:
    """
    Asynchronous scraper for fetching scholarships from the Eurodesk portal.
    """

    EURODESK_URL: str = (
        "https://www.eurodesk.pl/granty?whom=7&category=17&sort=deadline%252Casc&limit=500&page=1"
    )

    @error_handler("fetch")
    async def fetch_html(self, session: ClientSession, url: str) -> str:
        """
        Fetches raw HTML content from a URL.

        Args:
            session (ClientSession): Active HTTP session.
            url (str): Target Eurodesk page.

        Returns:
            str: Raw HTML.
        """
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()

    @staticmethod
    def parse_html_to_soup(html: str) -> BeautifulSoup:
        """
        Converts HTML string into BeautifulSoup object.

        Args:
            html (str): Raw HTML content.

        Returns:
            BeautifulSoup: Parsed document.
        """
        return BeautifulSoup(html, 'html.parser')

    @staticmethod
    @error_handler("convert")
    def parse_date(date_str: str) -> Optional[str]:
        """
        Parses a date string into 'YYYY.MM.DD' format, returns 'stały nabór' if applicable,
        and returns None for unknown formats.

        Args:
            date_str (str): Date in format 'DD.MM.YYYY' or text like 'stały nabór'.

        Returns:
            Optional[str]: Reformatted date string, 'stały nabór', or None.
        """
        clean_str = date_str.strip().lower()

        if clean_str == "stały nabór":
            return "stały nabór"

        try:
            dt = datetime.strptime(clean_str, "%d.%m.%Y")
            return dt.strftime("%Y.%m.%d")
        except ValueError:
            return None

    @staticmethod
    def extract_fields(soup: BeautifulSoup) -> Dict[str, List[Tag]]:
        """
        Extracts scholarship field tags from parsed HTML.

        Args:
            soup (BeautifulSoup): Parsed DOM tree.

        Returns:
            Dict[str, List[Tag]]: Dictionary of tag lists.
        """
        return {
            "titles": soup.find_all('h3', class_='card-title'),
            "organizers": soup.find_all('p', class_='card-fundator'),
            "deadlines": soup.find_all('small')
        }

    @error_handler("convert")
    def parse_scholarship_entry(self, i: int, elements: Dict[str, List[Tag]]) -> Dict[str, str]:
        """
        Builds a single scholarship record from HTML components.

        Args:
            i (int): Index of the item.
            elements (Dict[str, List[Tag]]): Extracted HTML fields.

        Returns:
            Dict[str, str]: Scholarship data.
        """

        title_tag: Tag | NavigableString | None = elements["titles"][i].find("a")
        title: str = title_tag.text.strip() if title_tag else ""
        link: str = f"https://www.eurodesk.pl{title_tag['href']}" if title_tag else ""

        organizer: str = elements["organizers"][i].text.strip()

        deadline_element: Tag = elements["deadlines"][i]
        raw_date: str = ""

        if deadline_element.find("b"):
            raw_date: str = deadline_element.find("b").text.strip()
        elif deadline_element.find("time") and deadline_element.find("time").has_attr("datetime"):
            raw_date: str = deadline_element.find("time")["datetime"].split("T")[0]

        parsed_deadline: datetime | None = self.parse_date(raw_date) if raw_date else None

        return {
            "from": "Eurodesk",
            "title": title,
            "organizer": organizer,
            "targetGroup": "studenci",
            "deadline": parsed_deadline,
            "link": link,
            "path": "assets/images/stypendium.svg",
            "location": "Polska"
        }

    @error_handler("convert")
    def build_scholarship_list(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """
        Compiles all parsed scholarships into structured data.

        Args:
            soup (BeautifulSoup): Parsed HTML document.

        Returns:
            List[Dict[str, str]]: List of structured scholarships.
        """
        elements: Dict[str, List[Tag]] = self.extract_fields(soup)
        total: int = min(len(elements["titles"]), len(elements["organizers"]), len(elements["deadlines"]))
        return [self.parse_scholarship_entry(i, elements) for i in range(total)]

    @error_handler("fetch")
    async def fetch_eurodesk(self) -> List[Dict[str, str]]:
        """
        Asynchronously fetches and parses scholarships from Eurodesk.

        Returns:
            List[Dict[str, str]]: Parsed scholarships from Eurodesk.
        """
        async with ClientSession() as session:
            html: str = await self.fetch_html(session, self.EURODESK_URL)
            soup: BeautifulSoup = self.parse_html_to_soup(html)
            return self.build_scholarship_list(soup)
