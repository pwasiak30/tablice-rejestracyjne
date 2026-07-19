# -*- coding: utf-8 -*-
# Buduje strukturalne dane dla Polski na podstawie zebranych informacji.
# Format linii: KOD1[,KOD2,...] | Nazwa | typ(miasto/powiat) | województwo

import json

RAW = """
# DOLNOŚLĄSKIE
DJ,VJ | Jelenia Góra | miasto | dolnośląskie
DL,VL | Legnica | miasto | dolnośląskie
DB,VB | Wałbrzych | miasto | dolnośląskie
DW,DX,VW,VX | Wrocław | miasto | dolnośląskie
DBL | bolesławiecki | powiat | dolnośląskie
DDZ | dzierżoniowski | powiat | dolnośląskie
DGL | głogowski | powiat | dolnośląskie
DGR | górowski | powiat | dolnośląskie
DJA | jaworski | powiat | dolnośląskie
DJE | karkonoski | powiat | dolnośląskie
DKA | kamiennogórski | powiat | dolnośląskie
DKL | kłodzki | powiat | dolnośląskie
DLE | legnicki | powiat | dolnośląskie
DLB | lubański | powiat | dolnośląskie
DLU | lubiński | powiat | dolnośląskie
DLW | lwówecki | powiat | dolnośląskie
DMI | milicki | powiat | dolnośląskie
DOL | oleśnicki | powiat | dolnośląskie
DOA | oławski | powiat | dolnośląskie
DPL | polkowicki | powiat | dolnośląskie
DST | strzeliński | powiat | dolnośląskie
DSR | średzki (dolnośląski) | powiat | dolnośląskie
DSW | świdnicki (dolnośląski) | powiat | dolnośląskie
DTR | trzebnicki | powiat | dolnośląskie
DBA | wałbrzyski | powiat | dolnośląskie
DWL | wołowski | powiat | dolnośląskie
DWR | wrocławski | powiat | dolnośląskie
DZA | ząbkowicki | powiat | dolnośląskie
DZG | zgorzelecki | powiat | dolnośląskie
DZL | złotoryjski | powiat | dolnośląskie

# KUJAWSKO-POMORSKIE
CB | Bydgoszcz | miasto | kujawsko-pomorskie
CG | Grudziądz | miasto | kujawsko-pomorskie
CT | Toruń | miasto | kujawsko-pomorskie
CW | Włocławek | miasto | kujawsko-pomorskie
CAL | aleksandrowski | powiat | kujawsko-pomorskie
CBR | brodnicki | powiat | kujawsko-pomorskie
CBY,CBC | bydgoski | powiat | kujawsko-pomorskie
CCH | chełmiński | powiat | kujawsko-pomorskie
CGD | golubsko-dobrzyński | powiat | kujawsko-pomorskie
CGR | grudziądzki | powiat | kujawsko-pomorskie
CIN | inowrocławski | powiat | kujawsko-pomorskie
CLI | lipnowski | powiat | kujawsko-pomorskie
CMG | mogileński | powiat | kujawsko-pomorskie
CNA | nakielski | powiat | kujawsko-pomorskie
CRA | radziejowski | powiat | kujawsko-pomorskie
CRY | rypiński | powiat | kujawsko-pomorskie
CSE | sępoleński | powiat | kujawsko-pomorskie
CSW | świecki | powiat | kujawsko-pomorskie
CTR | toruński | powiat | kujawsko-pomorskie
CTU | tucholski | powiat | kujawsko-pomorskie
CWA | wąbrzeski | powiat | kujawsko-pomorskie
CWL | włocławski | powiat | kujawsko-pomorskie
CZN | żniński | powiat | kujawsko-pomorskie

# LUBELSKIE
LB | Biała Podlaska | miasto | lubelskie
LC | Chełm | miasto | lubelskie
LU | Lublin | miasto | lubelskie
LZ | Zamość | miasto | lubelskie
LBI | bialski | powiat | lubelskie
LBL | biłgorajski | powiat | lubelskie
LCH | chełmski | powiat | lubelskie
LHR | hrubieszowski | powiat | lubelskie
LJA | janowski | powiat | lubelskie
LKS | krasnostawski | powiat | lubelskie
LKR | kraśnicki | powiat | lubelskie
LLB | lubartowski | powiat | lubelskie
LUB | lubelski | powiat | lubelskie
LLE | łęczyński | powiat | lubelskie
LLU | łukowski | powiat | lubelskie
LOP | opolski (lubelski) | powiat | lubelskie
LPA | parczewski | powiat | lubelskie
LPU | puławski | powiat | lubelskie
LRA | radzyński | powiat | lubelskie
LRY | rycki | powiat | lubelskie
LSW | świdnicki (lubelski) | powiat | lubelskie
LTM | tomaszowski (lubelski) | powiat | lubelskie
LWL | włodawski | powiat | lubelskie
LZA | zamojski | powiat | lubelskie

# LUBUSKIE
FG | Gorzów Wielkopolski | miasto | lubuskie
FZ | Zielona Góra | miasto | lubuskie
FGW | gorzowski | powiat | lubuskie
FKR | krośnieński (lubuski) | powiat | lubuskie
FMI | międzyrzecki | powiat | lubuskie
FNW | nowosolski | powiat | lubuskie
FSL | słubicki | powiat | lubuskie
FSD | strzelecko-drezdenecki | powiat | lubuskie
FSU | sulęciński | powiat | lubuskie
FSW | świebodziński | powiat | lubuskie
FWS | wschowski | powiat | lubuskie
FZI | zielonogórski | powiat | lubuskie
FZG | żagański | powiat | lubuskie
FZA | żarski | powiat | lubuskie

# ŁÓDZKIE
EL,ED | Łódź | miasto | łódzkie
EP | Piotrków Trybunalski | miasto | łódzkie
ES | Skierniewice | miasto | łódzkie
EBR | brzeziński | powiat | łódzkie
EBE | bełchatowski | powiat | łódzkie
EKU | kutnowski | powiat | łódzkie
ELA | łaski | powiat | łódzkie
ELE | łęczycki | powiat | łódzkie
ELC | łowicki | powiat | łódzkie
ELW | łódzki wschodni | powiat | łódzkie
EOP | opoczyński | powiat | łódzkie
EPA | pabianicki | powiat | łódzkie
EPJ | pajęczański | powiat | łódzkie
EPI | piotrkowski | powiat | łódzkie
EPD | poddębicki | powiat | łódzkie
ERA | radomszczański | powiat | łódzkie
ERW | rawski | powiat | łódzkie
ESI | sieradzki | powiat | łódzkie
ESK | skierniewicki | powiat | łódzkie
ETM | tomaszowski (łódzki) | powiat | łódzkie
EWI | wieluński | powiat | łódzkie
EWE | wieruszowski | powiat | łódzkie
EZD | zduńskowolski | powiat | łódzkie
EZG | zgierski | powiat | łódzkie

# MAŁOPOLSKIE
KR,KK,JR,JK | Kraków | miasto | małopolskie
KN,JN | Nowy Sącz | miasto | małopolskie
KT,JT | Tarnów | miasto | małopolskie
KBC,KBA | bocheński | powiat | małopolskie
KBR | brzeski (małopolski) | powiat | małopolskie
KCH | chrzanowski | powiat | małopolskie
KDA | dąbrowski | powiat | małopolskie
KGR | gorlicki | powiat | małopolskie
KRA,KRK | krakowski | powiat | małopolskie
KLI | limanowski | powiat | małopolskie
KMI | miechowski | powiat | małopolskie
KMY | myślenicki | powiat | małopolskie
KNS | nowosądecki | powiat | małopolskie
KNT | nowotarski | powiat | małopolskie
KOL | olkuski | powiat | małopolskie
KOS | oświęcimski | powiat | małopolskie
KPR | proszowicki | powiat | małopolskie
KSU | suski | powiat | małopolskie
KTA | tarnowski | powiat | małopolskie
KTT | tatrzański | powiat | małopolskie
KWA | wadowicki | powiat | małopolskie
KWI | wielicki | powiat | małopolskie

# MAZOWIECKIE
WA,WB,WD,WE,WF,WH,WI,WJ,WK,WN,WT,WU,WW,WX,WY | Warszawa (m.st.) | miasto | mazowieckie
WO,AO | Ostrołęka | miasto | mazowieckie
WP,AP | Płock | miasto | mazowieckie
WR,AR | Radom | miasto | mazowieckie
WS,AS | Siedlce | miasto | mazowieckie
WBR | białobrzeski | powiat | mazowieckie
WCI | ciechanowski | powiat | mazowieckie
WG | garwoliński | powiat | mazowieckie
WGS | gostyniński | powiat | mazowieckie
WGM | grodziski (mazowiecki) | powiat | mazowieckie
WGR | grójecki | powiat | mazowieckie
WKZ | kozienicki | powiat | mazowieckie
WL | legionowski | powiat | mazowieckie
WLI | lipski | powiat | mazowieckie
WLS | łosicki | powiat | mazowieckie
WMA | makowski | powiat | mazowieckie
WM | miński | powiat | mazowieckie
WML | mławski | powiat | mazowieckie
WND | nowodworski (mazowiecki) | powiat | mazowieckie
WOS | ostrołęcki | powiat | mazowieckie
WOR | ostrowski (mazowiecki) | powiat | mazowieckie
WOT | otwocki | powiat | mazowieckie
WPI,WPA,WPW,WPX | piaseczyński | powiat | mazowieckie
WPL | płocki | powiat | mazowieckie
WPN | płoński | powiat | mazowieckie
WPR,WPP,WPS | pruszkowski | powiat | mazowieckie
WPZ | przasnyski | powiat | mazowieckie
WPY | przysuski | powiat | mazowieckie
WPU | pułtuski | powiat | mazowieckie
WRA | radomski | powiat | mazowieckie
WSI | siedlecki | powiat | mazowieckie
WSE | sierpecki | powiat | mazowieckie
WSC | sochaczewski | powiat | mazowieckie
WSK | sokołowski | powiat | mazowieckie
WSZ | szydłowiecki | powiat | mazowieckie
WZ | warszawski zachodni | powiat | mazowieckie
WWE | węgrowski | powiat | mazowieckie
WWL,WV | wołomiński | powiat | mazowieckie
WWY | wyszkowski | powiat | mazowieckie
WZW | zwoleński | powiat | mazowieckie
WZU | żuromiński | powiat | mazowieckie
WZY | żyrardowski | powiat | mazowieckie

# OPOLSKIE
OP | Opole | miasto | opolskie
OB | brzeski (opolski) | powiat | opolskie
OGL | głubczycki | powiat | opolskie
OK | kędzierzyńsko-kozielski | powiat | opolskie
OKL | kluczborski | powiat | opolskie
OKR | krapkowicki | powiat | opolskie
ONA | namysłowski | powiat | opolskie
ONY | nyski | powiat | opolskie
OOL | oleski | powiat | opolskie
OPO | opolski | powiat | opolskie
OPR | prudnicki | powiat | opolskie
OST | strzelecki (opolski) | powiat | opolskie

# PODKARPACKIE
RK,YK | Krosno | miasto | podkarpackie
RP,YP | Przemyśl | miasto | podkarpackie
RZ,YZ | Rzeszów | miasto | podkarpackie
RT,YT | Tarnobrzeg | miasto | podkarpackie
RBI | bieszczadzki | powiat | podkarpackie
RBR | brzozowski | powiat | podkarpackie
RDE | dębicki | powiat | podkarpackie
RJA | jarosławski | powiat | podkarpackie
RJS | jasielski | powiat | podkarpackie
RKL | kolbuszowski | powiat | podkarpackie
RKR | krośnieński (podkarpacki) | powiat | podkarpackie
RLS | leski | powiat | podkarpackie
RLE | leżajski | powiat | podkarpackie
RLU | lubaczowski | powiat | podkarpackie
RLA | łańcucki | powiat | podkarpackie
RMI | mielecki | powiat | podkarpackie
RNI | niżański | powiat | podkarpackie
RPR | przemyski | powiat | podkarpackie
RPZ | przeworski | powiat | podkarpackie
RRS | ropczycko-sędziszowski | powiat | podkarpackie
RZE,RZZ,RZR | rzeszowski | powiat | podkarpackie
RSA | sanocki | powiat | podkarpackie
RST | stalowowolski | powiat | podkarpackie
RSR | strzyżowski | powiat | podkarpackie
RTA | tarnobrzeski | powiat | podkarpackie

# PODLASKIE
BI | Białystok | miasto | podlaskie
BL | Łomża | miasto | podlaskie
BS | Suwałki | miasto | podlaskie
BAU | augustowski | powiat | podlaskie
BIA,BIB | białostocki | powiat | podlaskie
BBI | bielski (podlaski) | powiat | podlaskie
BGR | grajewski | powiat | podlaskie
BHA | hajnowski | powiat | podlaskie
BKL | kolneński | powiat | podlaskie
BLM | łomżyński | powiat | podlaskie
BMN | moniecki | powiat | podlaskie
BSE | sejneński | powiat | podlaskie
BSI | siemiatycki | powiat | podlaskie
BSK | sokólski | powiat | podlaskie
BSU | suwalski | powiat | podlaskie
BWM | wysokomazowiecki | powiat | podlaskie
BZA | zambrowski | powiat | podlaskie

# POMORSKIE
GD,XD | Gdańsk | miasto | pomorskie
GA,XA | Gdynia | miasto | pomorskie
GS,XS | Słupsk | miasto | pomorskie
GSP,XSP | Sopot | miasto | pomorskie
GBY | bytowski | powiat | pomorskie
GCH | chojnicki | powiat | pomorskie
GCZ | człuchowski | powiat | pomorskie
GDA | gdański | powiat | pomorskie
GKA,GKY,GKZ | kartuski | powiat | pomorskie
GKS | kościerski | powiat | pomorskie
GKW | kwidzyński | powiat | pomorskie
GLE | lęborski | powiat | pomorskie
GMB | malborski | powiat | pomorskie
GND | nowodworski (pomorski) | powiat | pomorskie
GPU | pucki | powiat | pomorskie
GSL | słupski | powiat | pomorskie
GST | starogardzki | powiat | pomorskie
GSZ | sztumski | powiat | pomorskie
GTC | tczewski | powiat | pomorskie
GWE,GWO | wejherowski | powiat | pomorskie

# ŚLĄSKIE
SB | Bielsko-Biała | miasto | śląskie
SY | Bytom | miasto | śląskie
SH | Chorzów | miasto | śląskie
SC | Częstochowa | miasto | śląskie
SD | Dąbrowa Górnicza | miasto | śląskie
SG | Gliwice | miasto | śląskie
SJZ | Jastrzębie-Zdrój | miasto | śląskie
SJ | Jaworzno | miasto | śląskie
SK | Katowice | miasto | śląskie
SM | Mysłowice | miasto | śląskie
SPI | Piekary Śląskie | miasto | śląskie
SRS,SL | Ruda Śląska | miasto | śląskie
SR | Rybnik | miasto | śląskie
SI | Siemianowice Śląskie | miasto | śląskie
SO | Sosnowiec | miasto | śląskie
SW | Świętochłowice | miasto | śląskie
ST | Tychy | miasto | śląskie
SZ | Zabrze | miasto | śląskie
SZO | Żory | miasto | śląskie
SBE,SE,SBN | będziński | powiat | śląskie
SBI | bielski (śląski) | powiat | śląskie
SCI,SCN | cieszyński | powiat | śląskie
SCZ | częstochowski | powiat | śląskie
SGL | gliwicki | powiat | śląskie
SKL | kłobucki | powiat | śląskie
SLU | lubliniecki | powiat | śląskie
SMI | mikołowski | powiat | śląskie
SMY | myszkowski | powiat | śląskie
SPS | pszczyński | powiat | śląskie
SRC | raciborski | powiat | śląskie
SRB | rybnicki | powiat | śląskie
STA | tarnogórski | powiat | śląskie
SBL | bieruńsko-lędziński | powiat | śląskie
SWD,SWZ | wodzisławski | powiat | śląskie
SZA | zawierciański | powiat | śląskie
SZY | żywiecki | powiat | śląskie

# ŚWIĘTOKRZYSKIE
TK | Kielce | miasto | świętokrzyskie
TBU | buski | powiat | świętokrzyskie
TJE | jędrzejowski | powiat | świętokrzyskie
TKA | kazimierski | powiat | świętokrzyskie
TKI,TKC,TKM,TKP | kielecki | powiat | świętokrzyskie
TKN | konecki | powiat | świętokrzyskie
TOP | opatowski | powiat | świętokrzyskie
TOS | ostrowiecki | powiat | świętokrzyskie
TPI | pińczowski | powiat | świętokrzyskie
TSA | sandomierski | powiat | świętokrzyskie
TSK | skarżyski | powiat | świętokrzyskie
TST | starachowicki | powiat | świętokrzyskie
TSZ | staszowski | powiat | świętokrzyskie
TLW | włoszczowski | powiat | świętokrzyskie

# WARMIŃSKO-MAZURSKIE
NE | Elbląg | miasto | warmińsko-mazurskie
NO | Olsztyn | miasto | warmińsko-mazurskie
NBA | bartoszycki | powiat | warmińsko-mazurskie
NBR | braniewski | powiat | warmińsko-mazurskie
NDZ | działdowski | powiat | warmińsko-mazurskie
NEB | elbląski | powiat | warmińsko-mazurskie
NEL | ełcki | powiat | warmińsko-mazurskie
NGI | giżycki | powiat | warmińsko-mazurskie
NIL | iławski | powiat | warmińsko-mazurskie
NKE | kętrzyński | powiat | warmińsko-mazurskie
NLI | lidzbarski | powiat | warmińsko-mazurskie
NMR | mrągowski | powiat | warmińsko-mazurskie
NNI | nidzicki | powiat | warmińsko-mazurskie
NNM | nowomiejski | powiat | warmińsko-mazurskie
NOE | olecki | powiat | warmińsko-mazurskie
NGO | gołdapski | powiat | warmińsko-mazurskie
NOL | olsztyński | powiat | warmińsko-mazurskie
NOS,NOT,NOX | ostródzki | powiat | warmińsko-mazurskie
NPI | piski | powiat | warmińsko-mazurskie
NSZ | szczycieński | powiat | warmińsko-mazurskie
NWE | węgorzewski | powiat | warmińsko-mazurskie

# WIELKOPOLSKIE
PK,PA | Kalisz | miasto | wielkopolskie
PKO,PN | Konin | miasto | wielkopolskie
PL | Leszno | miasto | wielkopolskie
PO,PY,PX | Poznań | miasto | wielkopolskie
PCH | chodzieski | powiat | wielkopolskie
PCT | czarnkowsko-trzcianecki | powiat | wielkopolskie
PGN | gnieźnieński | powiat | wielkopolskie
PGS | gostyński | powiat | wielkopolskie
PGO | grodziski (wielkopolski) | powiat | wielkopolskie
PJA | jarociński | powiat | wielkopolskie
PKA | kaliski | powiat | wielkopolskie
PKE | kępiński | powiat | wielkopolskie
PKL | kolski | powiat | wielkopolskie
PKN | koniński | powiat | wielkopolskie
PKS | kościański | powiat | wielkopolskie
PKR | krotoszyński | powiat | wielkopolskie
PLE | leszczyński | powiat | wielkopolskie
PMI | międzychodzki | powiat | wielkopolskie
PNT | nowotomyski | powiat | wielkopolskie
POB | obornicki | powiat | wielkopolskie
POS | ostrowski (wielkopolski) | powiat | wielkopolskie
POT | ostrzeszowski | powiat | wielkopolskie
PP | pilski | powiat | wielkopolskie
PPL | pleszewski | powiat | wielkopolskie
POZ,PZ | poznański | powiat | wielkopolskie
PRA | rawicki | powiat | wielkopolskie
PSL | słupecki | powiat | wielkopolskie
PSZ | szamotulski | powiat | wielkopolskie
PSR | średzki (wielkopolski) | powiat | wielkopolskie
PSE | śremski | powiat | wielkopolskie
PTU | turecki | powiat | wielkopolskie
PWA | wągrowiecki | powiat | wielkopolskie
PWL | wolsztyński | powiat | wielkopolskie
PWR | wrzesiński | powiat | wielkopolskie
PZL | złotowski | powiat | wielkopolskie

# ZACHODNIOPOMORSKIE
ZK | Koszalin | miasto | zachodniopomorskie
ZS,ZZ | Szczecin | miasto | zachodniopomorskie
ZSW | Świnoujście | miasto | zachodniopomorskie
ZBI | białogardzki | powiat | zachodniopomorskie
ZCH | choszczeński | powiat | zachodniopomorskie
ZDR | drawski | powiat | zachodniopomorskie
ZGL | goleniowski | powiat | zachodniopomorskie
ZGY | gryficki | powiat | zachodniopomorskie
ZGR | gryfiński | powiat | zachodniopomorskie
ZKA | kamieński | powiat | zachodniopomorskie
ZKL | kołobrzeski | powiat | zachodniopomorskie
ZKO | koszaliński | powiat | zachodniopomorskie
ZLO | łobeski | powiat | zachodniopomorskie
ZMY | myśliborski | powiat | zachodniopomorskie
ZPL | policki | powiat | zachodniopomorskie
ZPY | pyrzycki | powiat | zachodniopomorskie
ZSL | sławieński | powiat | zachodniopomorskie
ZST | stargardzki | powiat | zachodniopomorskie
ZSZ | szczecinecki | powiat | zachodniopomorskie
ZSD | świdwiński | powiat | zachodniopomorskie
ZWA | wałecki | powiat | zachodniopomorskie
"""

entries = []
for line in RAW.strip().splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    codes_part, name, typ, voiv = [p.strip() for p in line.split("|")]
    codes = [c.strip() for c in codes_part.split(",")]
    entries.append({
        "codes": codes,
        "name": name,
        "type": typ,
        "voivodeship": voiv,
    })

print(f"Liczba jednostek: {len(entries)}")
total_codes = sum(len(e["codes"]) for e in entries)
print(f"Liczba kodów (wariantów): {total_codes}")

with open("data/poland.json", "w", encoding="utf-8") as f:
    json.dump(entries, f, ensure_ascii=False, indent=1)

# quick sanity check: duplicate codes
seen = {}
dupes = []
for e in entries:
    for c in e["codes"]:
        if c in seen:
            dupes.append((c, seen[c], e["name"]))
        seen[c] = e["name"]
if dupes:
    print("UWAGA - duplikaty kodów:", dupes)
else:
    print("Brak duplikatów kodów - OK")
