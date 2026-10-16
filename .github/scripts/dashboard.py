"""Render the terminal-style profile dashboard panels from public GitHub data.

Writes, for both desktop and mobile layouts:
  contributions[-mobile].svg  heatmap of the last year
  whoami[-mobile].svg         portrait + streak/contribution tiles + monthly bars
  languages[-mobile].svg      language share across public, non-fork repositories

Usage (the workflow runs this daily with the built-in GITHUB_TOKEN):
    GITHUB_TOKEN=... python dashboard.py Pranav-0710 dist/

Every number comes from the GitHub GraphQL API. Nothing is hardcoded except the
settings below. If the API call fails, nothing is written, so the workflow
republishes the previous cards.
"""
import base64
import io
import json
import os
import sys
import urllib.request
from collections import OrderedDict
from datetime import date, datetime, timezone

ROLE = "ML / AI engineering · full-stack"
PROMPT_USER = "jey"
# Portrait source: this file if it exists, otherwise the GitHub avatar.
PORTRAIT_FILE = "assets/portrait.png"
# left, top, right, bottom as fractions of the source image (tuned for the current avatar).
PORTRAIT_CROP = (0.2, 0.0, 0.9, 0.7)
# "dither": dot-matrix, works with photos. "ascii": character art, best with a cartoon or
# illustrated avatar on a plain background.
PORTRAIT_STYLE = "dither"
# The portrait loops: dots appear in staggered waves, hold, then dissolve.
FADE_LAYERS = 4
FADE_CYCLE = 7  # seconds per loop

BG, PANEL, BAR, BORDER, GRID = "#0d1117", "#0d1117", "#161b22", "#30363d", "#21262d"
TEXT, MUTED, DIM = "#c9d1d9", "#8b949e", "#6e7681"
GREEN = "#39d353"
LEVELS = {"NONE": "#161b22", "FIRST_QUARTILE": "#0e4429", "SECOND_QUARTILE": "#006d32",
          "THIRD_QUARTILE": "#26a641", "FOURTH_QUARTILE": "#39d353"}
FONT = "ui-monospace,SFMono-Regular,'SF Mono','JetBrains Mono','Cascadia Code',Menlo,Consolas,'Liberation Mono',monospace"

QUERY = """
query($login: String!) {
  user(login: $login) {
    login name createdAt avatarUrl(size: 400)
    followers { totalCount }
    publicRepos: repositories(privacy: PUBLIC, ownerAffiliations: OWNER) { totalCount }
    repositories(privacy: PUBLIC, ownerAffiliations: OWNER, isFork: false, first: 100) {
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } }
      }
    }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date weekday contributionCount contributionLevel } }
      }
    }
  }
}
"""


# ── data ────────────────────────────────────────────────────────────────────

def graphql(login):
    body = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body, headers={
        "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
        "Content-Type": "application/json",
        "User-Agent": "profile-dashboard",
    })
    with urllib.request.urlopen(req, timeout=30) as res:
        payload = json.load(res)
    if payload.get("errors"):
        raise RuntimeError(payload["errors"])
    return payload["data"]["user"]


def fmt_day(d):
    return f"{d:%b} {d.day}"


