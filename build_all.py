# -*- coding: utf-8 -*-
"""
Buduje ostateczny plik data.json ze wszystkimi krajami:
- kraje geograficzne z pełnymi tabelami kodów (PL, DE, AT, CZ, SK, RO, BG, HR, SI, GR, IE, GB, UA, BY)
- kraje niegeograficzne (z krótką notatką historyczną)
"""
import csv, json

def load_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

countries = {}

# ---------- POLSKA ----------
with open("data/poland.json", encoding="utf-8") as f:
    pl_entries = json.load(f)
with open("data/poland_cities_index.json", encoding="utf-8") as f:
    pl_cities_index = json.load(f)
countries["PL"] = {
    "name": "Polska",
    "flag": "🇵🇱",
    "type": "geographic",
    "level": "powiat / miasto na prawach powiatu",
    "plateFormat": "2-3 litery (prefiks regionu) + 4-5 znaków (cyfry/litery)",
    "parseNote": "Prefiks to 2 lub 3 pierwsze znaki (litery) tablicy, przed spacją/myślnikiem.",
    "entries": [
        {"codes": e["codes"], "location": e["name"], "region": e["voivodeship"], "unit": e["type"]}
        for e in pl_entries
    ],
    # miasta NIE będące same w sobie powiatem (ani miastem na prawach powiatu) -
    # używane tylko do wyszukiwania odwrotnego (miasto -> kod powiatu, w którym leży)
    "citiesIndex": pl_cities_index,
}

# ---------- NIEMCY ----------
de_rows = load_csv("data/germany_kfz_codes.csv")
countries["DE"] = {
    "name": "Niemcy",
    "flag": "🇩🇪",
    "type": "geographic",
    "level": "Kreis / kreisfreie Stadt (powiat / miasto na prawach powiatu)",
    "plateFormat": "1-3 litery (kod miasta/powiatu) + 1-2 litery + 1-4 cyfry, np. M-AB 123",
    "parseNote": "Prefiks to litery przed myślnikiem/spacją, na początku tablicy.",
    "entries": [
        {"codes": [r["code"]], "location": r["ort_landkreis"], "region": r["bundesland"], "unit": ""}
        for r in de_rows
    ],
}

# ---------- AUSTRIA ----------
at_rows = load_csv("data/austria_kennzeichen_codes.csv")
countries["AT"] = {
    "name": "Austria",
    "flag": "🇦🇹",
    "type": "geographic",
    "level": "Bezirk / Statutarstadt (powiat / miasto statutarne)",
    "plateFormat": "1-2 litery (kod powiatu) + 1-4 litery + 1-4 cyfry, np. W 12345A",
    "parseNote": "Prefiks to litery przed pierwszą cyfrą/spacją.",
    "entries": [
        {"codes": [r["code"]], "location": r["place"], "region": r["state"], "unit": r.get("notes", "")}
        for r in at_rows if r["place"]
    ],
}

# ---------- CZECHY ----------
cz_modern = load_csv("data/czech_kraj_modern_codes.csv")
cz_hist = load_csv("data/czech_okres_historical_codes.csv")
countries["CZ"] = {
    "name": "Czechy",
    "flag": "🇨🇿",
    "type": "geographic",
    "level": "kraj (region) - obecnie; dawniej okres (powiat/miasto) do 2001",
    "plateFormat": "1 litera (kod kraju, obecnie) + 1 cyfra + 3 cyfry + 2 litery, np. 1A2 3456",
    "parseNote": "Obecny system (od 2001) koduje w PIERWSZEJ literze tylko kraj (region), nie miasto. Starsze pojazdy (sprzed 2001) mogą mieć zachowany dawny 2-literowy kod okresu (powiatu/miasta).",
    "entries": [
        {"codes": [r["code"]], "location": r["kraj_region"], "region": "", "unit": "kraj (region, system aktualny)"}
        for r in cz_modern
    ],
    "historicalEntries": [
        {"codes": [r["code"]], "location": r["okres_mesto"], "region": r.get("kraj_region_today", ""), "unit": "okres (system 1960-2001)"}
        for r in cz_hist if r["okres_mesto"] and "government" not in r["okres_mesto"].lower()
    ],
}

