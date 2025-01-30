# Diese Datei ist ein Python-Script, welches die Preise für den Versand von Paketen in verschiedene Länder berechnet.
# Entwickelt von Jan-Ole Michael "steelcroissant", postonaut.de, Postfach 202102, 41552 Kaarst, Deutschland
# Veröffentlicht unter CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)
# https://github.com/OlMi1/versandpreise/

import requests, xmltodict, json, sys, math, time

# Diese Args können zum Teil auch per Konsole übergeben werden (Zeile 240ff)
ZIEL = "DEU" # Dreistelliger Ländercode: https://www.iban.com/country-codes
GEWICHT = 300 # g
LAENGE = 250 # Höchster Wert; mm
BREITE = 100 # Mittlerer Wert; mm
HOEHE = 30 # Kleinster Wert; mm
WRITTEN = True # Ausgeschriebene Liste oder JSON? False = JSON
LIMIT = 0 # Sortiert nach Preis - wie viele Optionen sollen ausgegeben werden? Bei WRITTEN=False wird das ignoriert, da gibt's immer alle

PAKAJOBENUTZEN = False # Soll Pakajo benutzt werden?
PRODUKTBEREICH = 16 # Für Pakajo notwendig
PAKAJOSESSION = ""
PAKAJOLABELMANDAT = "1234" # Mandat für Pakajo-Label, NICHT finale
PRIO = False # Nicht mehr Prio, sondern Pakajo-Nachetikettierung

