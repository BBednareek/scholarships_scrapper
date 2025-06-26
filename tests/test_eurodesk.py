from pytest import fixture
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, List
from Scrapping.EuroDesk.scholarships_ed import EuroDeskScraper


HTML_SNIPPET: str = """
<html>
  <body>
    <h3 class="card-title"><a href="/granty/123">Scholarship Title</a></h3>
    <p class="card-fundator">Organizer Name</p>
    <small><b>25.12.2025</b></small>
  </body>
</html>
"""


@fixture
def scraper() -> EuroDeskScraper:
    """
    Fixture to provide a fresh instance of EuroDeskScraper for each test.

    Returns:
        EuroDeskScraper: An instance of the scraper class.
    """
    return EuroDeskScraper()


def test_parse_date_valid(scraper: EuroDeskScraper) -> None:
    """
    Tests parsing of a valid date string.

    Args:
        scraper (EuroDeskScraper): The scraper fixture.
    """
    assert scraper.parse_date("01.01.2025") == datetime(2025, 1, 1)


def test_parse_date_invalid(scraper: EuroDeskScraper) -> None:
    """
    Tests parsing of an invalid date string (e.g. 'stały nabór').

    Args:
        scraper (EuroDeskScraper): The scraper fixture.
    """
    assert scraper.parse_date("stały nabór") is None


def test_parse_html_to_soup(scraper: EuroDeskScraper) -> None:
    """
    Verifies that valid HTML is correctly parsed into BeautifulSoup.

    Args:
        scraper (EuroDeskScraper): The scraper fixture.
    """
    soup: BeautifulSoup = scraper.parse_html_to_soup("<html><body><h1>Test</h1></body></html>")
    assert isinstance(soup, BeautifulSoup)
    assert soup.find("h1").text == "Test"


def test_extract_fields(scraper: EuroDeskScraper) -> None:
    """
    Validates that all required fields are extracted from the HTML.

    Args:
        scraper (EuroDeskScraper): The scraper fixture.
    """
    soup: BeautifulSoup = scraper.parse_html_to_soup(HTML_SNIPPET)
    fields: Dict[str, List] = scraper.extract_fields(soup)
    assert "titles" in fields and len(fields["titles"]) == 1
    assert "organizers" in fields and len(fields["organizers"]) == 1
    assert "deadlines" in fields and len(fields["deadlines"]) == 1


def test_parse_scholarship_entry(scraper: EuroDeskScraper) -> None:
    """
    Asserts correctness of single scholarship parsing logic.

    Args:
        scraper (EuroDeskScraper): The scraper fixture.
    """
    soup: BeautifulSoup = scraper.parse_html_to_soup(HTML_SNIPPET)
    elements: Dict[str, List] = scraper.extract_fields(soup)
    entry: Dict[str, str] = scraper.parse_scholarship_entry(0, elements)
    assert entry["Title"] == "Scholarship Title"
    assert entry["Organizer"] == "Organizer Name"
    assert entry["Deadline"] == datetime(2025, 12, 25)
    assert entry["Link"] == "https://www.eurodesk.pl/granty/123"


def test_build_scholarship_list(scraper: EuroDeskScraper) -> None:
    """
    Validates the full list of scholarships built from HTML.

    Args:
        scraper (EuroDeskScraper): The scraper fixture.
    """
    soup: BeautifulSoup = scraper.parse_html_to_soup(HTML_SNIPPET)
    scholarships: List[Dict[str, str]] = scraper.build_scholarship_list(soup)
    assert isinstance(scholarships, list)
    assert scholarships[0]["From"] == "Eurodesk"