def summarize(user):
    cal = user["contributionsCollection"]["contributionCalendar"]
    weeks = cal["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    for d in days:
        d["d"] = date.fromisoformat(d["date"])

    # Current streak: a day with no contributions yet today does not break it.
    idx = len(days) - 1
    if days[idx]["contributionCount"] == 0:
        idx -= 1
    cur, cur_start = 0, None
    while idx >= 0 and days[idx]["contributionCount"] > 0:
        cur, cur_start, idx = cur + 1, days[idx]["d"], idx - 1

    best_run, run, run_start, best_span = 0, 0, None, None
    for d in days:
        if d["contributionCount"] > 0:
            run_start = d["d"] if run == 0 else run_start
            run += 1
            if run > best_run:
                best_run, best_span = run, (run_start, d["d"])
        else:
            run = 0

    active = [d for d in days if d["contributionCount"] > 0]
    best = max(days, key=lambda d: d["contributionCount"])
    months = OrderedDict()
    for d in days:
        key = d["d"].replace(day=1)
        months[key] = months.get(key, 0) + d["contributionCount"]
    monthly = list(months.items())[-12:]

    lang = {}
    for repo in user["repositories"]["nodes"]:
        for edge in repo["languages"]["edges"]:
            lang[edge["node"]["name"]] = lang.get(edge["node"]["name"], 0) + edge["size"]
    total_bytes = sum(lang.values()) or 1
    langs = sorted(((n, s / total_bytes) for n, s in lang.items()), key=lambda x: -x[1])[:6]

    total = cal["totalContributions"]
    return {
        "login": user["login"],
        "name": user["name"] or user["login"],
        "avatar": user["avatarUrl"],
        "weeks": weeks,
        "total": total,
        "current": cur, "current_sub": f"since {fmt_day(cur_start)}" if cur else "start one today",
        "longest": best_run,
        "longest_sub": f"{fmt_day(best_span[0])} – {fmt_day(best_span[1])}" if best_span else "—",
        "active": len(active), "active_sub": f"of {len(days)} days",
        "best": best["contributionCount"], "best_sub": f"{best['d']:%b} {best['d'].day}, {best['d'].year}",
        "avg": f"{total / len(active):.1f}" if active else "0",
        "monthly": monthly,
        "langs": langs,
        "repos": user["publicRepos"]["totalCount"],
        "stars": sum(r["stargazerCount"] for r in user["repositories"]["nodes"]),
        "followers": user["followers"]["totalCount"],
        "since": datetime.fromisoformat(user["createdAt"].replace("Z", "+00:00")).strftime("%b %Y"),
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }


# ── portrait ────────────────────────────────────────────────────────────────

RAMP = " .,:;irsXA253hMHGS#9B&@"


def load_portrait(avatar_url):
    """Cropped grayscale source image, or None if Pillow or the image is unavailable."""
    try:
        from PIL import Image, ImageOps
        if os.path.exists(PORTRAIT_FILE):
            img = Image.open(PORTRAIT_FILE)
        else:
            req = urllib.request.Request(avatar_url, headers={"User-Agent": "profile-dashboard"})
            with urllib.request.urlopen(req, timeout=30) as res:
                img = Image.open(io.BytesIO(res.read()))
        img = img.convert("L")
    except Exception as exc:  # noqa: BLE001 - any failure falls back to initials
        print(f"portrait skipped: {exc}", file=sys.stderr)
        return None
    w, h = img.size
    l, t, r, b = PORTRAIT_CROP
    img = img.crop((int(l * w), int(t * h), int(r * w), int(b * h)))
    return ImageOps.autocontrast(img, cutoff=1)


def fade_css(size):
    """Looping dissolve for the portrait layers, with a scan line sweeping in."""
    stagger = 0.3
    return ('<style>'
            f'.pl{{animation:pl {FADE_CYCLE}s ease-in-out infinite backwards}}'
            '@keyframes pl{0%{opacity:0}10%{opacity:1}65%{opacity:1}78%{opacity:0}100%{opacity:0}}'
            + "".join(f'.pl{k}{{animation-delay:{k * stagger:.1f}s}}' for k in range(FADE_LAYERS))
            + f'.scan{{opacity:0;animation:scan {FADE_CYCLE}s linear infinite}}'
            f'@keyframes scan{{0%{{opacity:.85;transform:translateY(0)}}'
            f'22%{{opacity:.85;transform:translateY({size}px)}}23%,100%{{opacity:0;transform:translateY({size}px)}}}}'
            '</style>')


def scan_line(x, y, size):
    return (f'<g class="scan"><rect x="{x}" y="{y - 4}" width="{size}" height="10" fill="{GREEN}" opacity=".12"/>'
            f'<rect x="{x}" y="{y}" width="{size}" height="2" fill="{GREEN}"/></g>')


def dither_svg(img, x, y, size, color=TEXT):
    """1-bit Floyd–Steinberg dot matrix, split into FADE_LAYERS transparent PNGs."""
    from PIL import Image, ImageEnhance
    pitch = 4
    n = size // pitch
    dots = ImageEnhance.Contrast(img).enhance(1.3).resize((n, n), Image.LANCZOS).convert("1")
    rgb = tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))
    layers = []
    for _ in range(FADE_LAYERS):
        layer = Image.new("P", (n * pitch, n * pitch), 0)
        layer.putpalette([0, 0, 0, *rgb])
        layers.append(layer)
    px, outs = dots.load(), [layer.load() for layer in layers]
    for j in range(n):
        for i in range(n):
            if px[i, j]:
                # Deterministic scatter, so the layers do not change between daily runs.
                out = outs[((i * 73856093) ^ (j * 19349663)) % FADE_LAYERS]
                for dy in range(pitch - 1):
                    for dx in range(pitch - 1):
                        out[i * pitch + dx, j * pitch + dy] = 1
    parts = []
    for k, layer in enumerate(layers):
        buf = io.BytesIO()
        layer.save(buf, "PNG", transparency=0, optimize=True)
        data = base64.b64encode(buf.getvalue()).decode()
        parts.append(f'<image class="pl pl{k}" x="{x}" y="{y}" width="{n * pitch}" height="{n * pitch}" '
                     f'style="image-rendering:pixelated" href="data:image/png;base64,{data}"/>')
    return "".join(parts)


