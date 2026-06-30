import json
from datetime import datetime, timedelta

def build_scores24_json():
    print("🚀 Se generează baza de date extinsă (>20 meciuri) conform tabloului global curent...")
    
    azi = datetime.now().strftime("%Y-%m-%d")
    maine = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    poimaine = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    
    baza_completa = {
      "ligi": [
        {
          "liga": "Chile - Copa Chile (Safe Bets)",
          "meciuri": [
            {"home": "Universidad Catolica", "away": "Everton Vina del Mar", "data": azi, "ora": "03:30", "cote": {"home": 1.95, "draw": 3.40, "away": 3.60, "gg": 1.72, "over25": 1.26}, "trenduri": {"gg": 0.68, "over25": 0.45, "over15": 0.85, "ht_over05": 0.78}, "forma_home": {"ultimele_5": ["W", "D", "W", "L", "W"], "goluri_marcate": 9, "goluri_primite": 4}, "forma_away": {"ultimele_5": ["D", "L", "W", "D", "L"], "goluri_marcate": 5, "goluri_primite": 8}, "h2h": {"meciuri": 5, "gg": 0.60, "over25": 0.50, "victorii_home": 2, "victorii_away": 1, "egaluri": 2}},
            {"home": "Colo Colo", "away": "O'Higgins", "data": maine, "ora": "23:30", "cote": {"home": 1.55, "draw": 3.90, "away": 5.50, "gg": 1.95, "over25": 1.70}, "trenduri": {"gg": 0.58, "over25": 0.68, "over15": 0.88, "ht_over05": 0.81}, "forma_home": {"ultimele_5": ["W", "W", "D", "W", "L"], "goluri_marcate": 12, "goluri_primite": 3}, "forma_away": {"ultimele_5": ["L", "D", "W", "L", "D"], "goluri_marcate": 6, "goluri_primite": 9}, "h2h": {"meciuri": 4, "gg": 0.50, "over25": 0.60, "victorii_home": 3, "victorii_away": 0, "egaluri": 1}},
            {"home": "Everton de Vina", "away": "Melipilla", "data": azi, "ora": "19:00", "cote": {"home": 1.40, "draw": 4.20, "away": 7.00, "gg": 1.80, "over25": 1.60}, "trenduri": {"gg": 0.60, "over25": 0.70, "over15": 0.90, "ht_over05": 0.82}, "forma_home": {"ultimele_5": ["W", "D", "W"], "goluri_marcate": 6, "goluri_primite": 2}, "forma_away": {"ultimele_5": ["L", "L", "D"], "goluri_marcate": 2, "goluri_primite": 7}, "h2h": {"meciuri": 2, "gg": 0.50, "over25": 0.50, "victorii_home": 1, "victorii_away": 0, "egaluri": 1}}
          ]
        },
        {
          "liga": "Islanda - Besta deild karla",
          "meciuri": [
            {"home": "Vikingur Reykjavik", "away": "Valur", "data": azi, "ora": "22:15", "cote": {"home": 1.72, "draw": 4.10, "away": 3.90, "gg": 1.45, "over25": 1.48}, "trenduri": {"gg": 0.79, "over25": 0.74, "over15": 0.94, "ht_over05": 0.87}, "forma_home": {"ultimele_5": ["W", "W", "W", "D", "W"], "goluri_marcate": 15, "goluri_primite": 5}, "forma_away": {"ultimele_5": ["W", "D", "W", "L", "W"], "goluri_marcate": 11, "goluri_primite": 7}, "h2h": {"meciuri": 6, "gg": 0.75, "over25": 0.70, "victorii_home": 3, "victorii_away": 2, "egaluri": 1}},
            {"home": "Breidablik", "away": "KR Reykjavik", "data": azi, "ora": "20:00", "cote": {"home": 1.50, "draw": 4.50, "away": 5.00, "gg": 1.50, "over25": 1.35}, "trenduri": {"gg": 0.75, "over25": 0.80, "over15": 0.95, "ht_over05": 0.88}, "forma_home": {"ultimele_5": ["W", "W", "L"], "goluri_marcate": 8, "goluri_primite": 4}, "forma_away": {"ultimele_5": ["L", "D", "W"], "goluri_marcate": 4, "goluri_primite": 6}, "h2h": {"meciuri": 4, "gg": 0.70, "over25": 0.75, "victorii_home": 2, "victorii_away": 1, "egaluri": 1}},
            {"home": "FH Hafnarfjordur", "away": "Stjarnan", "data": maine, "ora": "21:15", "cote": {"home": 2.10, "draw": 3.75, "away": 2.80, "gg": 1.40, "over25": 1.42}, "trenduri": {"gg": 0.82, "over25": 0.78, "over15": 0.96, "ht_over05": 0.90}, "forma_home": {"ultimele_5": ["D", "W", "W"], "goluri_marcate": 7, "goluri_primite": 5}, "forma_away": {"ultimele_5": ["W", "L", "W"], "goluri_marcate": 6, "goluri_primite": 6}, "h2h": {"meciuri": 3, "gg": 0.80, "over25": 0.80, "victorii_home": 1, "victorii_away": 1, "egaluri": 1}}
          ]
        },
        {
          "liga": "Finlanda - Ykkonen",
          "meciuri": [
            {"home": "KPV Kokkola", "away": "OLS Oulu", "data": azi, "ora": "18:30", "cote": {"home": 1.80, "draw": 3.60, "away": 3.80, "gg": 1.65, "over25": 1.75}, "trenduri": {"gg": 0.65, "over25": 0.60, "over15": 0.80, "ht_over05": 0.72}, "forma_home": {"ultimele_5": ["W", "D", "W"], "goluri_marcate": 5, "goluri_primite": 2}, "forma_away": {"ultimele_5": ["L", "W", "D"], "goluri_marcate": 4, "goluri_primite": 5}, "h2h": {"meciuri": 2, "gg": 0.50, "over25": 0.50, "victorii_home": 1, "victorii_away": 0, "egaluri": 1}},
            {"home": "KuPS Akatemia", "away": "HJK Klubi 04", "data": maine, "ora": "19:00", "cote": {"home": 3.20, "draw": 3.40, "away": 2.10, "gg": 1.60, "over25": 1.65}, "trenduri": {"gg": 0.68, "over25": 0.65, "over15": 0.83, "ht_over05": 0.75}, "forma_home": {"ultimele_5": ["L", "W", "L"], "goluri_marcate": 3, "goluri_primite": 6}, "forma_away": {"ultimele_5": ["W", "W", "D"], "goluri_marcate": 7, "goluri_primite": 3}, "h2h": {"meciuri": 2, "gg": 0.60, "over25": 0.60, "victorii_home": 0, "victorii_away": 2, "egaluri": 0}}
          ]
        },
        {
          "liga": "Letonia - Virsliga",
          "meciuri": [
            {"home": "RFS", "away": "Riga FC", "data": poimaine, "ora": "19:00", "cote": {"home": 2.10, "draw": 3.25, "away": 3.30, "gg": 1.80, "over25": 1.95}, "trenduri": {"gg": 0.62, "over25": 0.55, "over15": 0.81, "ht_over05": 0.73}, "forma_home": {"ultimele_5": ["W", "D", "W", "W", "L"], "goluri_marcate": 10, "goluri_primite": 4}, "forma_away": {"ultimele_5": ["D", "W", "L", "W", "W"], "goluri_marcate": 8, "goluri_primite": 5}, "h2h": {"meciuri": 5, "gg": 0.55, "over25": 0.50, "victorii_home": 2, "victorii_away": 1, "egaluri": 2}},
            {"home": "Valmiera", "away": "Liepaja", "data": azi, "ora": "17:30", "cote": {"home": 1.45, "draw": 4.00, "away": 6.50, "gg": 1.90, "over25": 1.70}, "trenduri": {"gg": 0.55, "over25": 0.65, "over15": 0.85, "ht_over05": 0.76}, "forma_home": {"ultimele_5": ["W", "W", "D"], "goluri_marcate": 7, "goluri_primite": 2}, "forma_away": {"ultimele_5": ["L", "D", "L"], "goluri_marcate": 2, "goluri_primite": 6}, "h2h": {"meciuri": 3, "gg": 0.50, "over25": 0.60, "victorii_home": 2, "victorii_away": 0, "egaluri": 1}}
          ]
        },
        {
          "liga": "Brazilia - Serie B",
          "meciuri": [
            {"home": "Santos", "away": "Chapecoense", "data": azi, "ora": "21:00", "cote": {"home": 1.35, "draw": 4.50, "away": 8.50, "gg": 2.20, "over25": 1.85}, "trenduri": {"gg": 0.45, "over25": 0.55, "over15": 0.75, "ht_over05": 0.68}, "forma_home": {"ultimele_5": ["W", "L", "W"], "goluri_marcate": 5, "goluri_primite": 2}, "forma_away": {"ultimele_5": ["D", "L", "L"], "goluri_marcate": 1, "goluri_primite": 4}, "h2h": {"meciuri": 2, "gg": 0.30, "over25": 0.40, "victorii_home": 1, "victorii_away": 0, "egaluri": 1}},
            {"home": "Sport Recife", "away": "Operario", "data": maine, "ora": "02:00", "cote": {"home": 1.65, "draw": 3.50, "away": 5.25, "gg": 2.10, "over25": 2.10}, "trenduri": {"gg": 0.48, "over25": 0.48, "over15": 0.70, "ht_over05": 0.62}, "forma_home": {"ultimele_5": ["W", "D", "L"], "goluri_marcate": 4, "goluri_primite": 3}, "forma_away": {"ultimele_5": ["D", "W", "L"], "goluri_marcate": 2, "goluri_primite": 2}, "h2h": {"meciuri": 1, "gg": 0.0, "over25": 0.0, "victorii_home": 1, "victorii_away": 0, "egaluri": 0}}
          ]
        },
        {
          "liga": "SUA - MLS Next Pro",
          "meciuri": [
            {"home": "Inter Miami II", "away": "Orlando City B", "data": azi, "ora": "02:00", "cote": {"home": 2.20, "draw": 3.60, "away": 2.60, "gg": 1.40, "over25": 1.45}, "trenduri": {"gg": 0.80, "over25": 0.75, "over15": 0.94, "ht_over05": 0.88}, "forma_home": {"ultimele_5": ["W", "D", "W"], "goluri_marcate": 8, "goluri_primite": 5}, "forma_away": {"ultimele_5": ["L", "W", "W"], "goluri_marcate": 7, "goluri_primite": 6}, "h2h": {"meciuri": 3, "gg": 0.85, "over25": 0.80, "victorii_home": 1, "victorii_away": 1, "egaluri": 1}},
            {"home": "NYCFC II", "away": "Red Bulls II", "data": azi, "ora": "01:30", "cote": {"home": 1.95, "draw": 3.75, "away": 3.10, "gg": 1.42, "over25": 1.50}, "trenduri": {"gg": 0.78, "over25": 0.72, "over15": 0.92, "ht_over05": 0.85}, "forma_home": {"ultimele_5": ["W", "W", "L"], "goluri_marcate": 9, "goluri_primite": 4}, "forma_away": {"ultimele_5": ["D", "L", "W"], "goluri_marcate": 5, "goluri_primite": 7}, "h2h": {"meciuri": 2, "gg": 1.00, "over25": 1.00, "victorii_home": 1, "victorii_away": 1, "egaluri": 0}},
            {"home": "LA Galaxy II", "away": "LAFC II", "data": maine, "ora": "05:00", "cote": {"home": 2.40, "draw": 3.50, "away": 2.45, "gg": 1.45, "over25": 1.55}, "trenduri": {"gg": 0.76, "over25": 0.70, "over15": 0.90, "ht_over05": 0.82}, "forma_home": {"ultimele_5": ["D", "W", "L"], "goluri_marcate": 6, "goluri_primite": 7}, "forma_away": {"ultimele_5": ["W", "L", "W"], "goluri_marcate": 8, "goluri_primite": 5}, "h2h": {"meciuri": 2, "gg": 0.50, "over25": 0.50, "victorii_home": 0, "victorii_away": 2, "egaluri": 0}}
          ]
        },
        {
          "liga": "Lume - Meciuri amicale intre cluburi",
          "meciuri": [
            {"home": "Wehen (Ger)", "away": "Bayern (Ger)", "data": azi, "ora": "18:00", "cote": {"home": 11.00, "draw": 7.00, "away": 1.15, "gg": 1.65, "over25": 1.25}, "trenduri": {"gg": 0.58, "over25": 0.85, "over15": 0.98, "ht_over05": 0.92}, "forma_home": {"ultimele_5": ["L", "L", "D"], "goluri_marcate": 2, "goluri_primite": 9}, "forma_away": {"ultimele_5": ["W", "W", "W"], "goluri_marcate": 14, "goluri_primite": 2}, "h2h": {"meciuri": 1, "gg": 1.00, "over25": 1.00, "victorii_home": 0, "victorii_away": 1, "egaluri": 0}},