# ---------- SŁOWACJA ----------
sk_rows = load_csv("data/slovakia_okres_codes_expanded.csv")
countries["SK"] = {
    "name": "Słowacja",
    "flag": "🇸🇰",
    "type": "geographic",
    "level": "okres (powiat)",
    "plateFormat": "2 litery (kod okresu) + 3 cyfry + 2 litery, np. BA123AB",
    "parseNote": "Prefiks to pierwsze 2 litery tablicy. Uwaga: od ok. 2022/2023 dla części nowych rejestracji wprowadzono też kody ogólnokrajowe niezwiązane z okresem, ale większość pojazdów na drogach nadal ma kod okresu.",
    "entries": [
        {"codes": [r["code"]], "location": r["okres"], "region": r.get("kraj_region", ""), "unit": "okres"}
        for r in sk_rows
    ],
}

# ---------- RUMUNIA ----------
ro_codes = {
    "AB": "Alba", "AG": "Argeș", "AR": "Arad", "B": "Bukareszt", "BC": "Bacău",
    "BH": "Bihor", "BN": "Bistrița-Năsăud", "BR": "Brăila", "BT": "Botoșani",
    "BV": "Brașov", "BZ": "Buzău", "CJ": "Cluj", "CL": "Călărași", "CS": "Caraș-Severin",
    "CT": "Constanța", "CV": "Covasna", "DB": "Dâmbovița", "DJ": "Dolj", "GJ": "Gorj",
    "GL": "Galați", "GR": "Giurgiu", "HD": "Hunedoara", "HR": "Harghita", "IF": "Ilfov",
    "IL": "Ialomița", "IS": "Iași", "MH": "Mehedinți", "MM": "Maramureș", "MS": "Mureș",
    "NT": "Neamț", "OT": "Olt", "PH": "Prahova", "SB": "Sibiu", "SJ": "Sălaj",
    "SM": "Satu Mare", "SV": "Suceava", "TL": "Tulcea", "TM": "Timiș", "TR": "Teleorman",
    "VL": "Vâlcea", "VN": "Vrancea", "VS": "Vaslui",
}
countries["RO"] = {
    "name": "Rumunia",
    "flag": "🇷🇴",
    "type": "geographic",
    "level": "județ (okręg/powiat)",
    "plateFormat": "1-2 litery (kod okręgu) + 2 cyfry + 3 litery, np. CJ 12 ABC (Bukareszt: B 12 ABC lub B 123 ABC)",
    "parseNote": "Prefiks to litery przed pierwszą spacją/cyfrą.",
    "entries": [{"codes": [c], "location": n, "region": "", "unit": "județ"} for c, n in ro_codes.items()],
}

# ---------- BUŁGARIA ----------
bg_codes = {
    "А": "Burgas", "В": "Warna", "ВН": "Widin", "ВР": "Wraca", "ВТ": "Wielkie Tyrnowo",
    "Е": "Błagojewgrad", "ЕВ": "Gabrowo", "ЕН": "Plewen", "К": "Kyrdżali", "КН": "Kiustendił",
    "М": "Montana", "Н": "Szumen", "ОВ": "Łoweč", "Р": "Ruse", "РА": "Pazardżik",
    "РВ": "Płowdiw", "РК": "Pernik", "РР": "Razgrad", "С": "Sofia (miasto)", "СА": "Sofia (miasto)",
    "СВ": "Sofia (miasto)", "СН": "Sliwen", "СМ": "Smolan", "СО": "Sofia (obwód)",
    "СС": "Silistra", "СТ": "Stara Zagora", "Т": "Tyrgowiszte", "ТХ": "Dobricz",
    "У": "Jambol", "Х": "Chaskowo",
}
countries["BG"] = {
    "name": "Bułgaria",
    "flag": "🇧🇬",
    "type": "geographic",
    "level": "obłast (region, miejsce PIERWSZEJ rejestracji)",
    "plateFormat": "1-2 litery cyrylicy (kod obłasti) + 4 cyfry + 2 litery, np. СВ 1234 АВ",
    "parseNote": "Kod to litery cyrylicy na początku tablicy. Od 2019 kod nie musi się zmieniać przy sprzedaży/przeprowadzce, więc wskazuje miejsce PIERWSZEJ rejestracji pojazdu, niekoniecznie obecne.",
    "entries": [{"codes": [c], "location": n, "region": "", "unit": "obłast"} for c, n in bg_codes.items()],
}

