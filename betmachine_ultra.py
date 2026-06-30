import json
import time
import os
import streamlit as st

# =========================
# 1. Încărcare JSON cu protecție
# =========================

def load_scores_json(path="scores24.json"):
    if not os.path.exists(path):
        st.error(f"Fișierul {path} nu există.")
        return {"ligi": []}

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                st.error("Fișierul scores24.json este gol.")
                return {"ligi": []}
            data = json.loads(content)
            return data
    except json.JSONDecodeError:
        st.error("Fișierul scores24.json este corupt sau incomplet.")
        return {"ligi": []}
    except Exception as e:
        st.error(f"Eroare la citirea scores24.json: {e}")
        return {"ligi": []}

# =========================
# 2. Funcții de decizie (GG, Over 2.5, 1X2)
# =========================

def is_good_for_gg(match):
    xa = match.get("xanalytics", {})

    return (
        xa.get("xg_home", 0) >= 1.2 and
        xa.get("xg_away", 0) >= 1.0 and
        xa.get("xthreat_home", 0) >= 1.5 and
        xa.get("xthreat_away", 0) >= 1.3
    )


def is_good_for_over25(match):
    xa = match.get("xanalytics", {})

    total_xg = xa.get("xg_home", 0) + xa.get("xg_away", 0)
    total_danger = xa.get("danger_attacks_home", 0) + xa.get("danger_attacks_away", 0)

    return (
        total_xg >= 2.6 and
        total_danger >= 70
    )


def predict_1x2(match):
    xa = match.get("xanalytics", {})

    score = (
        xa.get("xg_home", 0) - xa.get("xg_away", 0) +
        (xa.get("pressing_home", 0) - xa.get("pressing_away", 0))
    )

    if score > 0.25:
        return "1"
    elif score < -0.25:
        return "2"
    else:
        return "X"

# =========================
# 3. Generarea listelor de bilete
# =========================

def flatten_matches(data):
    meciuri = []
    for liga in data.get("ligi", []):
        for m in liga.get("meciuri", []):
            meciuri.append(m)
    return meciuri


def genereaza_bilete(meciuri):
    bilete_gg = [m for m in meciuri if is_good_for_gg(m)]
    bilete_over25 = [m for m in meciuri if is_good_for_over25(m)]

    bilete_1x2 = []
    for m in meciuri:
        rezultat = predict_1x2(m)
        bilete_1x2.append({
            "meci": f'{m["home"]} - {m["away"]}',
            "predictie": rezultat,
            "xg_home": m.get("xanalytics", {}).get("xg_home", 0),
            "xg_away": m.get("xanalytics", {}).get("xg_away", 0)
        })

    return bilete_gg, bilete_over25, bilete_1x2

# =========================
# 4. UI Streamlit
# =========================

def main():
    st.set_page_config(page_title="BetMachine Pro 55 ULTRA", layout="wide")

    st.title("BetMachine Pro 55 ULTRA")
    st.caption("Analiză avansată cu Football Analytics (xG, xThreat, Pressing)")

    data = load_scores_json()
    meciuri = flatten_matches(data)

    if not meciuri:
        st.warning("Nu există meciuri în scores24.json.")
        return

    bilete_gg, bilete_over25, bilete_1x2 = genereaza_bilete(meciuri)

    tab1, tab2, tab3, tab4 = st.tabs(["Toate meciurile", "Bilete GG", "Bilete Over 2.5", "Bilete 1X2"])

    # =========================
    # TAB 1: Toate meciurile
    # =========================
    with tab1:
        st.subheader("Toate meciurile disponibile")

        options = [f'{m["liga"]}: {m["home"]} - {m["away"]} ({m["data"]} {m["ora"]})' for m in meciuri]
        selected = st.selectbox("Alege un meci", options)

        idx = options.index(selected)
        match = meciuri[idx]

        st.markdown(f"### {match['home']} - {match['away']}")
        st.write(f"Liga: {match['liga']}")
        st.write(f"Data: {match['data']}  Ora: {match['ora']}")

        # Football Analytics (xG / xThreat / Pressing)
        st.subheader("Football Analytics (xG / xThreat / Pressing)")

        xa = match.get("xanalytics", {})

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("xG Home", xa.get("xg_home", 0))
            st.metric("xThreat Home", xa.get("xthreat_home", 0))

        with col2:
            st.metric("xG Away", xa.get("xg_away", 0))
            st.metric("xThreat Away", xa.get("xthreat_away", 0))

        with col3:
            st.metric("Pressing Home", xa.get("pressing_home", 0))
            st.metric("Pressing Away", xa.get("pressing_away", 0))

        st.write("---")
        st.write("Blocul xanalytics brut:")
        st.json(xa)

    # =========================
    # TAB 2: Bilete GG
    # =========================
    with tab2:
        st.subheader("Bilete GG (ambele marchează)")

        if not bilete_gg:
            st.info("Nu s-au găsit meciuri bune pentru GG pe baza analytics.")
        else:
            for m in bilete_gg:
                xa = m.get("xanalytics", {})
                st.markdown(f"**{m['home']} - {m['away']}**  ({m['liga']})")
                st.write(f"xG Home: {xa.get('xg_home', 0)}  |  xG Away: {xa.get('xg_away', 0)}")
                st.write(f"xThreat Home: {xa.get('xthreat_home', 0)}  |  xThreat Away: {xa.get('xthreat_away', 0)}")
                st.write("---")

    # =========================
    # TAB 3: Bilete Over 2.5
    # =========================
    with tab3:
        st.subheader("Bilete Over 2.5 goluri")

        if not bilete_over25:
            st.info("Nu s-au găsit meciuri bune pentru Over 2.5 pe baza analytics.")
        else:
            for m in bilete_over25:
                xa = m.get("xanalytics", {})
                total_xg = xa.get("xg_home", 0) + xa.get("xg_away", 0)
                total_danger = xa.get("danger_attacks_home", 0) + xa.get("danger_attacks_away", 0)

                st.markdown(f"**{m['home']} - {m['away']}**  ({m['liga']})")
                st.write(f"Total xG: {total_xg}  |  Atacuri periculoase: {total_danger}")
                st.write("---")

    # =========================
    # TAB 4: Bilete 1X2
    # =========================
    with tab4:
        st.subheader("Bilete 1X2 (pe baza xG + pressing)")

        if not bilete_1x2:
            st.info("Nu s-au generat bilete 1X2.")
        else:
            for b in bilete_1x2:
                st.markdown(f"**{b['meci']}**  →  Predicție: **{b['predictie']}**")
                st.write(f"xG Home: {b['xg_home']}  |  xG Away: {b['xg_away']}")
                st.write("---")


if __name__ == "__main__":
    main()
