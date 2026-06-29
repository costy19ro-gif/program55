import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime, timedelta
import time

st.set_page_config(page_title="BetMachine Pro 55 ULTRA", layout="wide")

# ---------------------------------------------------------
# AUTO-REFRESH JSON LOCAL (Zonă securizată împotriva erorilor)
# ---------------------------------------------------------
def auto_refresh_json(path, interval_sec=300):
    last_update = 0
    data_cache = None
    while True:
        if time.time() - last_update > interval_sec:
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                        if not content:
                            data_cache = {"ligi": []}
                        else:
                            data_cache = json.loads(content)
                    last_update = time.time()
                    st.toast("🔁 Datele au fost reîncărcate automat din fișierul local.")
                except (json.JSONDecodeError, FileNotFoundError, PermissionError):
                    # Dacă fișierul este corupt, parțial scris sau gol, nu crăpăm aplicația
                    if data_cache is None:
                        data_cache = {"ligi": []}
            else:
                data_cache = {"ligi": []}
        yield data_cache

json_path = "scores24.json"
json_stream = auto_refresh_json(json_path)

try:
    scores24_data = next(json_stream)
except StopIteration:
    scores24_data = {"ligi": []}

# Verificare de siguranță pentru structura JSON-ului
if not scores24_data or "ligi" not in scores24_data or len(scores24_data["ligi"]) == 0:
    st.error("❌ Fișierul JSON Scores24 este gol sau nu a fost găsit încă. Așteaptă rularea scraper-ului.")
    st.stop()

st.title("🔥 BetMachine Pro 55 ULTRA")
st.success("✅ JSON Scores24 încărcat cu succes")

# ---------------------------------------------------------
# SELECTOR DE ZI
# ---------------------------------------------------------
zile_disponibile = sorted({m["data"] for liga in scores24_data["ligi"] for m in liga.get("meciuri", []) if "data" in m})
if not zile_disponibile:
    st.warning("⚠️ Nu s-au găsit zile valabile în meciurile din fișierul JSON.")
    st.stop()

zi_aleasa = st.selectbox("📅 Alege ziua", zile_disponibile)

# ---------------------------------------------------------
# EXTRAGERE AUTOMATĂ MECIURI (2/zi × 3 zile) PENTRU AFIȘARE
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

st.header("📋 Meciuri extrase automat (fără API) — până la 6 meciuri")
for m in meciuri_locale:
    st.write(
        f"🏆 {m['liga']} | {m['data']} {m['ora']} | "
        f"{m['home']} vs {m['away']} | "
        f"GG={m['trenduri'].get('gg', 0)} | "
        f"O2.5={m['trenduri'].get('over25', 0)} | "
        f"O1.5={m['trenduri'].get('over15', 0)} | "
        f"HT O0.5={m['trenduri'].get('ht_over05', 0)} | "
        f"1={m['cote'].get('home', 0)} X={m['cote'].get('draw', 0)} 2={m['cote'].get('away', 0)}"
    )

# ---------------------------------------------------------
# FUNCȚII PREDICȚII PENTRU BILETUL ULTRA
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
    c_home = c.get("home", 0.0)
    c_draw = c.get("draw", 0.0)
    c_away = c.get("away", 0.0)

    score_home = (
        form_home * 0.4 +
        gh_for * 0.2 -
        gh_against * 0.1 +
        gg_prob * 0.1 +
        over25_prob * 0.1 +
        h2h_over25 * 0.1
    )

    score_away = (
        form_away * 0.4 +
        ga_for * 0.2 -
        ga_against * 0.1 +
        gg_prob * 0.1 +
        over25_prob * 0.1 +
        h2h_gg * 0.1
    )

    return {
        "score_home": score_home,
        "score_away": score_away,
        "gg_prob": gg_prob,
        "over25_prob": over25_prob,
        "over15_prob": over15_prob,
        "ht_over05_prob": ht_over05_prob,
        "cote_home": c_home,
        "cote_draw": c_draw,
        "cote_away": c_away,
    }