# ---------- CHORWACJA ----------
hr_rows = load_csv("data/croatia_codes.csv")
countries["HR"] = {
    "name": "Chorwacja",
    "flag": "🇭🇷",
    "type": "geographic",
    "level": "miasto / żupania",
    "plateFormat": "2 litery (kod miasta) + 3-4 cyfry + 1-2 litery, np. ZG 1234-AB",
    "parseNote": "Prefiks to pierwsze 2 litery tablicy.",
    "entries": [
        {"codes": [r["code"]], "location": r["city_or_region"], "region": "", "unit": ""}
        for r in hr_rows
    ],
}

# ---------- SŁOWENIA ----------
si_codes = {
    "CE": "Celje", "GO": "Nova Gorica", "KK": "Krško", "KP": "Koper", "KR": "Kranj",
    "LJ": "Ljubljana", "MB": "Maribor", "MS": "Murska Sobota", "NM": "Novo Mesto",
    "PO": "Postojna", "SG": "Slovenj Gradec",
}
countries["SI"] = {
    "name": "Słowenia",
    "flag": "🇸🇮",
    "type": "geographic",
    "level": "miasto / region rejestracyjny",
    "plateFormat": "2 litery (kod miasta) + 3-4 znaki + 1-2 litery, np. LJ AB-123",
    "parseNote": "Prefiks to pierwsze 2 litery tablicy.",
    "entries": [{"codes": [c], "location": n, "region": "", "unit": ""} for c, n in si_codes.items()],
}

# ---------- GRECJA ----------
gr_rows = load_csv("data/greece_codes.csv")
countries["GR"] = {
    "name": "Grecja",
    "flag": "🇬🇷",
    "type": "geographic",
    "level": "prefektura (nomos)",
    "plateFormat": "1-3 litery greckie (przypominające łacińskie) + 4 cyfry, np. ΑΒΓ-1234",
    "parseNote": "Prefiks to litery na początku tablicy (tylko znaki wizualnie podobne do łacińskich: Α,Β,Ε,Ζ,Η,Ι,Κ,Μ,Ν,Ο,Ρ,Τ,Υ,Χ).",
    "entries": [
        {"codes": [r["code"]], "location": r["prefecture"], "region": "", "unit": ""}
        for r in gr_rows
    ],
}

# ---------- IRLANDIA ----------
ie_codes = {
    "C": "Cork", "CE": "Clare", "CN": "Cavan", "CW": "Carlow", "D": "Dublin",
    "DL": "Donegal", "G": "Galway", "KE": "Kildare", "KK": "Kilkenny", "KY": "Kerry",
    "L": "Limerick", "LD": "Longford", "LH": "Louth", "LM": "Leitrim", "LS": "Laois",
    "MH": "Meath", "MN": "Monaghan", "MO": "Mayo", "OY": "Offaly", "RN": "Roscommon",
    "SO": "Sligo", "T": "Tipperary", "W": "Waterford", "WH": "Westmeath",
    "WX": "Wexford", "WW": "Wicklow",
}
countries["IE"] = {
    "name": "Irlandia",
    "flag": "🇮🇪",
    "type": "geographic",
    "level": "hrabstwo (county)",
    "plateFormat": "2 cyfry (rok) + 1 litera (półrocze) + 1-2 litery (kod hrabstwa) + cyfry, np. 231-D-12345",
    "parseNote": "Kod hrabstwa znajduje się w środkowej części tablicy, po roku/półroczu, przed numerem sekwencyjnym.",
    "entries": [{"codes": [c], "location": n, "region": "", "unit": "hrabstwo"} for c, n in ie_codes.items()],
}