def translateAlpha3ToAlpha2(alpha3):
    definitions = {
        "AFG": "AF",
        "ALB": "AL",
        "DZA": "DZ",
        "ASM": "AS",
        "AND": "AD",
        "AGO": "AO",
        "AIA": "AI",
        "ATG": "AG",
        "ARG": "AR",
        "ARM": "AM",
        "ABW": "AW",
        "AUS": "AU",
        "AUT": "AT",
        "AZE": "AZ",
        "BHS": "BS",
        "BHR": "BH",
        "BGD": "BD",
        "BRB": "BB",
        "BLR": "BY",
        "BEL": "BE",
        "BLZ": "BZ",
        "BEN": "BJ",
        "BMU": "BM",
        "BTN": "BT",
        "BOL": "BO",
        "BIH": "BA",
        "BWA": "BW",
        "BRA": "BR",
        "VGB": "VG",
        "BRN": "BN",
        "BGR": "BG",
        "BFA": "BF",
        "BDI": "BI",
        "KHM": "KH",
        "CMR": "CM",
        "CAN": "CA",
        "CPV": "CV",
        "CAF": "CF",
        "TCD": "TD",
        "CHL": "CL",
        "CHN": "CN",
        "HKG": "HK",
        "MAC": "MO",
        "COL": "CO",
        "COM": "KM",
        "COG": "CG",
        "CRI": "CR",
        "CIV": "CI",
        "HRV": "HR",
        "CUB": "CU",
        "CYP": "CY",
        "CZE": "CZ",
        "DNK": "DK",
        "DJI": "DJ",
        "DMA": "DM",
        "DOM": "DO",
        "ECU": "EC",
        "EGY": "EG",
        "SLV": "SV",
        "GNQ": "GQ",
        "ERI": "ER",
        "EST": "EE",
        "ETH": "ET",
        "FRO": "FO",
        "FJI": "FJ",
        "FIN": "FI",
        "FRA": "FR",
        "GUF": "GF",
        "PYF": "PF",
        "GAB": "GA",
        "GMB": "GM",
        "GEO": "GE",
        "DEU": "DE",
        "GHA": "GH",
        "GRC": "GR",
        "GRL": "GL",
        "GRD": "GD",
        "GLP": "GP",
        "GUM": "GU",
        "GTM": "GT",
        "GNB": "GW",
        "HTI": "HT",
        "HND": "HN",
        "HUN": "HU",
        "ISL": "IS",
        "IND": "IN",
        "IDN": "ID",
        "IRN": "IR",
        "IRQ": "IQ",
        "IRL": "IE",
        "ISR": "IL",
        "ITA": "IT",
        "JPN": "JP",
        "JOR": "JO",
        "KAZ": "KZ",
        "KEN": "KE",
        "KIR": "KI",
        "PRK": "KP",
        "KOR": "KR",
        "KWT": "KW",
        "KGZ": "KG",
        "LAO": "LA",
        "LVA": "LV",
        "LBN": "LB",
        "LSO": "LS",
        "LBR": "LR",
        "LBY": "LY",
        "LIE": "LI",
        "LTU": "LT",
        "LUX": "LU",
        "MDG": "MG",
        "MWI": "MW",
        "MYS": "MY",
        "MDV": "MV",
        "MLI": "ML",
        "MLT": "MT",
        "MHL": "MH",
        "MTQ": "MQ",
        "MRT": "MR",
        "MUS": "MU",
        "MEX": "MX",
        "FSM": "FM",
        "MDA": "MD",
        "MCO": "MC",
        "MNG": "MN",
        "MNE": "ME",
        "MSR": "MS",
        "MAR": "MA",
        "MOZ": "MZ",
        "MMR": "MM",
        "NAM": "NA",
        "NRU": "NR",
        "NPL": "NP",
        "NLD": "NL",
        "ANT": "AN",
        "NCL": "NC",
        "NZL": "NZ",
        "NIC": "NI",
        "NER": "NE",
        "NGA": "NG",
        "MNP": "MP",
        "NOR": "NO",
        "OMN": "OM",
        "PAK": "PK",
        "PLW": "PW",
        "PSE": "PS",
        "PAN": "PA",
        "PNG": "PG",
        "PRY": "PY",
        "PER": "PE",
        "PHL": "PH",
        "PCN": "PN",
        "POL": "PL",
        "PRT": "PT",
        "PRI": "PR",
        "QAT": "QA",
        "REU": "RE",
        "ROU": "RO",
        "RUS": "RU",
        "RWA": "RW",
        "KNA": "KN",
        "LCA": "LC",
        "VCT": "VC",
        "WSM": "WS",
        "SMR": "SM",
        "STP": "ST",
        "SAU": "SA",
        "SEN": "SN",
        "SRB": "RS",
        "SYC": "SC",
        "SLE": "SL",
        "SGP": "SG",
        "SVK": "SK",
        "SVN": "SI",
        "SLB": "SB",
        "SOM": "SO",
        "ZAF": "ZA",
        "ESP": "ES",
        "LKA": "LK",
        "SDN": "SD",
        "SUR": "SR",
        "SWZ": "SZ",
        "SWE": "SE",
        "CHE": "CH",
        "SYR": "SY",
        "TWN": "TW",
        "TJK": "TJ",
        "TZA": "TZ",
        "THA": "TH",
        "TLS": "TL",
        "TGO": "TG",
        "TON": "TO",
        "TTO": "TT",
        "TUN": "TN",
        "TUR": "TR",
        "TKM": "TM",
        "TUV": "TV",
        "UGA": "UG",
        "UKR": "UA",
        "ARE": "AE",
        "GBR": "GB",
        "USA": "US",
        "URY": "UY",
        "UZB": "UZ",
        "VUT": "VU",
        "VEN": "VE",
        "VNM": "VN",
        "VIR": "VI",
        "YEM": "YE",
        "ZMB": "ZM",
        "ZWE": "ZW"
    }
    return definitions[alpha3]

# replace the ziel, weight and so on with console given arguments if they exist
if (len(sys.argv) > 1):
    print(sys.argv) # Debug
    ZIEL = sys.argv[1]
    GEWICHT = int(sys.argv[2])
    LAENGE = int(sys.argv[3])
    BREITE = int(sys.argv[4])
    HOEHE = int(sys.argv[5])
    PRODUKTBEREICH = int(sys.argv[6])
    PRIO = sys.argv[7] == "prio"
    WRITTEN = (sys.argv[8] == "written") if (len(sys.argv) > 8) else False

if (LAENGE < BREITE): LAENGE, BREITE = BREITE, LAENGE

