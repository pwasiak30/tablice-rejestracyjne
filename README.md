# 🚘 Tablice rejestracyjne — Europa

Prosta aplikacja webowa (jeden plik `index.html`, działa offline, bez backendu), która:

- **rozpoznaje lokalizację po numerze rejestracyjnym** — wybierz kraj, wpisz tablicę, dostaniesz miasto/powiat/region (tam gdzie system to umożliwia);
- **wyszukuje w drugą stronę** — wybierz kraj, wpisz nazwę miasta/powiatu/regionu, zobaczysz jakie prefiksy tam obowiązują.

## Zakres

| Kraj | Poziom szczegółowości |
|---|---|
| 🇵🇱 Polska | powiat / miasto na prawach powiatu (380 jednostek) + wyszukiwanie po dowolnym z ~953 miast leżących w powiecie ziemskim |
| 🇩🇪 Niemcy | Kreis / kreisfreie Stadt (731 kodów) |
| 🇦🇹 Austria | Bezirk / Statutarstadt |
| 🇨🇿 Czechy | kraj (region) — system obecny od 2001; + system historyczny okresów sprzed 2001 |
| 🇸🇰 Słowacja | okres (powiat) |
| 🇷🇴 Rumunia, 🇧🇬 Bułgaria, 🇭🇷 Chorwacja, 🇸🇮 Słowenia, 🇬🇷 Grecja, 🇮🇪 Irlandia, 🇬🇧 Wielka Brytania | region / prefektura / hrabstwo / miasto (w zależności od kraju) |
| 🇺🇦 Ukraina, 🇧🇾 Białoruś | obwód / obłast |
| pozostałe kraje UE (Francja, Włochy, Hiszpania, Holandia, Belgia, Luksemburg, Portugalia, Szwecja, Dania, Finlandia, Litwa, Łotwa, Estonia, Cypr, Malta, Węgry) | oznaczone jako **niegeograficzne** — obecny system tablic nie koduje miejsca rejestracji (aplikacja to wyraźnie komunikuje zamiast zgadywać) |

## Użycie

Wystarczy otworzyć `index.html` w dowolnej przeglądarce (też na telefonie) — cała aplikacja i dane są w jednym pliku, nie wymaga instalacji ani internetu.

## Struktura repo

- `index.html` — gotowa aplikacja (dane są osadzone bezpośrednio w pliku)
- `data.json` — wygenerowany plik z danymi dla wszystkich krajów (źródło dla `index.html`)
- `data/` — surowe dane źródłowe (CSV/JSON) zebrane z Wikipedii i oficjalnych przepisów
- `build_poland.py`, `build_all.py` — skrypty budujące `data.json` z surowych danych w `data/`

## Źródła danych

Głównie angielska i polska Wikipedia (strony "Vehicle registration plates of X" oraz "Tablice rejestracyjne w Polsce" / "Lista miast w województwie..."), a dla Polski dodatkowo załącznik nr 13 do rozporządzenia Ministra Infrastruktury z 8 listopada 2024 r. (Dz.U. 2024 poz. 1709).

## Zastrzeżenie

To narzędzie orientacyjne, nie oficjalna baza rządowa. Systemy tablic bywają zmieniane przez poszczególne kraje — w razie wątpliwości warto sprawdzić źródło urzędowe danego państwa. Dla kilku rzadziej używanych kodów (zwłaszcza Grecja, Chorwacja) możliwe są drobne nieścisłości.