def ascii_rows(img, cols, rows):
    from PIL import Image, ImageFilter, ImageOps
    edges = ImageOps.autocontrast(img.filter(ImageFilter.FIND_EDGES))
    img = Image.blend(img, edges, 0.35).resize((cols, rows), Image.LANCZOS)
    px = img.load()
    return ["".join(RAMP[min(len(RAMP) - 1, int(px[x, y] / 255 * len(RAMP)))] for x in range(cols))
            for y in range(rows)]


def ascii_svg(rows, x0, y0, cw, rh, size):
    tiers = [(DIM, set(RAMP[1:8])), (MUTED, set(RAMP[8:15])), (TEXT, set(RAMP[15:]))]
    groups = [[] for _ in range(FADE_LAYERS)]
    for r, line in enumerate(rows):
        for color, chars in tiers:
            xs = [f"{x0 + c * cw:.1f}" for c, ch in enumerate(line) if ch in chars]
            text = "".join(ch for ch in line if ch in chars)
            if text:
                groups[r % FADE_LAYERS].append(
                    f'<text y="{y0 + r * rh:.1f}" x="{" ".join(xs)}" fill="{color}">{esc(text)}</text>')
    return "".join(f'<g class="pl pl{k}" font-size="{size}">{"".join(g)}</g>' for k, g in enumerate(groups))


def portrait_svg(img, name, x, y, size):
    """Portrait block filling a size×size square at (x, y), looping fade in and out."""
    if img is not None and PORTRAIT_STYLE == "dither":
        art = dither_svg(img, x, y, size, MUTED)
    elif img is not None:
        cols = 60
        cw = size / cols
        rows = int(size / (cw * 1.72))
        art = ascii_svg(ascii_rows(img, cols, rows), x, y + cw * 1.4, cw, cw * 1.72, round(cw * 1.62, 1))
    else:
        initials = "".join(p[0] for p in name.split()[:2]).upper() or "?"
        art = (f'<text class="pl pl0" x="{x + size / 2}" y="{y + size / 2 + 30}" text-anchor="middle" '
               f'font-size="96" font-weight="700" fill="{GREEN}">{esc(initials)}</text>')
    return fade_css(size) + art + scan_line(x, y, size)


# ── drawing helpers ─────────────────────────────────────────────────────────

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def prompt_line(cx, y, cmd, size=14):
    return (f'<text x="{cx}" y="{y}" text-anchor="middle" font-size="{size}">'
            f'<tspan fill="{GREEN}">{PROMPT_USER}@github</tspan><tspan fill="{MUTED}"> ~ $ </tspan>'
            f'<tspan fill="{TEXT}">{esc(cmd)}</tspan></text>')


