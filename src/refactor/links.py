import datetime
from datetime import date

from urllib.parse import urljoin

from bs4 import BeautifulSoup





class BulletinsParser:
    def __init__(self, url: str, start_date: date, end_date: date):
        self.base_url = url
        self.start_date = start_date
        self.end_date = end_date

    def parse_html(self, html: str):
        '''HTML парсим и возвращаем список кортежей'''
        results = []
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all("a", class_="accordeon-inner__item-title link xls")

        for link in links:
            href = link.get("href")
            if not href:
                continue
            href_path = href.split("?")[0]
            if not ("/upload/reports/oil_xls/oil_xls_" in href_path and href_path.endswith(".xls")):
                continue
            try:
                filename_data = href_path.split("oil_xls_")[1][:8]
                file_date = datetime.datetime.strftime(filename_data, "%Y%m%d").date()
                if self.start_date <= file_date <= self.end_date:
                    full_url = self._bild_url(href_path)
                    results.append((full_url, file_date))
                else:
                    print('Вне диапазона')
            except Exception as e:
                print('Ну удалось извлечь')
        return results
    
    def _bild_url(self, href_path: str):
        '''Формируем полный урл'''
        if href_path.startswith("http"):
            return href_path
        return urljoin(self.base_url, href_path)
    
def parse_links(html: str, start_date: date, end_date: date, url: str):
    parser = BulletinsParser(url, start_date, end_date)
    return parser.parse_html(html)

# хелрпер
results = parse_links(html_content, date(2024,1,1), date(2024,2,1), "https://spimex.com")

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

        href = href.split("?")[0]
        if "/upload/reports/oil_xls/oil_xls_" not in href or not href.endswith(".xls"):
            continue

        try:
            date = href.split("oil_xls_")[1][:8]
            file = datetime.datetime.strptime(date, "%Y%m%d").date()
            if start_date <= file <= end_date:
                u = href if href.startswith("http") else f"https://spimex.com{href}"
                results.append((u, file))
            else:
                print(f"Ссылка {href} вне диапазона дат")
        except Exception as e:
            print(f"Не удалось извлечь дату из ссылки {href}: {e}")

    return results
