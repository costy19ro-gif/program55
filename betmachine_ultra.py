import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="BetMachine Pro 55 ULTRA", layout="wide")

def load_scores24_json(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

st.title("🔥 BetMachine Pro 55 ULTRA")

json_path = "scores24.json"
scores24_data = load_scores24_json(json_path)

if not scores24_data:
    st.error("❌ Nu am găsit fișierul JSON Scores24")
    st.stop()

st.success("✅ JSON Scores24 încărcat cu succes")

# 📅 selector de zi
zile_disponibile = sorted({m["data"] for liga in scores24_data["ligi"] for m in liga["meciuri"]})
zi_aleasa = st.selectbox("📅 Alege ziua", zile_disponibile)

def calc_form_score(form_list):
    score_map = {"W": 3, "D": 1, "L": 0}
    return sum(score_map.get(r, 0) for r in form_list)

def ultra_predict(match):
    t = match.get("trenduri", {})
    gg_prob = t.get("gg", 0.0)
    over25_prob = t.get("over25", 0.0)
    over15_prob = t.get("over15", 0.0)
    ht_over05_prob = t.get("ht_over05", 0.0)
    home_score_prob = t.get("home_score", 0.0)
    away_score_prob = t.get("away_score", 0.0)

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
        "home_score_prob": home_score_prob,
        "away_score_prob": away_score_prob,
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
                "home_score_prob": round(p["home_score_prob"], 2),
                "away_score_prob": round(p["away_score_prob"], 2),
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

st.header("🎯 Bilet ULTRA (GG / Over / O1.5 / HT O0.5 / Home/Away Score)")

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
                f"Home Score={b['home_score_prob']} | "
                f"Away Score={b['away_score_prob']} | "
                f"1={b['cote_home']} X={b['cote_draw']} 2={b['cote_away']}"
            )

        st.subheader("📊 Statistici ligă")
        st.line_chart(df[["gg_prob", "over25_prob", "over15_prob"]])

    st.header("⚡ Bilet ULTRA+ (value bets)")
    for b in bilete_ultra_plus:
        st.write(
            f"**{b['tip']}** | {b['meci']} | scor={b['score']} | cota={b['cota']}"
        )
