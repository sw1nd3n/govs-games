# ---- Sportzone leagues ----
NCHL = "https://cstats.nchl.com/team/{team}/stats/?season={season}"
WRAHL = "https://wrahl.com/team/{team}/stats/?season={season}"
ASUMMERHL = "https://albertasummerhockey.com/team/{team}/stats/?season={season}"

LEAGUE_NAMES = {NCHL: "NCHL", WRAHL: "WRAHL", ASUMMERHL: "ASUMMERHL"}

ROOTS = {
    "NCHL": "https://cstats.nchl.com",
    "WRAHL": "https://wrahl.com",
    "ASUMMERHL": "https://albertasummerhockey.com",
}

# (team_id, season_id, label, base) — same list as govs-stats
TARGETS = [
    (25649, 147, "VS - E", NCHL),
    (25649, 148, "VS - E", NCHL),
    (25649, 149, "VS - E", NCHL),
    (25649, 154, "VS - E", NCHL),
    (25649, 155, "VS - E", NCHL),
    (25649, 160, "VS - E", NCHL),
    (25649, 161, "VS - E", NCHL),
    (25649, 162, "VS - E", NCHL),
    (25649, 163, "VS - E", NCHL),
    (25649, 164, "VS - E", NCHL),
    (25649, 165, "VS - E", NCHL),
    (25649, 166, "VS - E", NCHL),
    (25655, 147, "VS - F", NCHL),
    (25655, 148, "VS - F", NCHL),
    (25655, 149, "VS - F", NCHL),
    (25655, 154, "VS - F", NCHL),
    (25655, 155, "VS - F", NCHL),
    (25655, 160, "VS - F", NCHL),
    (25655, 161, "VS - F", NCHL),
    (25655, 162, "VS - F", NCHL),
    (25655, 163, "VS - F", NCHL),
    (25655, 164, "VS - F", NCHL),
    (25655, 165, "VS - F", NCHL),
    (25655, 166, "VS - F", NCHL),
    (28185, 147, "VS - G", NCHL),
    (28185, 148, "VS - G", NCHL),
    (28185, 149, "VS - G", NCHL),
    (28185, 154, "VS - G", NCHL),
    (28185, 155, "VS - G", NCHL),
    (28185, 160, "VS - G", NCHL),
    (28185, 161, "VS - G", NCHL),
    (28185, 162, "VS - G", NCHL),
    (28185, 163, "VS - G", NCHL),
    (28185, 164, "VS - G", NCHL),
    (28185, 165, "VS - G", NCHL),
    (28185, 166, "VS - G", NCHL),
    (30960, 147, "VS - H", NCHL),
    (30960, 148, "VS - H", NCHL),
    (30960, 149, "VS - H", NCHL),
    (30960, 154, "VS - H", NCHL),
    (30960, 155, "VS - H", NCHL),
    (30960, 160, "VS - H", NCHL),
    (30960, 161, "VS - H", NCHL),
    (30960, 162, "VS - H", NCHL),
    (30960, 163, "VS - H", NCHL),
    (30960, 164, "VS - H", NCHL),
    (30960, 165, "VS - H", NCHL),
    (30960, 166, "VS - H", NCHL),

    (10828, 99, "VS - B", WRAHL),
    (10828, 101, "VS - B", WRAHL),
    (10828, 103, "VS - B", WRAHL),
    (10828, 104, "VS - B", WRAHL),
    (10828, 105, "VS - B", WRAHL),
    (10828, 106, "VS - B", WRAHL),
    (10828, 107, "VS - B", WRAHL),
    (10828, 108, "VS - B", WRAHL),
    (10828, 109, "VS - B", WRAHL),
    (10828, 112, "VS - B", WRAHL),
    
    (10828, 113, "VS - B", WRAHL),
    (10828, 114, "VS - B", WRAHL),
    (10828, 117, "VS - B", WRAHL),
    (10828, 118, "VS - B", WRAHL),
    (10828, 119, "VS - B", WRAHL),
    (11835, 109, "VS - A", WRAHL),
    (11835, 112, "VS - A", WRAHL),
    (11835, 113, "VS - A", WRAHL),
    (11835, 114, "VS - A", WRAHL),
    (11835, 117, "VS - A", WRAHL),
    (3020, 64, "VS - A", ASUMMERHL),
]

# ---- ASHL / SportNinja teams: (team_id, label) ----
ASHL_TEAMS = [
    ("1S9vxCG4ogfXwn8U", "VS - C"),
    ("vn1dxgLkcLT896eN", "VS - D"),
]
