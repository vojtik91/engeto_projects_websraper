# engeto_projects_websraper

README – Election Scraper

========================================
📌 Popis projektu
========================================
Tento Python skript stahuje a zpracovává výsledky voleb pro zadaný okres z webu volby.cz a ukládá je do CSV souboru.

Skript:
- Stáhne výsledky pro všechny obce v zadaném okrese.
- Vytvoří tabulku s údaji o voličích a počtech hlasů pro všechny strany.
- Výsledky uloží do souboru ve formátu CSV.

========================================
🔧 Požadavky
========================================
Před spuštěním je nutné mít nainstalovaný Python (verze 3.x) a následující knihovny (viz. requirements.txt):

- requests – pro stahování HTML stránek
- pandas – pro zpracování tabulkových dat
- beautifulsoup4 – pro analýzu HTML

Pokud nejsou nainstalovány, spusťte v terminálu:

pip install -r requirements.txt

========================================
▶️ Spuštění skriptu
========================================
Skript se spouští pomocí dvou argumentů:
1. Název okresu – jméno okresu, pro který chcete získat výsledky.
2. Název výstupního souboru – soubor, do kterého se uloží výsledky (např. vysledky.csv).

Příklad spuštění:

python election_scraper.py "Prostějov" "vysledky_prostejov.csv"

Poznámka:
- Pokud uživatel nezadá oba argumenty nebo zadá neexistující okres, skript zobrazí chybovou hlášku a ukončí se.
- Výstupní soubor CSV obsahuje všechny strany, které v některé obci získaly hlasy, a je seřazen podle názvů obcí.

========================================
📂 Struktura výstupního souboru (CSV)
========================================
Výsledný soubor bude obsahovat následující sloupce:

- Kód obce
- Název obce
- Voliči v seznamu
- Vydané obálky
- Platné hlasy
- Hlasy pro jednotlivé strany

Každý řádek odpovídá jedné obci, sloupce reprezentují strany, které získaly alespoň jeden hlas.

========================================
📜 Možné chyby a jejich řešení
========================================

Problém: `ModuleNotFoundError: No module named 'requests'`
Řešení: Spusť `pip install requests`

Problém: `ModuleNotFoundError: No module named 'pandas'`
Řešení: Spusť `pip install pandas`

Problém: `ModuleNotFoundError: No module named 'bs4'`
Řešení: Spusť `pip install beautifulsoup4`

Problém: `Okres 'Prostějov' nebyl nalezen.`
Řešení: Zkontroluj správný název okresu.

========================================



Seznam okresů pro použití jako argument

========================================
📌 Formát spuštění skriptu:
========================================
python election_scraper.py "NÁZEV OKRESU" "NAZEV_SOUBORU.csv"

Například pro okres Prostějov:
python election_scraper.py "Prostějov" "vysledky_prostejov.csv"

========================================
📍 Seznam okresů (platné argumenty)
========================================

Hlavní města krajů:
- Praha
- Brno-město
- Ostrava-město
- Plzeň-město
- České Budějovice
- Hradec Králové
- Pardubice
- Liberec
- Jihlava
- Zlín
- Karlovy Vary
- Ústí nad Labem

Další okresy podle krajů:

✅ Středočeský kraj
- Benešov
- Beroun
- Kladno
- Kolín
- Kutná Hora
- Mělník
- Mladá Boleslav
- Nymburk
- Praha-východ
- Praha-západ
- Příbram
- Rakovník

✅ Jihočeský kraj
- České Budějovice
- Český Krumlov
- Jindřichův Hradec
- Písek
- Prachatice
- Strakonice
- Tábor

✅ Plzeňský kraj
- Domažlice
- Klatovy
- Plzeň-jih
- Plzeň-město
- Plzeň-sever
- Rokycany
- Tachov

✅ Karlovarský kraj
- Cheb
- Karlovy Vary
- Sokolov

✅ Ústecký kraj
- Děčín
- Chomutov
- Litoměřice
- Louny
- Most
- Teplice
- Ústí nad Labem

✅ Liberecký kraj
- Česká Lípa
- Jablonec nad Nisou
- Liberec
- Semily

✅ Královéhradecký kraj
- Hradec Králové
- Jičín
- Náchod
- Rychnov nad Kněžnou
- Trutnov

✅ Pardubický kraj
- Chrudim
- Pardubice
- Svitavy
- Ústí nad Orlicí

✅ Vysočina
- Havlíčkův Brod
- Jihlava
- Pelhřimov
- Třebíč
- Žďár nad Sázavou

✅ Jihomoravský kraj
- Blansko
- Brno-město
- Brno-venkov
- Břeclav
- Hodonín
- Vyškov
- Znojmo

✅ Olomoucký kraj
- Jeseník
- Olomouc
- Prostějov
- Přerov
- Šumperk

✅ Zlínský kraj
- Kroměříž
- Uherské Hradiště
- Vsetín
- Zlín

✅ Moravskoslezský kraj
- Bruntál
- Frýdek-Místek
- Karviná
- Nový Jičín
- Opava
- Ostrava-město

========================================
📌 Poznámky:
========================================
- Okresní názvy musí být přesné (např. "Praha-východ" místo "Praha východ").
- Pokud skript vypíše chybu "Okres nebyl nalezen.", zkontroluj správnost názvu.
- Pokud si nejsi jistý názvem okresu, podívej se na seznam výše.