def build_ultra_ticket(matches, min_gg=0.65, min_over25=0.60):
    bilete_ultra = []
    bilete_ultra_plus = []

    for m in matches:
        p = ultra_predict(m)

        if p["gg_prob"] >= min_gg or p["over25_prob"] >= min_over25:
            bilete_ultra.append({
                "meci": f"{m.get('home', '?')} vs {m.get('away', '?')}",
                "gg_prob": round(p["gg_prob"], 2),
                "over25_prob": round(p["over25_prob"], 2),
                "over15_prob": round(p["over15_prob"], 2),
                "ht_over05_prob": round(p["ht_over05_prob"], 2),
                "cote_home": p["cote_home"],
                "cote_draw": p["cote_draw"],
                "cote_away": p["cote_away"],
            })

        if p["score_home"] > p["score_away"] and p["cote_home"] >= 2.00:
            bilete_ultra_plus.append({
                "tip": "1 (value)",
                "meci": f"{m.get('home', '?')} vs {m.get('away', '?')}",
                "score": round(p["score_home"], 2),
                "cota": p["cote_home"],
            })
        elif p["score_away"] > p["score_home"] and p["cote_away"] >= 2.50:
            bilete_ultra_plus.append({
                "tip": "2 (value)",
                "meci": f"{m.get('home', '?')} vs {m.get('away', '?')}",
                "score": round(p["score_away"], 2),
                "cota": p["cote_away"],
            })

    return bilete_ultra, bilete_ultra_plus

st.header("🎯 Bilet ULTRA (ziua aleasă)")

for liga in scores24_data.get("ligi", []):
    meciuri_filtrate = [m for m in liga.get("meciuri", []) if m.get("data") == zi_aleasa]
    if not meciuri_filtrate:
        continue

    st.subheader(f"🏆 {liga.get('liga', 'Necunoscută')} — {zi_aleasa}")

    bilete_ultra, bilete_ultra_plus = build_ultra_ticket(meciuri_filtrate)

    if bilete_ultra:
        df = pd.DataFrame(bilete_ultra)

        for b in bilete_ultra:
            st.write(
                f"**{b['meci']}** | "
                f"GG={b['gg_prob']} | "
                f"O2.5={b['over25_prob']} | "
                f"O1.5={b['over15_prob']} | "
                f"HT O0.5={b['ht_over05_prob']} | "
                f"1={b['cote_home']} X={b['cote_draw']} 2={b['cote_away']}"
            )

        st.subheader("📊 Statistici ligă")
        st.line_chart(df[["gg_prob", "over25_prob", "over15_prob"]])

    st.subheader("⚡ Bilet ULTRA+ (value bets)")
    if bilete_ultra_plus:
        for b in bilete_ultra_plus:
            st.write(
                f"**{b['tip']}** | {b['meci']} | scor={b['score']} | cota={b['cota']}"
            )
    else:
        st.info("Nu s-au găsit oportunități de tip value bet pentru această ligă.")

# ---------------------------------------------------------
# GENERATOR BILET DIN LIGI NORMALE (FĂRĂ CUPA MONDIALĂ)
# ---------------------------------------------------------
def filtreaza_ligi_fara_worldcup(scores_data):
    ligi_filtrate = []
    for liga in scores_data.get("ligi", []):
        nume = liga.get("liga", "")
        if ("World Cup" in nume) or ("CM" in nume) or ("Cupa Mondială" in nume):
            continue
        ligi_filtrate.append(liga)
    return ligi_filtrate

def selecteaza_meciuri_valide(ligi, cota_minima=1.28):
    meciuri_valide = []
    for liga in ligi:
        for m in liga.get("meciuri", []):
            c = m.get("cote", {})
            # Verificăm dacă măcar una dintre cote depășește pragul stabilit
            if (
                c.get("gg", 0) >= cota_minima or
                c.get("over25", 0) >= cota_minima or
                c.get("home", 0) >= cota_minima or
                c.get("away", 0) >= cota_minima or
                c.get("draw", 0) >= cota_minima
            ):
                meciuri_valide.append({
                    "liga": liga.get("liga", "Necunoscută"),
                    "home": m.get("home", "?"),
                    "away": m.get("away", "?"),
                    "data": m.get("data", ""),
                    "cote": c
                })
    return meciuri_valide

# Procesarea și afișarea listei curățate de meciuri
st.markdown("---")
st.header("🎟️ Meciuri Filtre Ligi Normale (Cote >= 1.28)")

