import re
import time
import cloudscraper
import pandas as pd
from targets import TARGETS, LEAGUE_NAMES

from bs4 import BeautifulSoup

MONTH_RE = re.compile(r"^[A-Z][a-z]+ \d{4}$")
GAME_RE = re.compile(r"/game/(\d+)/")

scraper = cloudscraper.create_scraper()
rows = []

for team_id, season_id, label, base in TARGETS:
    url = base.replace("/stats/", "/schedule/").format(team=team_id, season=season_id)
    try:
        for attempt in range(4):
            resp = scraper.get(url, timeout=30)
            if resp.status_code == 200:
                break
            print(f"WARN: {resp.status_code} on {url}, retry {attempt + 1}")
            time.sleep(15)
        resp.raise_for_status()
    except Exception as e:
        print(f"SKIP: {label} schedule ({url}) — {type(e).__name__}: {e}")
        time.sleep(3)
        continue

    soup = BeautifulSoup(resp.text, "lxml")
    found = 0
    for table in soup.find_all("table"):
        headers = [th.get_text(strip=True) for th in table.find_all("th")]
        if "Opponent" not in headers:
            continue
        heading = table.find_previous(string=MONTH_RE)
        year = heading.strip().split()[-1] if heading else ""

        for tr in table.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) < 8:
                continue
            c = [td.get_text(" ", strip=True) for td in tds]
            link = tr.find("a", href=GAME_RE)
            m = GAME_RE.search(link["href"]) if link else None

            score_for = score_against = None
            parts = [p.strip() for p in c[7].split("-")]
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                score_for, score_against = int(parts[0]), int(parts[1])

            rows.append({
                "game_id": m.group(1) if m else None,
                "league": LEAGUE_NAMES[base],
                "team_id": team_id,
                "season_id": season_id,
                "label": label,
                "date": f"{c[1]} {year}".strip(),
                "time": c[2],
                "arena": c[3],
                "home_away": c[4],
                "opponent": c[5],
                "result": c[6],
                "score_for": score_for,
                "score_against": score_against,
            })
            found += 1
    print(f"OK: {label} s{season_id} — {found} games")
    time.sleep(3)

if not rows:
    raise SystemExit("No games parsed from any schedule page")

pd.DataFrame(rows).to_csv("games.csv", index=False)
print(f"Done. {len(rows)} game rows.")
