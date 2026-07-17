import os
import time
import requests
import pandas as pd
from targets import ASHL_TEAMS

API = "https://canlan2-api.sportninja.net/v1"
SEED = os.environ["ASHL_SEED_TOKEN"]

r = requests.post(f"{API}/auth/refresh",
                  headers={"Authorization": f"Bearer {SEED}"}, timeout=30)
r.raise_for_status()
H = {"Authorization": f"Bearer {r.json()['access_token']}"}
print("Auth OK")

WINDOW = {"exclude_cancelled_games": 1, "order": "asc",
          "starts_after": "2015-01-01T00:00:00-07:00",
          "starts_before": "2027-12-31T00:00:00-07:00"}

game_rows = []
for team_id, label in ASHL_TEAMS:
    r = requests.get(f"{API}/teams/{team_id}/schedules", headers=H, timeout=30)
    r.raise_for_status()
    scheds = r.json()
    scheds = scheds["data"] if isinstance(scheds, dict) else scheds
    for s in scheds:
        sid = s.get("id")
        sname = s.get("name") or s.get("name_full") or "unknown"
        if not sid:
            continue
        params = dict(WINDOW, team_id=team_id)
        r2 = requests.get(f"{API}/schedules/{sid}/games", headers=H,
                          params=params, timeout=30)
        if r2.status_code != 200:
            print(f"SKIP: {label} / {sname} games -> HTTP {r2.status_code}")
            continue
        body = r2.json()
        glist = body.get("data", body) if isinstance(body, dict) else body
        n = 0
        for gm in glist:
            home = gm.get("homeTeam") or {}
            vis = gm.get("visitingTeam") or {}
            is_home = home.get("id") == team_id
            opp = (vis if is_home else home).get("name")
            done_flag = gm.get("ended_at") is not None
            game_rows.append({
                "game_id": gm.get("id"),
                "league": "ASHL",
                "team_id": team_id,
                "label": label,
                "season_id": sid,
                "season_name": sname,
                "date": gm.get("starts_at"),
                "home_away": "HOME" if is_home else "AWAY",
                "opponent": opp,
                "opponent_id": (vis if is_home else home).get("id"),
                "score_for": gm.get("home_team_score") if is_home else gm.get("visiting_team_score"),
                "score_against": gm.get("visiting_team_score") if is_home else gm.get("home_team_score"),
                "completed": done_flag,
                "last_period": ((gm.get("current_period") or {}).get("period_type") or {}).get("name"),
                "went_ot": ((gm.get("current_period") or {}).get("period_type") or {}).get("is_overtime"),
                "shootout": gm.get("shootout"),
            })
            n += 1
        print(f"OK: {label} / {sname} — {n} games")
        time.sleep(1)

gdf = pd.DataFrame(game_rows)
gdf.to_csv("ashl_games.csv", index=False)
print(f"Index done: {len(gdf)} games")

# ---- box scores, incremental ----
try:
    old_sk = pd.read_csv("ashl_game_player_stats.csv")
    done = set(old_sk["game_id"])
except FileNotFoundError:
    old_sk, done = None, set()
try:
    old_gl = pd.read_csv("ashl_game_goalie_stats.csv")
except FileNotFoundError:
    old_gl = None

todo = gdf[gdf["completed"] & ~gdf["game_id"].isin(done)].drop_duplicates("game_id")
print(f"{len(todo)} new completed games to fetch ({len(done)} stored)")

sk_rows, gl_rows = [], []
for _, g in todo.iterrows():
    gid = g["game_id"]
    for tid in (g["team_id"], g["opponent_id"]):
        if not tid:
            continue
        for goalie, bucket in ((0, sk_rows), (1, gl_rows)):
            try:
                r = requests.get(
                    f"{API}/games/{gid}/stats/players/team/{tid}",
                    headers=H, params={"goalie": goalie}, timeout=30)
                if r.status_code != 200:
                    print(f"WARN: {gid}/{tid} g={goalie} HTTP {r.status_code}")
                    continue
                for entry in r.json().get("data", []):
                    p = entry.get("player", {})
                    row = {
                        "game_id": gid,
                        "league": "ASHL",
                        "date": g["date"],
                        "jersey": p.get("player_number"),
                        "player": f"{p.get('name_first','')} {p.get('name_last','')}".strip(),
                        "player_id": p.get("id"),
                        "sn_team_id": tid,
                    }
                    for s in entry.get("stats", []):
                        row[s["abbr"]] = s["value"]
                    bucket.append(row)
            except Exception as e:
                print(f"SKIP {gid}/{tid} g={goalie} — {type(e).__name__}: {e}")
            time.sleep(0.5)
    print(f"OK game {gid}")

if sk_rows:
    out = pd.concat([old_sk, pd.DataFrame(sk_rows)]) if old_sk is not None else pd.DataFrame(sk_rows)
    out.to_csv("ashl_game_player_stats.csv", index=False)
if gl_rows:
    out = pd.concat([old_gl, pd.DataFrame(gl_rows)]) if old_gl is not None else pd.DataFrame(gl_rows)
    out.to_csv("ashl_game_goalie_stats.csv", index=False)
print(f"Done. +{len(sk_rows)} skater rows, +{len(gl_rows)} goalie rows.")