ZIELALPHA2 = translateAlpha3ToAlpha2(ZIEL)
FIREFOXHEADERS = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0" }
if (LIMIT <= 0): LIMIT = 999

def doDeutschePostDomesticLogicCheck(laenge, breite, hoehe, gewicht):
    return (gewicht <= 1000
        and laenge <= 353 and breite <= 250 and hoehe <= 50
        and laenge >= 100 and breite >= 70)
def getDeutschePostInfo(zielland = ZIEL, tracking = False):
    response = {}

    briefartenDeutschland = {
        "Standardbrief": {"l": 235, "b": 125, "h": 5, "g": 20, "preis": 0.95},
        "Kompaktbrief": {"l": 235, "b": 125, "h": 10, "g": 50, "preis": 1.10},
        "Großbrief": {"l": 353, "b": 250, "h": 20, "g": 500, "preis": 1.80},
        "Maxibrief": {"l": 353, "b": 250, "h": 50, "g": 1000, "preis": 2.9}
    }
    aufpreiseDeutschland = { # PRIO verschwindet '25
        "Einschreiben Einwurf": 2.35
    }

    # TODO 8.11.; Überarbeiten, prüfen, eigentlich entfernen? Warenversand intl. nun auch in der Praxis nicht mehr möglich.
    briefartenInternational = {
        "Standardbrief International": {"l": 235, "b": 125, "h": 5, "g": 20, "preis": 1.1},
        "Kompaktbrief International": {"l": 235, "b": 125, "h": 10, "g": 50, "preis": 1.7}#,
        #"Großbrief International": {"g": 500, "preis": 3.7},
    }
    aufpreiseInternational = { "Einschreiben": 3.5 }

    aufpreiskosten = 0
    if (zielland == "DEU"): 
        briefarten = briefartenDeutschland
        aufpreise = aufpreiseDeutschland
        if (tracking): aufpreiskosten = aufpreise["Einschreiben Einwurf"]
    else: 
        briefarten = briefartenInternational
        aufpreise = aufpreiseInternational
        if (tracking): aufpreiskosten = aufpreise["Einschreiben"]

    # get the correct class and add it to responsedata["deutschepost"]
    for briefart in briefarten:
        if (briefart == "Großbrief International"):
            if (LAENGE + BREITE + HOEHE <= 900 and GEWICHT <= 500):
                return { "preis": briefarten[briefart]["preis"] + aufpreiskosten, "produkt": briefart }
            
        elif (LAENGE <= briefarten[briefart]["l"] and BREITE <= briefarten[briefart]["b"]
            and HOEHE <= briefarten[briefart]["h"] and GEWICHT <= briefarten[briefart]["g"]):
            return { "preis": briefarten[briefart]["preis"] + aufpreiskosten, "produkt": briefart }

    return response