# ---------- WIELKA BRYTANIA ----------
gb_codes = {
    "A": "Anglia Wschodnia (Peterborough / Norwich / Ipswich)",
    "B": "Birmingham",
    "C": "Walia (Cardiff / Swansea / Bangor)",
    "D": "Deeside – Shrewsbury (Chester / Shrewsbury)",
    "E": "Essex (Chelmsford)",
    "F": "Forest & Fens (Nottingham / Lincoln)",
    "G": "Garden of England (Maidstone / Brighton)",
    "H": "Hampshire – Dorset (Bournemouth / Portsmouth)",
    "K": "Borehamwood / Northampton",
    "L": "Londyn (Wimbledon / Borehamwood / Sidcup)",
    "M": "Manchester – Merseyside",
    "N": "Północna Anglia (Newcastle / Stockton)",
    "O": "Oxford",
    "P": "Preston / Carlisle",
    "R": "Reading",
    "S": "Szkocja (Glasgow / Edinburgh / Dundee / Aberdeen / Inverness)",
    "V": "Severn Valley (Worcester)",
    "W": "Zachodnia Anglia (Exeter / Truro / Bristol)",
    "Y": "Yorkshire (Leeds / Sheffield / Beverley)",
}
countries["GB"] = {
    "name": "Wielka Brytania",
    "flag": "🇬🇧",
    "type": "geographic",
    "level": "region DVLA ('local memory tag')",
    "plateFormat": "2 litery (region) + 2 cyfry (wiek) + 3 litery, np. AB12 CDE",
    "parseNote": "Prefiks to pierwsza litera dwuliterowego kodu na początku tablicy (druga litera precyzuje lokalne biuro DVLA w obrębie regionu). Irlandia Północna ma odrębny system bez kodów regionalnych (format np. XIL 1234).",
    "entries": [{"codes": [c], "location": n, "region": "", "unit": ""} for c, n in gb_codes.items()],
}

