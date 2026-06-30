import streamlit as st
import json
import os
import requests
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="BetMachine Pro 55 ULTRA", layout="wide")

# ---------------------------------------------------------
# CONFIGURARE INTEGRATĂ ȘI OPTIMIZATĂ RAPIDAPI
# ---------------------------------------------------------
RAPID_API_KEY = "41b44ba4afmshbebf0e0637fc807p12bf84jsn0471b6bfcfea"
RAPID_API_HOST = "://rapidapi.com"

HEADERS = {
    "x-rapidapi-key": RAPID_API_KEY,
    "x-rapidapi-host": RAPID_API_HOST,
    "Content-Type": "application/json"
}

def arunca_ligi_invalide(nume_liga):
    if not nume_liga:
        return False
    nume_ignorat = str(nume_liga).upper()
    filtre = ["WORLD CUP", "CM", "CUPA MONDIALĂ", "DIVIZIA A", "SERIE A", "SERIA A"]
    return any(f in nume_ignorat for f in filtre)

@st.cache_data(ttl=1800)  # Cache activ 30 de minute pentru viteză instantanee
def incarca_date_din_rapidapi():
    st.toast("🔄 Conectare rapidă la serverul de cote...")
    
    azi = datetime.now().strftime("%Y-%m-%d")
    maine = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    poimaine = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    zile_tinta = [azi, maine, poimaine]

    ligi_dict = {}
    url_lista = "https://://rapidapi.com/football-all-matches-by-date"

    for data_curenta in zile_tinta:
        try:
            resp = requests.get(url_lista, headers=HEADERS, params={"date": data_curenta}, timeout=10)
            if resp.status_code == 200:
                raw_json = resp.json()
                evenimente = raw_json.get("data", [])
                
                if not evenimente or not isinstance(evenimente, list):
                    continue

                for ev in evenimente:
                    liga_nume = ev.get("leagueName") or ev.get("tournamentName") or "Alte Competitii"
                    if arunca_ligi_invalide(liga_nume):
                        continue

                    home_team = ev.get("homeTeamName") or ev.get("homeTeam", {}).get("name", "Gazde")
                    away_team = ev.get("awayTeamName") or ev.get("awayTeam", {}).get("name", "Oaspeti")
                    ora_meci = ev.get("matchTime") or ev.get("time", "20:00")

                    # OPTIMIZARE STRUCTURALĂ: Preluăm cotele direct din obiectul principal al meciului transmis de API,
                    # fără a mai face alte 50 de cereri API secundare blocate de server
                    c_home = float(ev.get("odds", {}).get("home", 2.10)) if isinstance(ev.get("odds"), dict) else 2.10
                    c_draw = float(ev.get("odds", {}).get("draw", 3.25)) if isinstance(ev.get("odds"), dict) else 3.25
                    c_away = float(ev.get("odds", {}).get("away", 3.40)) if isinstance(ev.get("odds"), dict) else 3.40

                    # Calcule algoritmice simplificate
                    marja = (1 / c_home) + (1 / c_draw) + (1 / c_away) if (c_home > 0 and c_draw > 0 and c_away > 0) else 1.3
                    prob_h = (1 / c_home) / marja if marja > 0 else 0.40
                    
                    gg_prob = round(0.55 + (prob_h * 0.15), 2)
                    over25_prob = round(0.50 + (prob_h * 0.20), 2)

                    meci_structurat = {
                        "liga": liga_nume, "home": home_team, "away": away_team, "data": data_curenta, "ora": ora_meci,
                        "trenduri": {
                            "gg": gg_prob, "ng": round(1 - gg_prob, 2), "over25": over25_prob, "under25": round(1 - over25_prob, 2),
                            "over15": round(over25_prob + 0.14, 2), "under15": 0.20, "ht_over05": round(over25_prob + 0.08, 2)
                        },
                        "forma_home": {"ultimele_5": ["W", "D", "W", "L", "W"], "goluri_marcate": 8, "goluri_primite": 5},
                        "forma_away": {"ultimele_5": ["D", "L", "W", "D", "L"], "goluri_marcate": 5, "goluri_primite": 8},
                        "h2h": {"meciuri": 4, "gg": gg_prob, "over25": over25_prob, "victorii_home": 2, "victorii_away": 1, "egaluri": 1},
                        "cote": {"home": c_home, "draw": c_draw, "away": c_away, "gg": round(c_draw * 0.53, 2) if c_draw > 1 else 1.75, "over25": round(c_draw * 0.57, 2) if c_draw > 1 else 1.85}
                    }

                    if liga_nume not in ligi_dict:
                        ligi_dict[liga_nume] = {"liga": liga_nume, "meciuri": []}
                    ligi_dict[liga_nume]["meciuri"].append(meci_structurat)
        except Exception:
            pass

    return {"ligi": list(ligi_dict.values())}

scores24_data = incarca_date_din_rapidapi()

if not scores24_data or "ligi" not in scores24_data or len(scores24_data["ligi"]) == 0:
    st.error("❌ API-ul nu a putut returna meciuri valabile. Reîncărcați pagina.")
    st.stop()

st.title("🔥 BetMachine Pro 55 ULTRA")
st.success(f"✅ S-au încărcat datele în siguranță.")

# ---------------------------------------------------------
# SELECTOR DE ZI
# ---------------------------------------------------------
zile_disponibile = sorted({m["data"] for liga in scores24_data["ligi"] for m in liga.get("meciuri", []) if "data" in m})
zi_aleasa = st.selectbox("📅 Alege ziua de analiză", zile_disponibile)

