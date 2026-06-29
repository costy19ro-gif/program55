# betmachine_ultra.py

import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime, timedelta
import time

st.set_page_config(page_title="BetMachine Pro 55 ULTRA", layout="wide")

# ---------------------------------------------------------
# AUTO-REFRESH JSON LOCAL
# ---------------------------------------------------------
def auto_refresh_json(path, interval_sec=300):
    last_update = 0
    data_cache = None
    while True:
        if time.time() - last_update > interval_sec:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    data_cache = json.load(f)
                last_update = time.time()
                st.toast("🔁 Datele au fost reîncărcate automat din fișierul local.")
        yield data_cache

json_path = "scores24.json"
json_stream = auto_refresh_json(json_path)
scores24_data = next(json_stream)

if not scores24_data:
    st.error("❌ Nu am găsit fișierul JSON Scores24")
    st.stop()

st.title("🔥 BetMachine Pro 55 ULTRA")
st.success("✅ JSON Scores24 încărcat cu succes")

# ---------------------------------------------------------
# SELECTOR DE ZI
# ---------------------------------------------------------
zile_disponibile = sorted({m["data"] for liga in scores24_data["ligi"] for m in liga["meciuri"]})
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

        for liga in scores_data["ligi"]:
            for m in liga["meciuri"]:
                if m["data"] == zi_curenta and len(meciuri_zi) < pe_zi:
                    meciuri_zi.append({
                        "liga": liga["liga"],
                        "home": m["home"],
                        "away": m["away"],
                        "data": m["data"],
                        "ora": m["ora"],
                        "cote": m["cote"],
                        "trenduri": m["trenduri"]
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

for liga in scores24_data["ligi"]:
    meciuri_filtrate = [m for m in liga["meciuri"] if m["data"] == zi_aleasa]
    if not meciuri_filtrate:
        continue

    st.subheader(f"🏆 {liga['liga']} — {zi_aleasa}")

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

    st.header("⚡ Bilet ULTRA+ (value bets)")
    for b in bilete_ultra_plus:
        st.write(
            f"**{b['tip']}** | {b['meci']} | scor={b['score']} | cota={b['cota']}"
        )

# ---------------------------------------------------------
# GENERATOR BILET DIN LIGI NORMALE (FĂRĂ CUPA MONDIALĂ)
# ---------------------------------------------------------
def filtreaza_ligi_fara_worldcup(scores_data):
    ligi_filtrate = []
    for liga in scores_data["ligi"]:
        nume = liga["liga"]
        if ("World Cup" in nume) or ("CM" in nume) or ("Cupa Mondială" in nume):
            continue
        ligi_filtrate.append(liga)
    return ligi_filtrate

def selecteaza_meciuri_valide(ligi, cota_minima=1.28):
    meciuri_valide = []
    for liga in ligi:
        for m in liga["meciuri"]:
            c = m.get("cote", {})
            if (
                c.get("gg", 0) >= cota_minima or
                c.get("over25", 0) >= cota_minima or
                c.get("home", 0) >= cota_minima or
                c.get("away", 0) >= cota_minima or
                c.get("draw", 0) >= cota_minima
            ):
                meciuri_valide.append({
                    "liga": liga["liga"],
                    "home": m["home"],
                    "away": m["away"],
                    "data": m["data"],
                    "ora": m["ora"],
                    "cote": c,
                    "trenduri": m["trenduri"]
                })
    return meciuri_valide

def genereaza_predictie(m):
    t = m["trenduri"]
    c = m["cote"]
    predictii = []

    if t.get("gg", 0) >= 0.65 and c.get("gg", 0) >= 1.28:
        predictii.append(("GG", c["gg"]))

    if t.get("over15", 0) >= 0.75 and c.get("over25", 0) >= 1.28:
        predictii.append(("Peste 2.5", c["over25"]))

    if t.get("over15", 0) >= 0.80:
        predictii.append(("Peste 1.5", 1.30))

    if t.get("ht_over05", 0) >= 0.70:
        predictii.append(("HT Peste 0.5", 1.35))

    if c.get("home", 0) >= 1.28 and t.get("gg", 0) < 0.50:
        predictii.append(("1", c["home"]))

    if c.get("away", 0) >= 1.28 and t.get("gg", 0) < 0.50:
        predictii.append(("2", c["away"]))

    if c.get("draw", 0) >= 1.28:
        predictii.append(("X", c["draw"]))

    if not predictii:
        return None

    return max(predictii, key=lambda x: x[1])

def construieste_bilet(meciuri):
    bilet = []
    total_cota = 1.0

    for m in meciuri:
        pred = genereaza_predictie(m)
        if pred:
            tip, cota = pred
            bilet.append({
                "meci": f"{m['home']} vs {m['away']}",
                "liga": m["liga"],
                "data": m["data"],
                "ora": m["ora"],
                "tip": tip,
                "cota": cota
            })
            total_cota *= cota

    return bilet, round(total_cota, 2)

ligi_fara_worldcup = filtreaza_ligi_fara_worldcup(scores24_data)
meciuri_valide = selecteaza_meciuri_valide(ligi_fara_worldcup)
bilet_auto, total_cota_auto = construieste_bilet(meciuri_valide)

st.header("🎫 Bilet Automat — Ligi normale (fără Cupa Mondială)")
for s in bilet_auto:
    st.write(
        f"✔️ {s['liga']} | {s['data']} {s['ora']} | "
        f"{s['meci']} ➜ {s['tip']} (cota {s['cota']})"
    )

st.subheader(f"💰 Cotă totală: {total_cota_auto}")