# ---------- UKRAINA ----------
ua_codes = {
    "AA": "Kijów (miasto)", "KA": "Kijów (miasto)", "TA": "Kijów (miasto)", "TT": "Kijów (miasto)",
    "AI": "obwód kijowski", "KI": "obwód kijowski", "TI": "obwód kijowski", "ME": "obwód kijowski",
    "AB": "obwód winnicki", "KB": "obwód winnicki", "MM": "obwód winnicki", "OK": "obwód winnicki",
    "AC": "obwód wołyński", "KC": "obwód wołyński", "CM": "obwód wołyński", "TC": "obwód wołyński",
    "AE": "obwód dniepropetrowski", "KE": "obwód dniepropetrowski", "RR": "obwód dniepropetrowski", "MI": "obwód dniepropetrowski",
    "AH": "obwód doniecki", "KH": "obwód doniecki", "TH": "obwód doniecki", "MH": "obwód doniecki",
    "AM": "obwód żytomierski", "KM": "obwód żytomierski", "TM": "obwód żytomierski", "MB": "obwód żytomierski",
    "AO": "obwód zakarpacki", "KO": "obwód zakarpacki", "MT": "obwód zakarpacki", "MO": "obwód zakarpacki",
    "AP": "obwód zaporoski", "KP": "obwód zaporoski", "TP": "obwód zaporoski", "MP": "obwód zaporoski",
    "AT": "obwód iwanofrankiwski", "KT": "obwód iwanofrankiwski", "TO": "obwód iwanofrankiwski", "XC": "obwód iwanofrankiwski",
    "AX": "obwód charkowski", "KX": "obwód charkowski", "XX": "obwód charkowski", "EX": "obwód charkowski",
    "AK": "Autonomiczna Republika Krymu", "KK": "Autonomiczna Republika Krymu", "MK": "Autonomiczna Republika Krymu",
    "BA": "obwód kirowohradzki", "HA": "obwód kirowohradzki", "XA": "obwód kirowohradzki", "EA": "obwód kirowohradzki",
    "BB": "obwód ługański", "HB": "obwód ługański", "EE": "obwód ługański", "EB": "obwód ługański",
    "BC": "obwód lwowski", "HC": "obwód lwowski", "EC": "obwód lwowski",
    "BE": "obwód mikołajowski", "HE": "obwód mikołajowski", "XE": "obwód mikołajowski", "XH": "obwód mikołajowski",
    "BH": "obwód odeski", "HH": "obwód odeski", "OO": "obwód odeski", "EH": "obwód odeski",
    "BI": "obwód połtawski", "HI": "obwód połtawski", "XI": "obwód połtawski", "EI": "obwód połtawski",
    "BK": "obwód rówieński", "HK": "obwód rówieński", "XK": "obwód rówieński", "EK": "obwód rówieński",
    "BM": "obwód sumski", "HM": "obwód sumski", "XM": "obwód sumski", "EM": "obwód sumski",
    "BO": "obwód tarnopolski", "HO": "obwód tarnopolski", "XO": "obwód tarnopolski", "EO": "obwód tarnopolski",
    "BT": "obwód chersoński", "HT": "obwód chersoński", "XT": "obwód chersoński", "ET": "obwód chersoński",
    "BX": "obwód chmielnicki", "HX": "obwód chmielnicki", "OX": "obwód chmielnicki", "PX": "obwód chmielnicki",
    "CA": "obwód czerkaski", "IA": "obwód czerkaski", "OA": "obwód czerkaski", "PA": "obwód czerkaski",
    "CB": "obwód czernihowski", "IB": "obwód czernihowski", "OB": "obwód czernihowski", "PB": "obwód czernihowski",
    "CE": "obwód czerniowiecki", "IE": "obwód czerniowiecki", "OE": "obwód czerniowiecki", "PE": "obwód czerniowiecki",
    "CH": "Sewastopol (miasto)", "IH": "Sewastopol (miasto)", "OH": "Sewastopol (miasto)", "PH": "Sewastopol (miasto)",
}
# grupujemy odwrotnie: region -> lista kodów
ua_grouped = {}
for code, region in ua_codes.items():
    ua_grouped.setdefault(region, []).append(code)

countries["UA"] = {
    "name": "Ukraina",
    "flag": "🇺🇦",
    "type": "geographic",
    "level": "obwód (region)",
    "plateFormat": "2 litery (kod obwodu) + 4 cyfry + 2 litery, np. AA 1234 BC",
    "parseNote": "Prefiks to pierwsze 2 litery tablicy (używane są tylko litery, które wyglądają jak łacińskie: A,B,C,E,H,I,K,M,O,P,T,X). Każdy obwód ma kilka generacji kodów przydzielanych w miarę wyczerpywania puli numerów.",
    "entries": [
        {"codes": sorted(codes), "location": region, "region": "", "unit": ""}
        for region, codes in ua_grouped.items()
    ],
}

# ---------- BIAŁORUŚ ----------
by_codes = {
    "1": "obwód brzeski", "2": "obwód witebski", "3": "obwód homelski",
    "4": "obwód grodzieński", "5": "obwód miński (region)", "6": "obwód mohylewski",
    "7": "Mińsk (miasto)", "8": "Mińsk (miasto) - kod rezerwowy od 2025",
    "0": "pojazdy wojskowe / MSW / straż graniczna",
}
countries["BY"] = {
    "name": "Białoruś",
    "flag": "🇧🇾",
    "type": "geographic",
    "level": "obłast (region)",
    "plateFormat": "4 cyfry + 2 litery + myślnik + 1 cyfra na końcu, np. 1234 AB-7 (dla ciężarówek: AB 1234-7)",
    "parseNote": "Kod regionu to OSTATNIA cyfra tablicy, po myślniku - nie pierwszy znak.",
    "entries": [{"codes": [c], "location": n, "region": "", "unit": ""} for c, n in by_codes.items()],
}