def panel(x, y, w, h, title, right=""):
    dots = "".join(f'<circle cx="{x + 16 + i * 14}" cy="{y + 14}" r="4" fill="{BORDER}"/>' for i in range(3))
    r = (f'<text x="{x + w - 14}" y="{y + 18}" text-anchor="end" font-size="10.5" fill="{DIM}">{esc(right)}</text>'
         if right else "")
    return (f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" rx="8" fill="{PANEL}" stroke="{BORDER}"/>'
            f'<path d="M{x + 1} {y + 28.5}H{x + w - 1}" stroke="{GRID}"/>{dots}'
            f'<text x="{x + 64}" y="{y + 18}" font-size="10.5" letter-spacing=".6" fill="{DIM}">{esc(title)}</text>{r}')


def svg(w, h, title, desc, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="t d"><title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>'
            f'<style>.fade{{animation:fade .6s ease-out backwards}}@keyframes fade{{from{{opacity:0}}}}'
            # Reduced motion keeps opacity fades (no movement) and drops the moving scan line.
            f'@media (prefers-reduced-motion:reduce){{.scan{{animation:none!important}}}}</style>'
            f'<rect width="{w}" height="{h}" rx="10" fill="{BG}"/><g font-family="{FONT}">{body}</g></svg>\n')


# ── panels ──────────────────────────────────────────────────────────────────

def contributions(s, mobile):
    weeks = s["weeks"][-26:] if mobile else s["weeks"]
    w = 480 if mobile else 1000
    pitch, cell = (15, 12) if mobile else (16, 13)
    grid_w = len(weeks) * pitch
    gx = (w - grid_w + 30) / 2
    py, gy = 44, 44 + 58
    h = gy + 7 * pitch + (80 if mobile else 58)
    out = [prompt_line(w / 2, 24, "./contributions.sh", 16 if mobile else 14),
           panel(0, py, w, h - py, "contributions.log", "last 6 months" if mobile else "last 12 months")]
    seen = None
    for i, week in enumerate(weeks):
        first = date.fromisoformat(week["contributionDays"][0]["date"])
        if first.month != seen and (i < len(weeks) - 2):
            seen = first.month
            out.append(f'<text x="{gx + i * pitch}" y="{gy - 10}" font-size="11" fill="{MUTED}">{first:%b}</text>')
        for d in week["contributionDays"]:
            out.append(f'<rect class="fade" style="animation-delay:{i * 0.012:.2f}s" x="{gx + i * pitch}" '
                       f'y="{gy + d["weekday"] * pitch}" width="{cell}" height="{cell}" rx="2.5" '
                       f'fill="{LEVELS[d["contributionLevel"]]}"><title>{d["contributionCount"]} on {d["date"]}</title></rect>')
    for wd, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        out.append(f'<text x="{gx - 8}" y="{gy + wd * pitch + cell - 2}" text-anchor="end" font-size="10.5" fill="{DIM}">{label}</text>')
    by = gy + 7 * pitch + 30
    count = sum(d["contributionCount"] for wk in weeks for d in wk["contributionDays"])
    label = f"{count:,} contributions in the last {'6 months' if mobile else 'year'}"
    out.append(f'<text x="{gx}" y="{by}" font-size="12" fill="{TEXT}">{label}</text>')
    lx = gx + grid_w - pitch - 5 * 14 - 34
    ly = by + 24 if mobile else by
    out.append(f'<text x="{lx - 8}" y="{ly}" text-anchor="end" font-size="10.5" fill="{DIM}">less</text>')
    for i, c in enumerate(LEVELS.values()):
        out.append(f'<rect x="{lx + i * 14}" y="{ly - 10}" width="11" height="11" rx="2" fill="{c}"/>')
    out.append(f'<text x="{lx + 5 * 14 + 4}" y="{ly}" font-size="10.5" fill="{DIM}">more</text>')
    return svg(w, h, f"{s['name']}'s contribution heatmap", f"{label}. Each square is one day, darker to brighter green as contributions increase.", "".join(out))