def getPakajoInfo(MANDAT, returnOriginal = True):
    url = "https://media-sc.com/rest/rest_xml_post.php"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Accept": "*/*",
        "Accept-Language": "de",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-type": "application/x-www-form-urlencoded",
        "Origin": "https://media-sc.com",
        "Connection": "keep-alive",
        "Referer": "https://media-sc.com/index.php?page=index_main&sess="+PAKAJOSESSION+"&sprache=1&prev_page=YWRyZXNzYnVjaF91ZWJlcnNpY2h0",
        "Cookie": "cb-enabled=accepted; PHPSESSID=" + PAKAJOSESSION,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }

    data = {
        "post_uri": "/10/tools/versandoptionen_auflisten.xml",
        "id_mandant[0]": MANDAT,
        "land_iso3": ZIEL,
        "gewicht_g": GEWICHT,
        "laenge_mm": LAENGE,
        "breite_mm": BREITE,
        "hoehe_mm": HOEHE,
        "service_level": "999" if PRIO and MANDAT==PAKAJOLABELMANDAT else "0",
        "flag_inkl_mwst": "0",
        "bm_produktbereich1": PRODUKTBEREICH,
        "bm_produktbereich2": "0",
        "id_versanddienstleister": "0",
    }

    try:
        response = requests.post(url, headers=headers, data=data, timeout=5000)
    except Exception as e:
        return { "preis": 0, "produkt": str(e) }
    json_data = xmltodict.parse(response.text)["mcs_shipment_system"]

    if (returnOriginal):
        return json_data
    else:
        preis = 0
        finalpreis = 0
        produkt = ""
        try:
            preis = json_data["versandprodukte_liste"]["versandprodukt"][0]["berechnungen"]["vkp_pos"],
            produkt = json_data["versandprodukte_liste"]["versandprodukt"][0]["vd_bezeichnung"]
        except:
            try: 
                preis = json_data["versandprodukte_liste"]["versandprodukt"]["berechnungen"]["vkp_pos"],
                produkt = json_data["versandprodukte_liste"]["versandprodukt"]["vd_bezeichnung"]
            except:
                return { "preis": 0, "produkt": "/"}
        preis = float(preis[0])
        finalpreis = preis

        return { "preis": finalpreis, "produkt": produkt, "teilpreis": preis }
    
def jumingo():
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    jumingoweight = GEWICHT / 1000
    if (jumingoweight < 0.1): jumingoweight = 0.1

    curWeekday = time.localtime().tm_wday
    # current time to string following format "2024-12-01T00:00:00.000+01:00" and another one for in 30 days. Current must be monday-friday
    current = time.strftime("%Y-%m-%dT%H:%M:%S.000+01:00", time.localtime(time.time() + (7-curWeekday if curWeekday in [5, 6] else 0)*24*60*60))
    future = time.strftime("%Y-%m-%dT%H:%M:%S.000+01:00", time.localtime(time.time() + 30*24*60*60))

    data = {
        "settings": {
            "mode": "m",
            "getExternalTariffs":True
        },
        "packages": [
            {
                "weight": jumingoweight,
                "height": math.ceil(HOEHE / 10), # Nur ganze Zahlen erlaubt. Daher CEIL, um Puffer zu schaffen
                "width": math.ceil(BREITE / 10),
                "length": math.ceil(LAENGE / 10),
                "quantity": 1
            }
        ],
        "packagingTypeId": 7,
        "pickupDate": current,
        "pickupDateMode": "flex",
        "details": {
            "extra_insurance_type":None
        },
        "deliveryDate": future,
        "vat":None,
        "from_address": {
            "country": "DE",
            "state":None
        },
        "to_address": {
            "country": translateAlpha3ToAlpha2(ZIEL),
            "state":None,
            "emailDelivery": "",
            "settings": {}
        },
        "filterData": {
            "deliveryTimeUntil": 0,
            "options": [],
            "packageTypes": 7,
            "priceMax":None,
            "shipperGroups": [],
            "shippingType":None,
            "tariffTypes": [],
            "timeMin": 0,
            "timeMax": 1440,
            "transitTimeMax":None,
            "sortTariffsBy": "best_offer_asc",
            "jumOnly":False,
            "showPricesWithVat":True
        },
        "customs_invoice": {
            "invoiceNumber":None,
            "invoiceDate":None,
            "currency": "EUR",
            "exportReason":None,
            "remarks":None,
            "lineItems": [
                {
                    "content":None,
                    "quantity":None,
                    "unitOfMeasurement": "PCS",
                    "hsTariffNumber":None,
                    "manufacturingCountry":None,
                    "netWeight":None,
                    "value":None
                }
            ]
        },
        "billing_address": {
            "company": "",
            "companyPersonal": "",
            "name": "",
            "street": "",
            "street2": "",
            "zip": "",
            "city": "",
            "country": "",
            "state":None,
            "phone": ""
        }
    }

    try:
        response = requests.post('https://www.jumingo.com/app/shipment-rates', headers=headers, data=json.dumps(data), timeout=5000)
    except Exception as e:
        return { "preis": 0, "produkt": str(e) }

    tarriffone = response.json()["tariffs"][0]
    return { "preis": tarriffone["price_brutto"], "produkt":  tarriffone["shipper"]["name"]}

def getHermesInfo():
    data = requests.get(f'https://www.myhermes.de/services/order/api/formconfig?country={ZIELALPHA2}', headers=FIREFOXHEADERS)
    if (data.status_code == 200):
        if (len(data.text) > 10):
            data = data.json()["prices"]
            measuredLength = (LAENGE + HOEHE) / 10
            
            dataResult = { "preis": 999, "produkt": "Hermes nicht erfolgreich" }
            for product in data:
                productPrice = product["amountInMinor"]
                if(productPrice == 0): continue

                productName = product["item"]["name"]
                try:
                    features = product["item"]["features"]
                except:
                    continue

                for feature in features:
                    if (feature["key"] == "SUMMAXCM"):
                        if  (int(feature["value"]) >= measuredLength and productPrice < dataResult["preis"]):
                            dataResult = { "preis": productPrice / 100, "produkt": productName }

            return dataResult
    { "preis": 999, "produkt": "Hermes nicht erfolgreich" }

def getGLSInfo():
    glserr = { "preis": 999, "produkt": "GLS nicht erfolgreich" }
    data = requests.get(f"https://web.glsde.app/api/v1/shipping/destination-countries/{ZIELALPHA2}/prices", headers=FIREFOXHEADERS)
    if (data.status_code == 200):
        data = data.json()["prices"][0]
        if (data["destinationType"] == "HOME"): data = data["pricesPerSize"]
        else: return glserr

        maxSizes = { "XS": 35, "S": 50, "M": 70, "L": 90 } # längste + kürzeste, cm; XL nicht unterstützt, zu faul
        measuredLength = (LAENGE + HOEHE) / 10

        neededSize = ""
        for size in maxSizes:
            if (measuredLength <= maxSizes[size]):
                neededSize = size
                break
        if (neededSize == ""): return glserr

        for size in data:
            if (size["size"] == neededSize):
                return { "preis": size["price"]["priceMinorUnits"] / 100, "produkt": "GLS " + neededSize }
    return glserr

def checkSendcloudWarenpost():
    if (LAENGE <= 353 and BREITE <= 250 and HOEHE <= 80 and GEWICHT <= 1000 and ZIEL=="DEU"):
        return { "preis": 3.4, "produkt": "SC Warenpost" }
    return { "preis": 999, "produkt": "SC Warenpost" }

isTracked = PRODUKTBEREICH in [16, 32, 1073741824]

responsedata = {}
if (PAKAJOBENUTZEN):
    if (PRIO): # changed to pakajo routed
        responsedata["pakajo_routed"] = getPakajoInfo(1822, False)
    responsedata["pakajo_final"] = getPakajoInfo(1823, False)
responsedata["jumingo_Exp."] = jumingo()
if (ZIEL=="DEU"): responsedata["sendcloud"] = checkSendcloudWarenpost()
responsedata["hermes"] = getHermesInfo()
responsedata["gls"] = getGLSInfo()
# responsedata["dpd"] = getDPDInfo() Ist mir zu schwer. Wer eine API kennt, gerne hinzufügen. Ist sonst auch indirekt bei Pakajo, aber ist teurer als direkt...

deutschepost = getDeutschePostInfo(ZIEL, isTracked)
if (deutschepost): responsedata["deutschepost"] = deutschepost

if (WRITTEN):
    try:
        # sort resultdata by price.
        responsedata = dict(sorted(responsedata.items(), key=lambda item: item[1]["preis"]))
        # only keep the first 4 items
        responsedata = dict(list(responsedata.items())[:LIMIT]) #[:LIMIT]
    except:
        # print erroring data
        print(json.dumps(responsedata))

    resultstr = ""
    print("START") # Um via Konsolenzugriff Debug und Output zu trennen
    for key in responsedata:
        resultdata = responsedata[key]
        
        if ("preis" not in resultdata): continue
        if (resultdata["preis"] == 0): continue

        resultstr += f'{key.replace("_", " ").capitalize()}: {format(resultdata["preis"], ".2f")}€\n'
    # Letzte Zeile (leer) entfernen und ab gehts
    print(resultstr[:-1])
else:
    print(json.dumps(responsedata))
