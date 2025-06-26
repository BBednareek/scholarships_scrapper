from pytest import fixture, mark
from datetime import datetime
from typing import List, Dict, Any
from Scrapping.MojeStypendia.scholarships_ms import MojeStypendiaScraper
from aiohttp.web_request import Request
from aiohttp.web_response import Response

HTML_SNIPPET = """
<html>
  <body>
    <div class="row large-up-2 list-open">
      <h2 class="title">Sample Scholarship</h2>
      <p class="organizator-title">Sample Organizer</p>
      <span class="taxonomy-list w2">studenci</span>
      <span class="content">Deadline:</span><span>10.11.2025</span>
      <a class="hide-for-large anchor" href="http://example.com">Apply</a>
    </div>
    <div class="row large-up-2 list-open">
      <h2 class="title">Second Scholarship</h2>
      <p class="organizator-title">Second Organizer</p>
      <span class="taxonomy-list w2">studenci</span>
      <span class="content">Deadline:</span><span>stały nabór</span>
      <a class="hide-for-large anchor" href="http://example.org">Apply2</a>
    </div>
  </body>
</html>
"""


@fixture
def scraper() -> MojeStypendiaScraper:
    """
    Fixture providing a new instance of the scraper.
    """
    return MojeStypendiaScraper()


def test_build_url() -> None:
    """
    Test correct interpolation of page number into base URL.
    """
    url = MojeStypendiaScraper.build_url("http://test/{}/", 3)
    assert url == "http://test/3/"


def test_parse_date_valid(scraper: MojeStypendiaScraper) -> None:
    """
    Test parsing a valid date string.
    """
    date = scraper.parse_date("10.11.2025")
    assert isinstance(date, datetime)
    assert date.year == 2025 and date.month == 11 and date.day == 10


def test_parse_date_invalid(scraper: MojeStypendiaScraper) -> None:
    """
    Test that parsing invalid deadline returns None.
    """
    assert scraper.parse_date("invalid") is None


def test_parse_html_to_soup(scraper: MojeStypendiaScraper) -> None:
    """
    Test HTML parsing into BeautifulSoup.
    """
    soup = scraper.parse_html_to_soup("<html><p>hi</p></html>")
    assert soup.find("p").text == "hi"


def test_extract_scholarship_blocks(scraper: MojeStypendiaScraper) -> None:
    """
    Ensure blocks are extracted from the snippet.
    """
    soup = scraper.parse_html_to_soup(HTML_SNIPPET)
    blocks = scraper.extract_scholarship_blocks(soup)
    assert isinstance(blocks, list)
    assert len(blocks) == 2


def test_parse_scholarship_block(scraper: MojeStypendiaScraper) -> None:
    """
    Test parsing of a single scholarship block.
    """
    soup = scraper.parse_html_to_soup(HTML_SNIPPET)
    blocks = scraper.extract_scholarship_blocks(soup)
    entry_valid = scraper.parse_scholarship_block(blocks[0], "Polska")
    entry_open = scraper.parse_scholarship_block(blocks[1], "Polska")

    # First entry
    assert entry_valid["Title"] == "Sample Scholarship"
    assert entry_valid["Organizer"] == "Sample Organizer"
    assert isinstance(entry_valid["Deadline"], datetime)
    assert entry_valid["Link"] == "http://example.com"
    assert entry_valid["Location"] == "Polska"

    # Second entry has open deadline -> None
    assert entry_open["Title"] == "Second Scholarship"
    assert entry_open["Deadline"] is None

@mark.asyncio
async def test_scrape_pages_and_aggregate(mocker) -> None:
    """
    Mock determine_page_count() and scrape_single_page() to test fluent flow.
    """
    scraper = MojeStypendiaScraper()
    dummy: List[Dict[str, Any]] = [{"Title": "A"}, {"Title": "B"}]

    session_mock = mocker.MagicMock()
    mocker.patch.object(scraper, "determine_page_count", return_value=2)
    mocker.patch.object(scraper, "scrape_single_page", return_value=dummy)

    results: List[Dict[str, Any]] = await scraper.scrape_pages(
        session=session_mock,
        base_url=MojeStypendiaScraper.DOMESTIC_BASE_URL,
        location="Polska"
    )

    assert isinstance(results, list)
    assert len(results) == 4  # 2 pages x 2 entries per page


@mark.asyncio
async def test_scrape_single_page_http(aiohttp_server, scraper) -> None:
    """
    Integration-like test for scrape_single_page using a local HTTP server.
    """
    from aiohttp import web

    async def handler(_request: Request) -> Response:
        return web.Response(text="Hello, world")

    app = web.Application()
    app.router.add_get("/", handler)
    server = await aiohttp_server(app)

    from aiohttp import ClientSession
    async with ClientSession() as session:
        result = await scraper.scrape_single_page(session, f"http://{server.host}:{server.port}/", "Polska")

    assert isinstance(result, list)
    assert result[0]["Location"] == "Polska"
