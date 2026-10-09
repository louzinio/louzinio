"""Render the GitHub contribution calendar as red-scale SVGs (light and dark)."""

import datetime as dt
import json
import os
import sys
import urllib.request

USER = os.environ.get("GH_USER", "louzinio")
OUT_DIR = sys.argv[1] if len(sys.argv) > 1 else "assets"

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount weekday } }
      }
    }
  }
}
"""

THEMES = {
    "dark": dict(bg="#0d1117", border="#30363d", text="#e6edf3", muted="#8b949e", accent="#e5484d",
                 levels=["#161b22", "#4a1216", "#7f1d24", "#c22a33", "#f0525a"]),
    "light": dict(bg="#ffffff", border="#d0d7de", text="#1f2328", muted="#59636e", accent="#cf222e",
                  levels=["#ebedf0", "#ffcdd0", "#ff8f96", "#e0434b", "#a3141c"]),
}

SANS = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"

CELL, GAP = 16, 4
STEP = CELL + GAP
LEFT, TOP = 96, 92
WIDTH, HEIGHT = 1200, 300


def fetch():
    token = os.environ["GITHUB_TOKEN"]
    body = json.dumps({"query": QUERY, "variables": {"login": USER}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body,
                                 headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        data = json.load(resp)
    if "errors" in data:
        raise SystemExit(data["errors"])
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def level(count, peak):
    if count == 0:
        return 0
    ratio = count / peak
    return 1 if ratio <= 0.25 else 2 if ratio <= 0.5 else 3 if ratio <= 0.75 else 4


def render(cal, t):
    weeks = cal["weeks"]
    peak = max(d["contributionCount"] for w in weeks for d in w["contributionDays"]) or 1
    total = cal["totalContributions"]

    cells, months = [], []
    last_month = None
    for wi, week in enumerate(weeks):
        x = LEFT + wi * STEP
        first = dt.date.fromisoformat(week["contributionDays"][0]["date"])
        if first.month != last_month and wi < len(weeks) - 2:
            months.append(f'<text x="{x}" y="{TOP - 10}">{first.strftime("%b")}</text>')
            last_month = first.month
        for day in week["contributionDays"]:
            y = TOP + day["weekday"] * STEP
            n = day["contributionCount"]
            label = f'{n} contribution{"" if n == 1 else "s"} on {day["date"]}'
            cells.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" '
                         f'fill="{t["levels"][level(n, peak)]}"><title>{label}</title></rect>')

    days = "".join(f'<text x="{LEFT - 12}" y="{TOP + i * STEP + 12}" text-anchor="end">{d}</text>'
                   for i, d in [(1, "Mon"), (3, "Wed"), (5, "Fri")])
    legend_x = LEFT + 53 * STEP - 5 * STEP - GAP
    legend_y = TOP + 7 * STEP + 22
    legend = "".join(f'<rect x="{legend_x + i * STEP}" y="{legend_y}" width="{CELL}" height="{CELL}" rx="3" fill="{c}"/>'
                     for i, c in enumerate(t["levels"]))
    updated = dt.date.today().isoformat()

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="{total} contributions in the last year">
  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="12" fill="{t["bg"]}" stroke="{t["border"]}"/>
  <rect x="{LEFT}" y="34" width="3" height="20" fill="{t["accent"]}"/>
  <text x="{LEFT + 14}" y="51" font-family="{SANS}" font-size="20" fill="{t["text"]}"><tspan font-weight="600">{total}</tspan> contributions in the last year</text>
  <g font-family="{MONO}" font-size="11" fill="{t["muted"]}">
    {"".join(months)}
    {days}
    <text x="{legend_x - 10}" y="{legend_y + 12}" text-anchor="end">Less</text>
    <text x="{legend_x + 5 * STEP + 6}" y="{legend_y + 12}">More</text>
    <text x="{LEFT}" y="{legend_y + 12}">updated {updated}</text>
  </g>
  {"".join(cells)}
  {legend}
</svg>
'''


def main():
    cal = fetch()
    for name, theme in THEMES.items():
        with open(os.path.join(OUT_DIR, f"contrib-{name}.svg"), "w", encoding="utf-8") as f:
            f.write(render(cal, theme))
    print(f"{cal['totalContributions']} contributions")


if __name__ == "__main__":
    main()