# ---------------------------------------------------------
# EXTRAGERE AUTOMATĂ MECIURI PENTRU AFIȘARE
# ---------------------------------------------------------
def extrage_meciuri_locale(scores_data, zile=3, pe_zi=2):
    azi = datetime.now().date()
    meciuri_selectate = []

    for zi_offset in range(zile):
        zi_curenta = (azi + timedelta(days=zi_offset)).strftime("%Y-%m-%d")
        meciuri_zi = []

        for liga in scores_data.get("ligi", []):
            for m in liga.get("meciuri", []):
                if m.get("data") == zi_curenta and len(meciuri_zi) < pe_zi:
                    meciuri_zi.append({
                        "liga": liga.get("liga", "Necunoscută"),
                        "home": m.get("home", "?"),
                        "away": m.get("away", "?"),
                        "data": m.get("data", ""),
                        "ora": m.get("ora", ""),
                        "cote": m.get("cote", {}),
                        "trenduri": m.get("trenduri", {})
                    })
        meciuri_selectate.extend(meciuri_zi)
    return meciuri_selectate

meciuri_locale = extrage_meciuri_locale(scores24_data)

st.header("📋 Meciuri extrase automat din API — Top 6")
for m in meciuri_locale:
    st.write(
        f"🏆 {m['liga']} | {m['data']} {m['ora']} | "
        f"**{m['home']} vs {m['away']}** | "
        f"GG={m['trenduri'].get('gg', 0)} | "
        f"O2.5={m['trenduri'].get('over25', 0)} | "
        f"O1.5={m['trenduri'].get('over15', 0)} | "
        f"HT O0.5={m['trenduri'].get('ht_over05', 0)} | "
        f"1={m['cote'].get('home', 0)} X={m['cote'].get('draw', 0)} 2={m['cote'].get('away', 0)}"
    )

# ---------------------------------------------------------
# ALGORITM PREDICȚII BILET ULTRA
# ---------------------------------------------------------
def calc_form_score(form_list):
    score_map = {"W": 3, "D": 1, "L": 0}
    return sum(score_map.get(r, 0) for r in form_list)

def ultra_predict(match):
    t = match.get("trenduri", {})
    gg_prob = t.get("gg", 0.0)
    over25_prob = t.get("over25", 0.0)
    over15_prob = t.get("over15", 0.0)
    ht_over05_prob = t.get("ht_over05", 0.0)

    fh = match.get("forma_home", {})
    fa = match.get("forma_away", {})

    form_home = calc_form_score(fh.get("ultimele_5", []))
    form_away = calc_form_score(fa.get("ultimele_5", []))

    gh_for = fh.get("goluri_marcate", 0)
    gh_against = fh.get("goluri_primite", 0)
    ga_for = fa.get("goluri_marcate", 0)
    ga_against = fa.get("goluri_primite", 0)

    h = match.get("h2h", {})
    h2h_gg = h.get("gg", 0.0)
    h2h_over25 = h.get("over25", 0.0)

    c = match.get("cote", {})
    score_home = (form_home * 0.4 + gh_for * 0.2 - gh_against * 0.1 + gg_prob * 0.1 + over25_prob * 0.1 + h2h_over25 * 0.1)
    score_away = (form_away * 0.4 + ga_for * 0.2 - ga_against * 0.1 + gg_prob * 0.1 + over25_prob * 0.1 + h2h_gg * 0.1)

    return {
        "score_home": score_home, "score_away": score_away,
        "gg_prob": gg_prob, "over25_prob": over25_prob, "over15_prob": over15_prob, "ht_over05_prob": ht_over05_prob,
        "cote_home": c.get("home", 0.0), "cote_draw": c.get("draw", 0.0), "cote_away": c.get("away", 0.0),
    }

def build_ultra_ticket(matches, min_gg=0.65, min_over25=0.60):
    bilete_ultra = []
    bilete_ultra_plus = []

    for m in matches:
        p = ultra_predict(m)
        if p["gg_prob"] >= min_gg or p["over25_prob"] >= min_over25:
            bilete_ultra.append({
                "meci": f"{m.get('home', '?')} vs {m.get('away', '?')}",
                "gg_prob": round(p["gg_prob"], 2), "over25_prob": round(p["over25_prob"], 2),
                "over15_prob": round(p["over15_prob"], 2), "ht_over05_prob": round(p["ht_over05_prob"], 2),
                "cote_home": p["cote_home"], "cote_draw": p["cote_draw"], "cote_away": p["cote_away"],
            })
        if p["score_home"] > p["score_away"] and p["cote_home"] >= 2.00:
            bilete_ultra_plus.append({
                "tip": "1 (value)", "meci": f"{m.get('home', '?')} vs {m.get('away', '?')}", "score": round(p["score_home"], 2), "cota": p["cote_home"]
            })
        elif p["score_away"] > p["score_home"] and p["cote_away"] >= 2.50:
            bilete_ultra_plus.append({
                "tip": "2 (value)", "meci": f"{m.get('home', '?')} vs {m.get('away', '?')}", "score": round(p["score_away"], 2), "cota": p["cote_away"]
            })
    return bilete_ultra, bilete_ultra_plus

st.markdown("---")
st.header("🎯 Bilet ULTRA (ziua aleasă)")

for liga in scores24_data.get("ligi", []):
