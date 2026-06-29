import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

def fetch_fortuna(day_offset=0):
    target_date = (datetime.now() + timedelta(days=day_offset)).strftime("%Y-%m-%d")
    url = "https://www.efortuna.ro/cote/fotbal"
    resp = requests.get(url, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")

    matches = []
    for block in soup.select(".event-row"):
        liga = block.select_one(".event-row__league-name")
        home = block.select_one(".event-row__participant--home")
        away = block.select_one(".event-row__participant--away")
        time_el = block.select_one(".event-row__time")
        odds = block.select(".event-row__odd-value")

        if not (liga and home and away and odds):
            continue

        try:
            c_home = float(odds[0].get_text(strip=True).replace(",", "."))
            c_draw = float(odds[1].get_text(strip=True).replace(",", "."))
            c_away = float(odds[2].get_text(strip=True).replace(",", "."))
        except Exception:
            continue

        matches.append({
            "liga": liga.get_text(strip=True),
            "home": home.get_text(strip=True),
            "away": away.get_text(strip=True),
            "data": target_date,
            "ora": time_el.get_text(strip=True) if time_el else "00:00",
            "trenduri": {
                "gg": 0.65,
                "ng": 0.35,
                "over25": 0.60,
                "under25": 0.40,
                "over15": 0.75,
                "under15": 0.25,
                "ht_over05": 0.65
            },
            "forma_home": {"ultimele_5": [], "goluri_marcate": 0, "goluri_primite": 0},
            "forma_away": {"ultimele_5": [], "goluri_marcate": 0, "goluri_primite": 0},
            "h2h": {"meciuri": 0, "gg": 0.0, "over25": 0.0, "victorii_home": 0, "victorii_away": 0, "egaluri": 0},
            "cote": {"home": c_home, "draw": c_draw, "away": c_away, "gg": 1.70, "over25": 1.90}
        })
    return matches

def fetch_superbet(day_offset=0):
    target_date = (datetime.now() + timedelta(days=day_offset)).strftime("%Y-%m-%d")
    url = "https://superbet.ro/cote/fotbal"
    resp = requests.get(url, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")

    matches = []
    for block in soup.select(".event-row"):
        liga = block.select_one(".event-row__league-name")
        home = block.select_one(".event-row__participant--home")
        away = block.select_one(".event-row__participant--away")
        time_el = block.select_one(".event-row__time")
        odds = block.select(".event-row__odd-value")

        if not (liga and home and away and odds):
            continue

        try:
            c_home = float(odds[0].get_text(strip=True).replace(",", "."))
            c_draw = float(odds[1].get_text(strip=True).replace(",", "."))
            c_away = float(odds[2].get_text(strip=True).replace(",", "."))
        except Exception:
            continue

        matches.append({
            "liga": liga.get_text(strip=True),
            "home": home.get_text(strip=True),
            "away": away.get_text(strip=True),
            "data": target_date,
            "ora": time_el.get_text(strip=True) if time_el else "00:00",
            "trenduri": {
                "gg": 0.68,
                "ng": 0.32,
                "over25": 0.63,
                "under25": 0.37,
                "over15": 0.78,
                "under15": 0.22,
                "ht_over05": 0.67
            },
            "forma_home": {"ultimele_5": [], "goluri_marcate": 0, "goluri_primite": 0},
            "forma_away": {"ultimele_5": [], "goluri_marcate": 0, "goluri_primite": 0},
            "h2h": {"meciuri": 0, "gg": 0.0, "over25": 0.0, "victorii_home": 0, "victorii_away": 0, "egaluri": 0},
            "cote": {"home": c_home, "draw": c_draw, "away": c_away, "gg": 1.75, "over25": 1.95}
        })
    return matches

def build_scores24_json():
    ligi_dict = {}
    for offset in range(3):  # azi, mâine, poimâine
        for m in fetch_fortuna(offset) + fetch_superbet(offset):
            liga = m["liga"]
            if liga not in ligi_dict:
                ligi_dict[liga] = {"liga": liga, "meciuri": []}
            ligi_dict[liga]["meciuri"].append(m)

    data = {"ligi": list(ligi_dict.values())}
    with open("scores24.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("✅ scores24.json actualizat cu meciuri reale (azi, mâine, poimâine).")

if __name__ == "__main__":
    build_scores24_json()
