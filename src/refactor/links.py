import datetime
from datetime import date

from bs4 import BeautifulSoup


def parse_page_links(html: str, start_date: date, end_date: date, url: str):
    """
    Парсит ссылки на бюллетени с одной страницы:
    <a class="accordeon-inner__item-title link xls" href="/upload/reports/oil_xls/oil_xls_20240101_test.xls">link1</a>
    """
    results = []
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", class_="accordeon-inner__item-title link xls")

    for link in links:
        href = link.get("href")
        if not href:
            continue

        href_base = href.split("?")[0]

        if not (href_base.startswith("/upload/reports/oil_xls/oil_xls_") and href_base.endswith(".xls")):
            continue

        try:
            date_str = href.split("oil_xls_")[1][:8]
            extracted_date = datetime.datetime.strptime(date_str, "%Y%m%d").date()
        except:
            print(f"Ошибка формата даты в ссылке {href}" )
            continue

        if start_date <= extracted_date <= end_date:
            full_url = href if href.startswith("http") else f"https://spimex.com{href}"
            results.append((full_url, extracted_date))
        else:
            print(f"Ссылка {href} вне диапазона дат")
    return results
