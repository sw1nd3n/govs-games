import re
import time
import cloudscraper
import pandas as pd
from bs4 import BeautifulSoup
from targets import ROOTS

PLAYER_RE = re.compile(r"/player/(\d+)/home/\?team=(\d+)")

scraper = cloudscraper.create_scraper()

games = pd.read_csv("games.csv")
games = games.dropna(subset=["game_id"])
games = games[games["result"].notna() & games["result"].astype(str).str.strip().ne("")]
games["game_id"] = games["game_id"].astype(int)

try:
    old_sk = pd.read_csv("game_player_stats.csv")
    done = set(old_sk["game_id"].astype(int))
except FileNotFoundError:
    old_sk, done = None, set()
try:
    old_gl = pd.read_csv("game_goalie_stats.csv")
except FileNotFoundError:
    old_gl = None

todo = games.drop_duplicates("game_id")
todo = todo[~todo["game_id"].isin(done)]
print(f"{len(todo)} new games to fetch ({len(done)} already stored)")

sk_rows, gl_rows = [], []

for _, g in todo.iterrows():
    gid = int(g["game_id"])
    url = f"{ROOTS[g['league']]}/game/{gid}/team-stats"
    try:
        for attempt in range(4):
            resp = scraper.get(url, timeout=30)
            if resp.status_code == 200:
                break
            print(f"WARN: {resp.status_code} on {url}, retry {attempt + 1}")
            time.sleep(15)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "lxml")
        parsed = 0
        for table in soup.find_all("table"):
            headers = [th.get_text(strip=True) for th in table.find_all("th")]
            is_sk = "Player" in headers
            is_gl = "Goalie" in headers
            if not (is_sk or is_gl):
                continue
            for tr in table.find_all("tr"):
                tds = tr.find_all("td")
                a = tr.find("a", href=PLAYER_RE)
                if not a or len(tds) < 6:
                    continue
                m = PLAYER_RE.search(a["href"])
                c = [td.get_text(strip=True) for td in tds]
                row = {
                    "game_id": gid,
                    "league": g["league"],
                    "date": g["date"],
                    "jersey": c[0],
                    "player": a.get_text(strip=True),
                    "player_id": int(m.group(1)),
                    "sz_team_id": int(m.group(2)),
                }
                if is_sk:
                    row.update({"G": c[2], "A": c[3], "P": c[4], "PIM": c[5]})
                    sk_rows.append(row)
                elif len(tds) >= 7:
                    row.update({"SA": c[2], "GA": c[3], "SV": c[4], "SV_PCT": c[5], "MIN": c[6]})
                    gl_rows.append(row)
                parsed += 1
        print(f"OK game {gid}: {parsed} rows")
    except Exception as e:
        print(f"SKIP game {gid} — {type(e).__name__}: {e}")
    time.sleep(2)

if sk_rows:
    out = pd.concat([old_sk, pd.DataFrame(sk_rows)]) if old_sk is not None else pd.DataFrame(sk_rows)
    out.to_csv("game_player_stats.csv", index=False)
if gl_rows:
    out = pd.concat([old_gl, pd.DataFrame(gl_rows)]) if old_gl is not None else pd.DataFrame(gl_rows)
    out.to_csv("game_goalie_stats.csv", index=False)
print(f"Done. +{len(sk_rows)} skater rows, +{len(gl_rows)} goalie rows.")