# ---------- KRAJE NIEGEOGRAFICZNE ----------
non_geo = {
    "FR": ("Francja", "🇫🇷", "Obecny system (SIV, format AA-123-AA) obowiązuje od 2009 r. i jest w pełni niegeograficzny - numer nie mówi nic o miejscu rejestracji. Właściciel może opcjonalnie umieścić na niebieskim pasku z boku tablicy numer departamentu, ale to tylko dekoracja, nie część numeru. System sprzed 2009 (FNI) kodował departament na końcu numeru."),
    "IT": ("Włochy", "🇮🇹", "Obecny system (AA 999 AA) obowiązuje od 1994 r. i jest niegeograficzny. System sprzed 1994 kodował prowincję 2 literami na początku tablicy."),
    "ES": ("Hiszpania", "🇪🇸", "Obecny system (1234 ABC) obowiązuje od 2000 r. i jest niegeograficzny. Systemy sprzed 2000 (do 1971 i 1971-2000) kodowały prowincję."),
    "NL": ("Holandia", "🇳🇱", "System obowiązuje od 1951 r. i jest niegeograficzny (przydział sekwencyjny). Sprzed 1951 kodowano prowincję jedną literą."),
    "BE": ("Belgia", "🇧🇪", "Obecny system (1-ABC-123) od 2010 r. Belgijskie tablice nigdy nie były geograficzne - są przypisane do właściciela, nie do miejsca rejestracji."),
    "LU": ("Luksemburg", "🇱🇺", "System od 2003 r., niegeograficzny."),
    "PT": ("Portugalia", "🇵🇹", "Obecny system (00-01-AA) od 1992 r., niegeograficzny. System sprzed 1992 dzielił kraj na 3 strefy (Południe/Lizbona, Północ/Porto, Centrum/Coimbra)."),
    "SE": ("Szwecja", "🇸🇪", "System (ABC 123) od 1973 r., niegeograficzny. Wcześniej kody liter oznaczały powiaty (län)."),
    "DK": ("Dania", "🇩🇰", "Obecny system w pełni losowy od 2012 r. Bardzo dawny system (1950-1958) kodował miasto/powiat jedną literą prefiksu."),
    "FI": ("Finlandia", "🇫🇮", "W pełni niegeograficzna od 1989 r. System 1950-1989 kodował prowincję pierwszą literą."),
    "LT": ("Litwa", "🇱🇹", "System od 2004 r., niegeograficzny. System 1990-2004 kodował okręg środkową literą (np. A-Alytus, V-Wilno)."),
    "LV": ("Łotwa", "🇱🇻", "System od 1993 r., niegeograficzny. Brak wcześniejszego systemu geograficznego (poza krótkim epizodem sowieckim 1991-93)."),
    "EE": ("Estonia", "🇪🇪", "W pełni losowa od 2019 r. (nieobowiązkowo już od 2013). Do 2013 pierwsza litera oznaczała biuro rejestracyjne/powiat."),
    "CY": ("Cypr", "🇨🇾", "System od 2013 r. (zmiana wzoru), numeracja sekwencyjna bez podziału regionalnego."),
    "MT": ("Malta", "🇲🇹", "System od 1995 r. (ZZZ 999) - pierwsza litera oznacza MIESIĄC odnowienia podatku drogowego, nie region."),
    "HU": ("Węgry", "🇭🇺", "Obecny system od lipca 2022 r. (4 litery + 3 cyfry) jest ogólnokrajowy i niegeograficzny, podobnie jak poprzedni system 1990-2022. Jedyny geograficzny system był przedwojenny (1910-1933)."),
}
for code, (name, flag, note) in non_geo.items():
    countries[code] = {
        "name": name, "flag": flag, "type": "non-geographic",
        "level": "", "plateFormat": "", "parseNote": note, "entries": [],
    }

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(countries, f, ensure_ascii=False, indent=1)

print("Kraje:", len(countries))
for code, c in countries.items():
    print(f"  {code}: {c['name']} - {c['type']} - {len(c.get('entries', []))} wpisów")