def tiles_block(s, x, y, w):
    tiles = [
        ("current streak", f"{s['current']}", "days", s["current_sub"]),
        ("longest streak", f"{s['longest']}", "days", s["longest_sub"]),
        ("contributions", f"{s['total']:,}", "", "last 12 months"),
        ("active days", f"{s['active']}", "", s["active_sub"]),
        ("best day", f"{s['best']}", "", s["best_sub"]),
        ("avg / active day", s["avg"], "", "contributions"),
    ]
    cw, rh = w / 2, 66
    out = []
    for i, (label, value, unit, sub) in enumerate(tiles):
        tx, ty = x + (i % 2) * cw, y + (i // 2) * rh
        out.append(f'<rect x="{tx + 6}" y="{ty + 6}" width="{cw - 12}" height="{rh - 10}" rx="6" fill="{BAR}" stroke="{GRID}"/>'
                   f'<text x="{tx + 18}" y="{ty + 24}" font-size="10" letter-spacing=".8" fill="{DIM}">{label.upper()}</text>'
                   f'<text x="{tx + 18}" y="{ty + 49}" font-size="22" font-weight="700" fill="{GREEN}">{value}'
                   f'<tspan font-size="11" font-weight="400" fill="{MUTED}" dx="6">{unit}</tspan></text>'
                   f'<text x="{tx + cw - 18}" y="{ty + 49}" text-anchor="end" font-size="10" fill="{DIM}">{esc(sub)}</text>')
    return "".join(out), 3 * rh


def bars_block(s, x, y, w, h):
    data = s["monthly"]
    top = max(v for _, v in data) or 1
    slot = w / len(data)
    bw = slot * 0.62
    out = [f'<text x="{x + 6}" y="{y + 10}" font-size="10" letter-spacing=".8" fill="{DIM}">CONTRIBUTIONS / MONTH</text>']
    base = y + h - 18
    for i, (m, v) in enumerate(data):
        bh = max(2, (base - y - 26) * v / top)
        bx = x + i * slot + (slot - bw) / 2
        out.append(f'<rect class="fade" style="animation-delay:{0.3 + i * 0.05:.2f}s" x="{bx:.1f}" y="{base - bh:.1f}" '
                   f'width="{bw:.1f}" height="{bh:.1f}" rx="2" fill="{GREEN if v == top else "#26a641"}">'
                   f'<title>{v} in {m:%b %Y}</title></rect>'
                   f'<text x="{bx + bw / 2:.1f}" y="{base + 13}" text-anchor="middle" font-size="9.5" fill="{DIM}">{m:%b}</text>')
        if v == top:
            out.append(f'<text x="{bx + bw / 2:.1f}" y="{base - bh - 5:.1f}" text-anchor="middle" font-size="10" fill="{GREEN}">{v}</text>')
    out.append(f'<path d="M{x} {base + .5}H{x + w}" stroke="{GRID}"/>')
    return "".join(out)


def whoami(s, img, mobile):
    w = 480 if mobile else 1000
    pw = w if mobile else 404
    size = pw - 40
    port_h = 28 + 20 + size + 66
    sx, sw = (0, w) if mobile else (pw + 16, w - pw - 16)
    out = [prompt_line(w / 2, 24, "whoami", 16 if mobile else 14)]

    out.append(panel(0, 44, pw, port_h, "portrait.txt"))
    out.append(portrait_svg(img, s["name"], 20, 44 + 28 + 20, size))
    cap_y = 44 + port_h - 34
    out.append(f'<text x="20" y="{cap_y}" font-size="16" font-weight="700" fill="{TEXT}">{esc(s["name"])}</text>'
               f'<text x="20" y="{cap_y + 19}" font-size="11.5" fill="{MUTED}">{esc(ROLE)}</text>')

    sy = 44 + port_h + 16 if mobile else 44
    tiles, th = tiles_block(s, sx + 8, sy + 34, sw - 16)
    bars_y = sy + 34 + th + 10
    bars_h = 150
    foot_y = bars_y + bars_h + 18
    stats_h = foot_y + 20 - sy
    if not mobile:
        stats_h = max(stats_h, port_h)
        foot_y = sy + stats_h - 16
    out.append(panel(sx, sy, sw, stats_h, "stats --public", f"updated {s['updated']}"))
    out.append(tiles)
    out.append(bars_block(s, sx + 20, bars_y, sw - 40, bars_h))
    meta = f"{s['repos']} public repos · {s['stars']} stars · {s['followers']} followers · since {s['since']}"
    out.append(f'<path d="M{sx + 1} {foot_y - 18.5}H{sx + sw - 1}" stroke="{GRID}"/>'
               f'<text x="{sx + sw / 2}" y="{foot_y}" text-anchor="middle" font-size="11" fill="{MUTED}">{meta}</text>')
    h = (sy + stats_h) + 2
    desc = (f"Portrait of {s['name']}. Current streak {s['current']} days, longest streak {s['longest']} days, "
            f"{s['total']} contributions in the last 12 months over {s['active']} active days, best day {s['best']}, "
            f"average {s['avg']} per active day. {meta}.")
    return svg(w, h, f"whoami: {s['name']}", desc, "".join(out))


def languages(s, mobile):
    w = 480 if mobile else 1000
    langs = s["langs"]
    per_col = len(langs) if mobile else (len(langs) + 1) // 2
    rh = 32
    h = 44 + 28 + 16 + per_col * rh + 40
    out = [prompt_line(w / 2, 24, "./languages.sh", 16 if mobile else 14),
           panel(0, 44, w, h - 44, "languages --by-bytes", "public, non-fork repos")]
    colw = w if mobile else w / 2
    shades = [GREEN, "#2ea043", "#26a641", "#238636", "#196c2e", "#0e4429"]
    for i, (name, share) in enumerate(langs):
        cx = (0 if mobile else (i // per_col) * colw) + 24
        y = 44 + 28 + 26 + (i % per_col) * rh
        bar_x, bar_w = cx + 150, colw - 150 - 24 - 64
        out.append(f'<text x="{cx}" y="{y + 4}" font-size="12" fill="{TEXT}">{esc(name)}</text>'
                   f'<rect x="{bar_x}" y="{y - 6}" width="{bar_w}" height="10" rx="3" fill="{BAR}"/>'
                   f'<rect class="fade" x="{bar_x}" y="{y - 6}" width="{max(3, bar_w * share / langs[0][1]):.1f}" height="10" rx="3" fill="{shades[i]}"/>'
                   f'<text x="{bar_x + bar_w + 56}" y="{y + 4}" text-anchor="end" font-size="12" fill="{MUTED}">{share * 100:.1f}%</text>')
    out.append(f'<text x="24" y="{h - 16}" font-size="10.5" fill="{DIM}">share of code by bytes (GitHub Linguist); notebooks count their outputs</text>')
    desc = "Language share by bytes across public non-fork repositories: " + ", ".join(f"{n} {p * 100:.1f}%" for n, p in langs) + "."
    return svg(w, h, "Language breakdown", desc, "".join(out))


def main():
    login, out_dir = sys.argv[1], sys.argv[2]
    s = summarize(graphql(login))
    img = load_portrait(s["avatar"])
    files = {}
    for mobile in (False, True):
        suffix = "-mobile" if mobile else ""
        files[f"contributions{suffix}.svg"] = contributions(s, mobile)
        files[f"whoami{suffix}.svg"] = whoami(s, img, mobile)
        files[f"languages{suffix}.svg"] = languages(s, mobile)
    os.makedirs(out_dir, exist_ok=True)
    for name, content in files.items():
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
            f.write(content)
        print(f"wrote {name}")


if __name__ == "__main__":
    main()
