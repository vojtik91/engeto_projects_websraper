import requests
import pandas as pd
from bs4 import BeautifulSoup
import sys
from urllib.parse import urljoin


MAIN_URL = "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"

def get_html(url: str) -> str:
    """
    Stáhne HTML kód z dané URL adresy.

    Args:
        url (str): URL adresa stránky.
    
    Returns:
        str: HTML kód stránky.
    """
    response = requests.get(url)
    response.encoding = "utf-8"
    return response.text

def get_districts(html: str) -> dict[str, str]:
    """
    Získá seznam okresů a jejich URL z hlavní stránky.

    Args:
        html (str): HTML hlavní stránky.

    Returns:
        Dict[str, str]: Slovník {název okresu: URL okresu}.
    """
    soup = BeautifulSoup(html, "html.parser")
    district_links = {}
    
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) > 2:
            district_name = cells[1].text.strip()
            link_tag = cells[3].find("a")
            if link_tag and "href" in link_tag.attrs:
                link = urljoin(MAIN_URL, link_tag["href"])
                district_links[district_name] = link
                
    return district_links

def get_town_links(html: str) -> list[dict[str, str]]:
    """
    Získá seznam obcí v daném okrese.

    Args:
        html (str): HTML stránky okresu.

    Returns:
        List[Dict[str, str]]: Seznam slovníků s klíči "Kód obce", "Název obce" a "Link".
    """
    soup = BeautifulSoup(html, "html.parser")
    town_data = []
    
    for row in soup.find_all("tr")[2:]:
        cells = row.find_all("td")
        if len(cells) >= 2:
            link_tag = cells[0].find("a")
            if link_tag and "href" in link_tag.attrs:
                code = link_tag.text.strip()
                name = cells[1].text.strip()
                link = urljoin(MAIN_URL, link_tag["href"])
                town_data.append({"Kód obce": code, "Název obce": name, "Link": link})
    
    return town_data

def get_town_stats(soup: BeautifulSoup) -> dict[str, int]|None:
    """
    Získá základní statistiky voleb v obci.

    Args:
        soup (BeautifulSoup): HTML parsovaný pomocí BeautifulSoup.

    Returns:
        Optional[Dict[str, int]]: Slovník s počtem voličů, vydaných obálek a platných hlasů,
                                  nebo None, pokud nejsou data dostupná.
    """
    tables = soup.find_all("table")
    if len(tables) < 3:
        return None

    stats_cells = tables[0].find_all("td")
    try:
        return {
            "Voliči v seznamu": int(stats_cells[3].text.strip().replace("\xa0", "").replace(" ", "")),
            "Vydané obálky": int(stats_cells[4].text.strip().replace("\xa0", "").replace(" ", "")),
            "Platné hlasy": int(stats_cells[7].text.strip().replace("\xa0", "").replace(" ", "")),
        }
    except (IndexError, ValueError):
        return None

def get_party_votes(soup: BeautifulSoup) -> dict[str, int]:
    """
    Získá počet hlasů pro jednotlivé strany v obci.

    Args:
        soup (BeautifulSoup): HTML parsovaný pomocí BeautifulSoup.

    Returns:
        Dict[str, int]: Slovník {název strany: počet hlasů}.
    """
    tables = soup.find_all("table")
    parties = {}
    
    for table in tables[1:]:  # Procházení tabulek s hlasy
        rows = table.find_all("tr")[2:]
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 3:
                party_name = cells[1].text.strip()
                try:
                    votes = int(cells[2].text.strip().replace("\xa0", "").replace(" ", ""))
                    parties[party_name] = votes
                except ValueError:
                    continue

    return parties

def get_town_data(town_url: str) -> dict[str, int | dict[str, int]]|None:
    """
    Získá veškerá volební data pro danou obec.

    Args:
        town_url (str): URL stránky obce.

    Returns:
        Optional[Dict[str, int | Dict[str, int]]]: Slovník s obecnými statistikami a hlasy stran,
                                                   nebo None, pokud data nejsou dostupná.
    """
    html = get_html(town_url)
    soup = BeautifulSoup(html, "html.parser")
    
    stats = get_town_stats(soup)
    if not stats:
        return None

    stats["Hlasy stran"] = get_party_votes(soup)
    return stats

def process_district(district_name: str, district_url: str) -> list[dict[str, int]]:
    """
    Zpracuje všechny obce v daném okrese.

    Args:
        district_name (str): Název okresu.
        district_url (str): URL stránky okresu.

    Returns:
        List[Dict[str, int]]: Seznam dat pro jednotlivé obce.
    """
    print(f"Zpracovávám okres: {district_name}...")
    
    district_html = get_html(district_url)
    towns = get_town_links(district_html)

    all_data = []
    all_parties = set()

    for town in towns:
        town_data = get_town_data(town["Link"])
        if town_data:
            row = {
                "Kód obce": town["Kód obce"],
                "Název obce": town["Název obce"],
                "Voliči v seznamu": town_data["Voliči v seznamu"],
                "Vydané obálky": town_data["Vydané obálky"],
                "Platné hlasy": town_data["Platné hlasy"],
            }

            for party, votes in town_data["Hlasy stran"].items():
                row[party] = votes
                all_parties.add(party)

            all_data.append(row)

    for row in all_data:
        for party in all_parties:
            row.setdefault(party, 0)

    return all_data

def save_to_csv(data: list[dict[str, int]], filename: str) -> None:
    """
    Uloží data do CSV souboru.

    Args:
        data (List[Dict[str, int]]): Data obcí.
        filename (str): Název výstupního souboru.
    """
    df = pd.DataFrame(data)
    df.sort_values(by="Název obce", inplace=True)
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"Data byla uložena do {filename}")

def main() -> None:
    """Hlavní funkce programu pro zpracování argumentů a spuštění scrappingu."""
    if len(sys.argv) != 3:
        print("Použití: python election_scraper.py 'NÁZEV OKRESU' 'VÝSTUPNÍ CSV'")
        sys.exit(1)

    district_name = sys.argv[1]
    output_file = sys.argv[2]

    main_html = get_html(MAIN_URL)
    districts = get_districts(main_html)

    if district_name not in districts:
        print(f"Okres '{district_name}' nebyl nalezen.")
        sys.exit(1)

    district_data = process_district(district_name, districts[district_name])
    save_to_csv(district_data, output_file)

if __name__ == "__main__":
    main()
