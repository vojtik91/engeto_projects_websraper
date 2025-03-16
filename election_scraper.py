import requests
import pandas as pd
from bs4 import BeautifulSoup
import sys

MAIN_URL = 'https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ'

# Funkce pro získání HTML obsahu
def get_html(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'html.parser')

# Funkce pro získání seznamu okresů
def get_districts():
    soup = get_html(MAIN_URL)
    district_links = {}
    for row in soup.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 2:
            district_name = cells[1].text.strip()
            link_tag = cells[3].find('a')
            if link_tag and 'href' in link_tag.attrs:
                link = 'https://www.volby.cz/pls/ps2017nss/' + link_tag['href']
                district_links[district_name] = link
    return district_links

# Funkce pro získání dat z okresu (seznam obcí)
def get_town_links(district_url):
    soup = get_html(district_url)
    town_data = []
    for row in soup.find_all('tr')[2:]:
        cells = row.find_all('td')
        if len(cells) >= 2:
            link_tag = cells[0].find('a')
            if link_tag and 'href' in link_tag.attrs:
                code = link_tag.text.strip()
                name = cells[1].text.strip()
                link = 'https://www.volby.cz/pls/ps2017nss/' + link_tag['href']
                town_data.append({'Kód obce': code, 'Název obce': name, 'Link': link})
    return town_data

# Funkce pro získání dat z konkrétní obce
def get_town_data(town_url):
    soup = get_html(town_url)
    tables = soup.find_all("table")

    if len(tables) < 3:
        return None  # Pokud nejsou k dispozici tabulky, vrať None

    # Celkové informace o voličích
    stats_cells = tables[0].find_all("td")
    try:
        voters = int(stats_cells[3].text.strip().replace("\xa0", "").replace(" ", ""))
        envelopes = int(stats_cells[4].text.strip().replace("\xa0", "").replace(" ", ""))
        valid_votes = int(stats_cells[7].text.strip().replace("\xa0", "").replace(" ", ""))
    except (IndexError, ValueError):
        return None

    # Hlasy jednotlivých stran
    parties = {}
    for table in tables[1:]:  # Procházení dalších tabulek
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

    return {
        "Voliči v seznamu": voters,
        "Vydané obálky": envelopes,
        "Platné hlasy": valid_votes,
        "Hlasy stran": parties
    }

# Funkce pro vytvoření CSV souboru
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.sort_values(by="Název obce", inplace=True)  # Seřazení podle názvu obce
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"Data byla uložena do {filename}")

# Hlavní skript
if __name__ == "__main__":
    # Kontrola argumentů
    if len(sys.argv) != 3:
        print("Použití: python election_scraper.py 'NÁZEV OKRESU' 'VÝSTUPNÍ CSV'")
        sys.exit(1)

    district_name = sys.argv[1]
    output_file = sys.argv[2]

    # Získání seznamu okresů
    districts = get_districts()

    if district_name not in districts:
        print(f"Okres '{district_name}' nebyl nalezen.")
        sys.exit(1)

    district_url = districts[district_name]
    towns = get_town_links(district_url)

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

            # Přidání hlasů pro všechny strany
            for party, votes in town_data["Hlasy stran"].items():
                row[party] = votes
                all_parties.add(party)

            all_data.append(row)

    # Doplnění nul pro strany, které v některých obcích nebyly
    for row in all_data:
        for party in all_parties:
            row.setdefault(party, 0)

    # Uložení do CSV
    save_to_csv(all_data, output_file)
