"""Draw the static, animated SVGs in assets/ (hero, section prompts, project cards, footer).

GitHub strips scripts and CSS from READMEs, so every animation lives inside an SVG and
uses CSS keyframes only (plus one SMIL gradient sweep on the name). All of them stop
under prefers-reduced-motion and still show their final state.

Usage, from the repo root:
    python .github/scripts/static_assets.py

Edit the text in the settings below, run it, commit the changed files in assets/.
"""
import math
import os
import random
import textwrap
from collections import namedtuple

USER = "jey"
NAME = "Jey Pranav"
ROLE_MAIN = "ML / AI engineering"
ROLE_REST = ""                     # optional muted second part, e.g. "voice AI · agents"
PITCH = ["I build software where models meet real users:",
         "voice AI, LLM agents, RL environments, 3D data",
         "products and brain-to-text research."]
PITCH_MOBILE = ["I build software where models meet real",
                "users: voice AI, LLM agents, RL",
                "environments, 3D data products and",
                "brain-to-text research."]
STATUS = "open to internships and collaborations"
STACK = [("LANGUAGES", "Python · TypeScript · SQL · Bash"),
         ("ML · LLM", "PyTorch · LightGBM · LoRA fine-tuning · agents"),
         ("WEB", "FastAPI · React · Next.js · Three.js"),
         ("SHIP", "Docker · GitHub Actions · Vercel · HF Spaces")]
PROMPTS = {"prompt-projects": "ls ~/projects --featured", "prompt-more": "ls ~/projects --all",
           "prompt-links": "./links.sh"}
FOOTER_CMD = 'echo "thanks for stopping by"'

BG, BAR, BORDER, GRID = "#0d1117", "#161b22", "#30363d", "#21262d"
TEXT, MUTED, DIM = "#c9d1d9", "#8b949e", "#6e7681"
GREEN, GREEN2, RED, AMBER, BLUE = "#39d353", "#26a641", "#f85149", "#d29922", "#58a6ff"
FONT = "ui-monospace,SFMono-Regular,'SF Mono','JetBrains Mono','Cascadia Code',Menlo,Consolas,'Liberation Mono',monospace"
REDUCED = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
BOX = "transform-box:fill-box;transform-origin:center;"
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "assets")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def doc(w, h, title, desc, css, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="t d"><title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>'
            f'<style>{css}{REDUCED}</style><defs>{defs}</defs>'
            f'<rect width="{w}" height="{h}" rx="10" fill="{BG}"/><g font-family="{FONT}">{body}</g></svg>\n')


def write(name, content):
    with open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def typed_prompt(cx, y, cmd, size, loop, delay=0.2):
    """`jey@github ~ $ cmd` with the command typed out and a block cursor.

    A background-coloured cover slides right in steps to reveal the text, which works in
    every browser. textLength pins the glyph widths so the cursor lands on the grid.
    """
    cw = size * 0.6
    n = len(cmd)
    x0 = cx - (len(USER) + 12 + n) * cw / 2  # "@github ~ $ " is 12 columns
    xt = x0 + (len(USER) + 7) * cw
    xc = x0 + (len(USER) + 12) * cw
    w = n * cw
    svg = (f'<g font-size="{size}">'
           f'<text x="{x0:.1f}" y="{y}" textLength="{(len(USER) + 7) * cw:.1f}" fill="{GREEN}">{USER}@github</text>'
           f'<text x="{xt + cw:.1f}" y="{y}" textLength="{3 * cw:.1f}" fill="{MUTED}">~ $</text>'
           f'<clipPath id="ty"><rect x="{xc - 1:.1f}" y="{y - size}" width="{w + cw + 4:.1f}" height="{size * 1.5}"/></clipPath>'
           f'<g clip-path="url(#ty)"><text x="{xc:.1f}" y="{y}" textLength="{w:.1f}" fill="{TEXT}">{esc(cmd)}</text>'
           f'<g class="cv"><rect x="{xc:.1f}" y="{y - size}" width="{w + cw + 6:.1f}" height="{size * 1.5}" fill="{BG}"/>'
           f'<rect class="cur" x="{xc + 2:.1f}" y="{y - size + 2}" width="{cw - 1:.1f}" height="{size + 1}" fill="{GREEN}"/></g></g></g>')
    css = f".cv{{transform:translateX({w:.1f}px);"
    if loop:
        css += (f"animation:ty 10s infinite}}@keyframes ty{{0%{{transform:translateX(0);animation-timing-function:steps({n},end)}}"
                f"12%,88%{{transform:translateX({w:.1f}px);animation-timing-function:steps({n},end)}}"
                f"94%,100%{{transform:translateX(0)}}}}")
    else:
        css += f"animation:ty {n * 0.06:.2f}s steps({n},end) {delay}s backwards}}@keyframes ty{{from{{transform:translateX(0)}}}}"
    css += ".cur{animation:bl 1.1s steps(1,end) infinite}@keyframes bl{50%{opacity:0}}"
    return svg, css


def chrome(x, y, w, h, title, right=""):
    """Terminal window frame, matching the panels dashboard.py draws."""
    out = (f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" rx="8" fill="none" stroke="{BORDER}"/>'
           f'<path d="M{x + 1} {y + 28.5}H{x + w - 1}" stroke="{GRID}"/>')
    for i in range(3):
        out += f'<circle cx="{x + 16 + i * 14}" cy="{y + 14}" r="4" fill="{BORDER}"/>'
    out += f'<text x="{x + 64}" y="{y + 18}" font-size="10.5" letter-spacing=".6" fill="{DIM}">{esc(title)}</text>'
    if right:
        out += f'<text x="{x + w - 14}" y="{y + 18}" text-anchor="end" font-size="10.5" fill="{DIM}">{esc(right)}</text>'
    return out


# ── hero ────────────────────────────────────────────────────────────────────

def hero(mobile):
    w, h = (480, 392) if mobile else (1000, 330)
    top = 46
    pad = 24 if mobile else 28
    ns = 38 if mobile else 44          # name size
    nw = len(NAME) * ns * 0.6
    prompt, css = typed_prompt(w / 2, 26 if mobile else 24, "cat README.md", 16 if mobile else 14, loop=False)
    t0 = 1.1                           # typing has finished
    frames = ["/#_ <%&!*?", "J#_ P%&n*?", "Je_ Pr&na?", "Jey Pra&av"]
    css += (".in{animation:in .7s ease-out backwards}@keyframes in{from{opacity:0;transform:translateY(8px)}}"
            ".f{opacity:0;animation:fl .09s linear}@keyframes fl{from,to{opacity:1}}"
            f".nm{{animation:on .01s linear {t0 + .36:.2f}s backwards}}@keyframes on{{from{{opacity:0}}}}"
            f".glow{{animation:gl 16s ease-in-out infinite alternate}}@keyframes gl{{to{{transform:translate({w * .45:.0f}px,40px)}}}}"
            f".scan{{animation:sc 9s linear infinite}}@keyframes sc{{0%{{transform:translateY(0);opacity:.5}}"
            f"30%{{transform:translateY({h - top - 34}px);opacity:.5}}31%,100%{{transform:translateY({h - top - 34}px);opacity:0}}}}"
            f".ping{{{BOX}animation:pg 2.4s ease-out infinite}}@keyframes pg{{from{{transform:scale(1);opacity:.7}}to{{transform:scale(3.4);opacity:0}}}}")
    css += "".join(f".f{i}{{animation-delay:{t0 + i * .09:.2f}s}}" for i in range(len(frames)))
    defs = (f'<radialGradient id="gl"><stop offset="0" stop-color="{GREEN}" stop-opacity=".2"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></radialGradient>'
            f'<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="11" cy="11" r=".9" fill="{BORDER}"/></pattern>'
            f'<linearGradient id="fadeR" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity=".9"/></linearGradient>'
            f'<mask id="dm"><rect width="{w}" height="{h}" fill="url(#fadeR)"/></mask>'
            f'<clipPath id="pc"><rect x="1" y="{top + 29}" width="{w - 2}" height="{h - top - 31}" rx="7"/></clipPath>'
            f'<linearGradient id="sh" gradientUnits="userSpaceOnUse" x1="-260" y1="0" x2="0" y2="0">'
            f'<stop offset="0" stop-color="{TEXT}"/><stop offset=".5" stop-color="#aff5b4"/><stop offset="1" stop-color="{TEXT}"/>'
            f'<animate attributeName="x1" values="-260;{w + 200}" dur="7s" repeatCount="indefinite"/>'
            f'<animate attributeName="x2" values="0;{w + 460}" dur="7s" repeatCount="indefinite"/></linearGradient>')
    ny = top + (86 if mobile else 92)
    b = [prompt,
         f'<g clip-path="url(#pc)"><rect y="{top}" width="{w}" height="{h}" fill="url(#dots)" mask="url(#dm)"/>'
         f'<circle class="glow" cx="{w * .2:.0f}" cy="{top + 110}" r="{230 if mobile else 300}" fill="url(#gl)"/>'
         f'<rect class="scan" x="1" y="{top + 30}" width="{w - 2}" height="1.5" fill="{GREEN}" opacity="0"/></g>',
         chrome(0, top, w, h - top - 2, "README.md", "" if mobile else "github.com/Pranav-0710")]
    name_attr = f'x="{pad}" y="{ny}" font-size="{ns}" font-weight="700" letter-spacing="0" textLength="{nw:.0f}"'
    for i, fr in enumerate(frames):
        b.append(f'<text class="f f{i}" {name_attr} fill="{GREEN}">{esc(fr)}</text>')
    b.append(f'<g class="nm"><text {name_attr} fill="url(#sh)">{esc(NAME)}</text>'
             f'<rect class="cur" x="{pad + nw + 12:.0f}" y="{ny - ns * .78:.0f}" width="{ns * .42:.0f}" height="{ns * .9:.0f}" rx="2" fill="{GREEN}"/></g>')
    d = t0 + .6
    if mobile:
        b.append(f'<g class="in" style="animation-delay:{d:.1f}s" font-size="16"><text x="{pad}" y="{ny + 36}" fill="{GREEN}">{esc(ROLE_MAIN)}</text>'
                 + (f'<text x="{pad}" y="{ny + 60}" fill="{MUTED}">{esc(ROLE_REST)}</text>' if ROLE_REST else '') + '</g>')
        py, step, fs, lines = ny + (100 if ROLE_REST else 76), 24, 15.5, PITCH_MOBILE
    else:
        b.append(f'<text class="in" style="animation-delay:{d:.1f}s" x="{pad}" y="{ny + 32}" font-size="15">'
                 f'<tspan fill="{GREEN}">{esc(ROLE_MAIN)}</tspan>'
                 + (f'<tspan fill="{MUTED}"> · {esc(ROLE_REST)}</tspan>' if ROLE_REST else '') + '</text>')
        py, step, fs, lines = ny + 72, 22, 14, PITCH
    b.append(f'<g class="in" style="animation-delay:{d + .3:.1f}s" font-size="{fs}" fill="{TEXT}">'
             + "".join(f'<text x="{pad}" y="{py + i * step}">{esc(t)}</text>' for i, t in enumerate(lines)) + '</g>')
    sy = h - (26 if mobile else 24)
    b.append(f'<g class="in" style="animation-delay:{d + 1.5:.1f}s"><circle class="ping" cx="{pad + 6}" cy="{sy - 4}" r="4" fill="{GREEN}"/>'
             f'<circle cx="{pad + 6}" cy="{sy - 4}" r="4" fill="{GREEN}"/>'
             f'<text x="{pad + 20}" y="{sy}" font-size="{14 if mobile else 12}" fill="{MUTED}">{esc(STATUS)}</text></g>')
    if not mobile:
        b.append(f'<path class="in" style="animation-delay:{d + .6:.1f}s" d="M560.5 {top + 52}V{h - 22}" stroke="{GRID}"/>')
        for i, (k, v) in enumerate(STACK):
            y = top + 68 + i * 50
            b.append(f'<g class="in" style="animation-delay:{d + .6 + i * .18:.2f}s">'
                     f'<rect x="592" y="{y - 8}" width="3" height="30" rx="1.5" fill="{GREEN}"/>'
                     f'<text x="606" y="{y}" font-size="10" letter-spacing=".8" fill="{DIM}">{esc(k)}</text>'
                     f'<text x="606" y="{y + 20}" font-size="13.5" fill="{TEXT}">{esc(v)}</text></g>')
    desc = f"{ROLE_MAIN}{', ' + ROLE_REST if ROLE_REST else ''}. {' '.join(PITCH)} {STATUS.capitalize()}."
    return doc(w, h, f"{NAME}: {ROLE_MAIN.lower()}", desc, css, "".join(b), defs)


def prompt(cmd, mobile):
    w = 480 if mobile else 1000
    body, css = typed_prompt(w / 2, 25, cmd, 16 if mobile else 14, loop=True)
    return doc(w, 40, f"{USER}@github ~ $ {cmd}", f"Terminal prompt: {cmd}", css, body)


def wave(y, amp, comps, x0, x1, period, step=4):
    pts = []
    x = x0
    while x <= x1:
        v = sum(a * math.sin(2 * math.pi * n * x / period + ph) for n, a, ph in comps)
        pts.append(f"{x},{y + amp * v:.1f}")
        x += step
    return "M" + " L".join(pts)


def footer(mobile):
    w, h = (480, 110) if mobile else (1000, 110)
    body, css = typed_prompt(w / 2, 30, FOOTER_CMD, 14 if mobile else 14, loop=True)
    css += (".w1{animation:w 9s linear infinite}.w2{animation:w 14s linear infinite reverse}"
            "@keyframes w{to{transform:translateX(-240px)}}")
    defs = (f'<clipPath id="fc"><rect width="{w}" height="{h}" rx="10"/></clipPath>'
            f'<linearGradient id="fe" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".2" stop-color="#fff"/>'
            f'<stop offset=".8" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<mask id="fm"><rect width="{w}" height="{h}" fill="url(#fe)"/></mask>')
    body += (f'<g clip-path="url(#fc)" mask="url(#fm)" fill="none" stroke-linecap="round">'
             f'<path class="w1" d="{wave(76, 12, [(1, 1, 0), (3, .35, 1)], 0, w + 240, 240)}" stroke="{GREEN}" stroke-width="1.6"/>'
             f'<path class="w2" d="{wave(80, 9, [(2, 1, 2), (1, .5, 0)], 0, w + 240, 240)}" stroke="{GREEN2}" stroke-width="1.2" opacity=".55"/></g>')
    return doc(w, h, "Thanks for stopping by", "Closing terminal line over two flowing wave lines.", css, body, defs)


# ── project cards (480 x 120, shown above each project's text) ───────────────

Scene = namedtuple("Scene", "title desc caption css body defs cap_x")


def card(title, desc, caption, css, body, defs="", cap_x=18):
    return Scene(title, desc, caption, css, body, defs, cap_x)


def scene_frame(sc):
    return (f'<rect x=".5" y=".5" width="479" height="119" rx="8" fill="{BG}" stroke="{GRID}"/>'
            f'<text x="{sc.cap_x}" y="21" font-size="10.5" letter-spacing=".4" fill="{DIM}">{esc(sc.caption)}</text>')


def render_card(sc):
    """A scene as a standalone 480 x 120 SVG (the small cards in the "more projects" fold-out)."""
    return doc(480, 120, sc.title, sc.desc, sc.css, scene_frame(sc) + sc.body, sc.defs)


def card_reliefroute():
    a, bb, c, dep, via = (200, 40), (330, 84), (430, 44), (60, 88), (300, 26)
    css = (".p{fill:none;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1}"
           f".p1{{stroke:{GREEN};animation:p1 10s linear infinite}}"
           "@keyframes p1{0%{stroke-dashoffset:1}18%,90%{stroke-dashoffset:0;opacity:1}96%,100%{stroke-dashoffset:0;opacity:0}}"
           f".p2{{stroke:{RED};opacity:0;animation:p2 10s linear infinite}}"
           f"@keyframes p2{{0%,14%{{stroke-dashoffset:1;stroke:{DIM};opacity:1}}26%,32%{{stroke-dashoffset:0;stroke:{DIM};opacity:1}}"
           f"36%,44%{{stroke-dashoffset:0;stroke:{RED};opacity:1}}50%,100%{{stroke-dashoffset:0;stroke:{RED};opacity:0}}}}"
           f".p3{{stroke:{GREEN};animation:p3 10s linear infinite}}"
           "@keyframes p3{0%,42%{stroke-dashoffset:1}56%,90%{stroke-dashoffset:0;opacity:1}96%,100%{stroke-dashoffset:0;opacity:0}}"
           f".p4{{stroke:{GREEN};animation:p4 10s linear infinite}}"
           "@keyframes p4{0%,70%{stroke-dashoffset:1}82%,90%{stroke-dashoffset:0;opacity:1}96%,100%{stroke-dashoffset:0;opacity:0}}"
           f".fl{{{BOX}animation:fl 10s ease-out infinite}}"
           "@keyframes fl{0%,28%{opacity:0;transform:scale(.4)}34%,90%{opacity:1;transform:scale(1)}96%,100%{opacity:0;transform:scale(1)}}"
           f".tr{{transform:translate({c[0]}px,{c[1]}px);animation:tr 10s linear infinite}}"
           f"@keyframes tr{{0%{{transform:translate({dep[0]}px,{dep[1]}px);opacity:1}}18%,52%{{transform:translate({a[0]}px,{a[1]}px)}}"
           f"62%{{transform:translate({via[0]}px,{via[1]}px)}}70%,72%{{transform:translate({bb[0]}px,{bb[1]}px)}}"
           f"84%,90%{{transform:translate({c[0]}px,{c[1]}px);opacity:1}}96%,100%{{transform:translate({c[0]}px,{c[1]}px);opacity:0}}}}")
    grid = "".join(f'<path d="M{x} 30V110" stroke="{BAR}"/>' for x in range(40, 480, 40))
    grid += "".join(f'<path d="M12 {y}H468" stroke="{BAR}"/>' for y in (50, 70, 90))
    stops = "".join(f'<circle cx="{x}" cy="{y}" r="6" fill="{BG}" stroke="{MUTED}" stroke-width="1.5"/>' for x, y in (a, bb, c))
    body = (grid
            + f'<path class="p p2" pathLength="1" d="M{a[0]} {a[1]}L{bb[0]} {bb[1]}"/>'
            + f'<g class="fl"><circle cx="265" cy="62" r="19" fill="{BLUE}" opacity=".22"/>'
              f'<path d="M258 55l14 14m0-14l-14 14" stroke="{RED}" stroke-width="2.5" stroke-linecap="round"/></g>'
            + f'<path class="p p1" pathLength="1" d="M{dep[0]} {dep[1]}L{a[0]} {a[1]}"/>'
            + f'<path class="p p3" pathLength="1" d="M{a[0]} {a[1]}L{via[0]} {via[1]}L{bb[0]} {bb[1]}"/>'
            + f'<path class="p p4" pathLength="1" d="M{bb[0]} {bb[1]}L{c[0]} {c[1]}"/>'
            + stops
            + f'<rect x="{dep[0] - 7}" y="{dep[1] - 7}" width="14" height="14" rx="3" fill="{GREEN2}"/>'
              f'<text x="{dep[0]}" y="{dep[1] + 22}" text-anchor="middle" font-size="10" fill="{DIM}">depot</text>'
            + f'<circle class="tr" r="5" fill="#fff" stroke="{GREEN}" stroke-width="2"/>')
    return card("ReliefRoute", "A truck leaves the depot, a road floods, and the route is redrawn around it.",
                "replans around a blocked road", css, body)


def card_dhwani():
    rnd = random.Random(7)
    css = (f".b{{{BOX}animation:eq 1s ease-in-out infinite alternate}}@keyframes eq{{from{{transform:scaleY(.2)}}}}"
           ".n{opacity:0;animation:n 4.5s linear infinite}@keyframes n{0%,30%{opacity:1}34%,100%{opacity:0}}"
           ".n2{animation-delay:1.5s}.n3{animation-delay:3s}"
           ".pd{transform:translateX(458px);animation:pd 4.5s linear infinite}@keyframes pd{from{transform:translateX(28px)}}")
    bars = ""
    for i in range(12):
        hgt = rnd.randint(14, 46)
        bars += (f'<rect class="b" style="animation-delay:-{rnd.random():.2f}s;animation-duration:{.7 + rnd.random() * .7:.2f}s" '
                 f'x="{28 + i * 9}" y="{62 - hgt / 2}" width="5" height="{hgt}" rx="2.5" fill="{GREEN if i % 3 else GREEN2}"/>')
    nodes = ""
    for i, (name, verb) in enumerate((("Prisma", "transcribe"), ("Laya", "decide"), ("Timbre", "speak"))):
        x = 170 + i * 102
        nodes += (f'<path d="M{x - 18} 62H{x}" stroke="{BORDER}"/>'
                  f'<rect x="{x + .5}" y="40.5" width="83" height="43" rx="6" fill="{BAR}" stroke="{BORDER}"/>'
                  f'<rect class="n n{i + 1}" x="{x + .5}" y="40.5" width="83" height="43" rx="6" fill="none" stroke="{GREEN}" stroke-width="1.5"/>'
                  f'<text x="{x + 42}" y="60" text-anchor="middle" font-size="12.5" font-weight="700" fill="{TEXT}">{name}</text>'
                  f'<text x="{x + 42}" y="75" text-anchor="middle" font-size="10" fill="{MUTED}">{verb}</text>')
    body = bars + nodes + f'<path d="M28 100H458" stroke="{GRID}"/><circle class="pd" cy="100" r="3" fill="{GREEN}"/>'
    return card("dhwani-desk", "A caller's voice passes through transcription, a local decision engine and speech synthesis.",
                "voice in · local decision · voice out", css, body)


def card_dataeng():
    css = "".join(f".s{i}{{animation:s{i} 10s linear infinite}}@keyframes s{i}{{0%,{15 + i * 20}%{{opacity:0}}"
                  f"{18 + i * 20}%,94%{{opacity:1}}100%{{opacity:0}}}}" for i in range(4))
    css += (".rw{transform-box:fill-box;transform-origin:left center;animation:rw 10s ease-in-out infinite}"
            "@keyframes rw{0%,15%{transform:scaleX(0)}18%,35%{transform:scaleX(.25)}38%,55%{transform:scaleX(.5)}"
            "58%,75%{transform:scaleX(.75)}78%,94%{transform:scaleX(1)}100%{transform:scaleX(0)}}")
    body = ""
    for i, name in enumerate(("schema", "scaling", "leakage", "fairness")):
        x = 18 + i * 113
        if i:
            body += f'<path d="M{x - 13} 58h9m-4 -4l4 4l-4 4" stroke="{DIM}" fill="none"/>'
        body += (f'<rect x="{x + .5}" y="38.5" width="99" height="39" rx="6" fill="{BAR}" stroke="{RED}" stroke-opacity=".7"/>'
                 f'<circle cx="{x + 16}" cy="58" r="4" fill="{RED}"/>'
                 f'<text x="{x + 28}" y="62" font-size="12" fill="{MUTED}">{name}</text>'
                 f'<g class="s{i}"><rect x="{x + .5}" y="38.5" width="99" height="39" rx="6" fill="{BAR}" stroke="{GREEN}"/>'
                 f'<circle cx="{x + 16}" cy="58" r="4" fill="{GREEN}"/>'
                 f'<text x="{x + 28}" y="62" font-size="12" fill="{TEXT}">{name}</text></g>')
    body += (f'<text x="18" y="102" font-size="10.5" fill="{DIM}">reward</text>'
             f'<rect x="72" y="94" width="388" height="8" rx="4" fill="{BAR}"/>'
             f'<rect class="rw" x="72" y="94" width="388" height="8" rx="4" fill="{GREEN}"/>')
    return card("DataEngEnv", "Four failing pipeline stages turn green one by one as a reward bar fills.",
                "agent repairs the pipeline, stage by stage", css, body)


def card_signal():
    rnd = random.Random(11)
    css = (".l{fill:none;stroke-width:2;stroke-linecap:round;stroke-dasharray:1;animation:l0 10s linear infinite}"
           + "".join(f".l{j}{{animation-name:l{j}}}@keyframes l{j}{{0%,{8 + j * 18}%{{stroke-dashoffset:1}}"
                     f"{18 + j * 18}%,88%{{stroke-dashoffset:0;opacity:1}}94%,100%{{stroke-dashoffset:0;opacity:0}}}}" for j in range(3))
           + ".sw{animation:sw 10s linear infinite}@keyframes sw{0%{transform:translateX(0);opacity:.9}"
             "60%{transform:translateX(434px);opacity:.9}61%,100%{transform:translateX(434px);opacity:0}}"
             ".tg{animation:tg 10s linear infinite}@keyframes tg{0%,62%{opacity:0}66%,88%{opacity:1}94%,100%{opacity:0}}")
    body = ""
    for i in range(6):
        px, on = 18 + i * 75, i % 2 == 0
        body += f'<rect x="{px + .5}" y="32.5" width="68" height="58" rx="3" fill="{BAR}" stroke="{GRID}"/>'
        for _ in range(26):
            body += (f'<rect x="{px + rnd.randint(3, 61)}" y="{rnd.randint(35, 86)}" width="{rnd.choice((2, 3, 4))}" height="2" '
                     f'fill="{GREEN2}" opacity="{rnd.choice((.15, .25, .35))}"/>')
        if on:
            j = i // 2
            body += f'<path class="l l{j}" pathLength="1" d="M{px + 16 + j * 14} 36L{px + 26 + j * 14} 87" stroke="{GREEN}"/>'
        body += (f'<text x="{px + 34}" y="106" text-anchor="middle" font-size="10.5" fill="{GREEN if on else DIM}">'
                 f'{"ON" if on else "OFF"}</text>')
    body += (f'<rect class="sw" x="18" y="32" width="3" height="59" fill="{GREEN}" opacity="0"/>'
             f'<g class="tg"><rect x="358.5" y="8.5" width="103" height="18" rx="9" fill="{BAR}" stroke="{GREEN}"/>'
             f'<text x="410" y="21" text-anchor="middle" font-size="10.5" fill="{GREEN}">eti_candidate</text></g>')
    return card("signal-hunters", "Six radio-telescope panels alternate ON and OFF; a drifting line appears only in the ON panels and the cadence is labelled a candidate.",
                "a drifting line, in ON panels only", css, body)


def card_terrain():
    cx, cy, r = 70, 64, 40
    css = (f".m{{{BOX}animation:m 6s ease-in-out infinite}}@keyframes m{{0%,100%{{transform:scaleX(1)}}50%{{transform:scaleX(0)}}}}"
           f".e{{{BOX}animation:e 2.2s ease-out infinite}}@keyframes e{{from{{transform:scale(1);opacity:.8}}to{{transform:scale(4);opacity:0}}}}"
           ".a{fill:none;stroke-dasharray:1;animation:a 8s linear infinite}"
           + "".join(f".a{i}{{animation-name:a{i}}}@keyframes a{i}{{0%,{8 + i * 22}%{{stroke-dashoffset:1}}"
                     f"{20 + i * 22}%,90%{{stroke-dashoffset:0;opacity:1}}96%,100%{{stroke-dashoffset:0;opacity:0}}}}"
                     f".t{i}{{animation:t{i} 8s linear infinite}}@keyframes t{i}{{0%,{20 + i * 22}%{{opacity:0}}"
                     f"{24 + i * 22}%,90%{{opacity:1}}96%,100%{{opacity:0}}}}" for i in range(3)))
    body = (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{BAR}" stroke="{GREEN2}" stroke-width="1.2"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="12" fill="none" stroke="{GREEN2}" stroke-opacity=".5"/>'
            f'<ellipse cx="{cx}" cy="{cy - 22}" rx="33" ry="8" fill="none" stroke="{GREEN2}" stroke-opacity=".35"/>'
            f'<ellipse cx="{cx}" cy="{cy + 22}" rx="33" ry="8" fill="none" stroke="{GREEN2}" stroke-opacity=".35"/>')
    for k in range(3):
        body += (f'<circle class="m" style="animation-delay:-{k * 2}s" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GREEN2}" '
                 f'stroke-opacity=".6" vector-effect="non-scaling-stroke"/>')
    dots = ((58, 50), (88, 68), (74, 88))
    rows = ((42, 150, "agrees", GREEN), (66, 118, "differs", AMBER), (90, 164, "agrees", GREEN))
    for i, ((dx, dy), (ry, bw, tag, col)) in enumerate(zip(dots, rows)):
        body += (f'<path class="a a{i}" pathLength="1" d="M{dx} {dy}Q{120} {ry - 16} 146 {ry}" stroke="{DIM}"/>'
                 f'<circle class="e" style="animation-delay:-{i * .7:.1f}s" cx="{dx}" cy="{dy}" r="2.5" fill="{GREEN}"/>'
                 f'<circle cx="{dx}" cy="{dy}" r="2.5" fill="{GREEN}"/>'
                 f'<rect x="152" y="{ry - 5}" width="30" height="9" rx="4.5" fill="{BORDER}"/>'
                 f'<rect x="190" y="{ry - 5}" width="{bw}" height="9" rx="4.5" fill="{GRID}"/>'
                 f'<g class="t{i}"><rect x="384.5" y="{ry - 9.5}" width="77" height="18" rx="9" fill="{BAR}" stroke="{col}"/>'
                 f'<text x="423" y="{ry + 3.5}" text-anchor="middle" font-size="10.5" fill="{col}">{tag}</text></g>')
    return card("Terrain", "A rotating globe sends three events to a list where each outlet's framing is tagged as agreeing or differing.",
                "one story, compared across outlets", css, body, cap_x=152)


def card_neuro():
    css = (".tr{animation:tr 7s linear infinite}@keyframes tr{to{transform:translateX(-240px)}}"
           ".hl{animation:hl 4.2s steps(6,end) infinite}@keyframes hl{to{transform:translateX(138px)}}")
    rnd = random.Random(3)
    traces = ""
    for k in range(4):
        comps = [(rnd.choice((2, 3)), 1, rnd.random() * 6), (rnd.choice((5, 7, 9)), .5, rnd.random() * 6), (12, .22, rnd.random() * 6)]
        traces += (f'<path d="{wave(40 + k * 18, 5.5, comps, 18, 300 + 240, 240, 3)}" fill="none" '
                   f'stroke="{GREEN if k % 2 == 0 else GREEN2}" stroke-width="1.4" stroke-linejoin="round"/>')
    defs = ('<clipPath id="nc"><rect x="18" y="28" width="270" height="76"/></clipPath>'
            '<linearGradient id="nf" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".15" stop-color="#fff"/>'
            '<stop offset=".85" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            '<mask id="nm"><rect x="18" y="28" width="270" height="76" fill="url(#nf)"/></mask>')
    body = f'<g clip-path="url(#nc)" mask="url(#nm)"><g class="tr">{traces}</g></g>'
    body += f'<path d="M298 66h18m-5 -5l5 5l-5 5" stroke="{DIM}" fill="none"/>'
    for i in range(6):
        x = 326 + i * 23
        body += (f'<rect x="{x + .5}" y="52.5" width="19" height="27" rx="3" fill="{BAR}" stroke="{BORDER}"/>'
                 f'<rect x="{x + 6}" y="72" width="8" height="1.5" fill="{DIM}"/>')
    body += (f'<rect class="hl" x="326.5" y="52.5" width="19" height="27" rx="3" fill="{GREEN}" fill-opacity=".12" stroke="{GREEN}"/>'
             f'<text x="393" y="98" text-anchor="middle" font-size="10.5" fill="{DIM}">one character at a time</text>')
    return card("neuroselect", "Scrolling MEG channel traces feed a row of character slots that are scanned one at a time.",
                "MEG channels to character-level CTC", css, body, defs)


# ── project panels: one wide panel per featured project ─────────────────────
# Animated scene + one-sentence pitch + three numbers + stack. Every number comes from the
# project's own README; edit the text here, run this script, commit the changed files in assets/.

PROJECTS = [
    dict(slug="dataengenv", folder="DataEngEnv", repo="DataEngEnv", scene=card_dataeng, title="DataEngEnv",
         pill="Meta AI × Hugging Face OpenEnv Hackathon 2026",
         tagline="PipelineOps Arena: a 4-stage environment where an LLM agent repairs a broken ML pipeline. "
                 "Rewards come from running the fixed code, not from an LLM judge.",
         metrics=[("4", "cascading stages", "schema → fairness"), ("0.25→0.38", "avg reward", "25-step GRPO run"),
                  ("live", "Hugging Face", "Space you can try")],
         chips=["Python", "FastAPI", "Docker", "OpenEnv", "Unsloth", "LoRA", "GRPO"], mark="LLaMA 3.1 8B fine-tune"),
    dict(slug="dhwani-desk", folder="dhwani-desk", repo="dhwani-desk", scene=card_dhwani, title="dhwani-desk",
         pill="Gnani AI · Great Indian AI Internship Challenge",
         tagline="A Kannada voice helpline for civic complaints that hands danger to a person first. "
                 "Every decision runs locally on a CPU.",
         metrics=[("30/34", "hazards caught", "held-out test calls"), ("0.71", "department F1", "macro, up from 0.13"),
                  ("1.5 s", "first reply", "approximate latency")],
         chips=["Python", "FastAPI", "React", "TypeScript", "Laya"], mark="no LLM in the call"),
    dict(slug="terrain", folder="Terrain", repo="Terrain", scene=card_terrain, title="Terrain",
         pill="Built for the OpenAI Hackathon",
         tagline="News intelligence on a 3D WebGL globe: compare how outlets around the world frame the same event, "
                 "with LLM consensus and contradiction analysis.",
         metrics=[("3D", "WebGL globe", "live events on a map"), ("GDELT", "+ RSS ingestion", "geocoded news"),
                  ("30-day", "scenario sim", "red-team mode")],
         chips=["Next.js", "React", "Three.js", "FastAPI", "Supabase", "PostGIS"], mark="live demo"),
    dict(slug="neuroselect", folder="neuroselect", repo="neuroselect", scene=card_neuro, title="neuroselect",
         pill="Research codebase · baseline stage",
         tagline="Reproducible groundwork for non-invasive brain-to-text decoding: a character-level CTC baseline "
                 "on public MEG data. Audits come first.",
         metrics=[("306", "MEG channels", "public SpanishBCBL"), ("8", "real trials", "extracted, audited"),
                  ("50 Hz", "processed rate", "from 1000 Hz MEG")],
         chips=["Python", "PyTorch", "MNE", "NumPy", "SciPy", "pytest"], mark="no benchmark claimed"),
]


def wrap(text, size, width):
    return textwrap.wrap(text, max(10, int(width / (size * 0.62))))


def chips_flow(chips, mark, x, y, max_w, size=11, gap=8):
    """Chips left to right, wrapping at max_w. Returns (svg, bottom y)."""
    out, cx, cy = [], x, y
    for label, hi in [(c, False) for c in chips] + ([(mark, True)] if mark else []):
        cw = len(label) * size * 0.6 + 18
        if cx + cw > x + max_w:
            cx, cy = x, cy + 28
        out.append(f'<rect x="{cx:.1f}" y="{cy}" width="{cw:.1f}" height="22" rx="11" fill="{GREEN if hi else BAR}" '
                   f'fill-opacity="{.12 if hi else 1}" stroke="{GREEN if hi else BORDER}"/>'
                   f'<text x="{cx + cw / 2:.1f}" y="{cy + 15}" text-anchor="middle" font-size="{size}" '
                   f'fill="{GREEN if hi else MUTED}">{esc(label)}</text>')
        cx += cw + gap
    return "".join(out), cy + 22


def metric_tiles(metrics, x, y, total_w, h=72, gap=12):
    tw = (total_w - gap * (len(metrics) - 1)) / len(metrics)
    out = []
    for i, (val, label, sub) in enumerate(metrics):
        tx = x + i * (tw + gap)
        out.append(f'<g class="rv" style="animation-delay:{.45 + i * .12:.2f}s">'
                   f'<rect x="{tx + .5:.1f}" y="{y + .5}" width="{tw - 1:.1f}" height="{h - 1}" rx="6" fill="{BAR}" stroke="{GRID}"/>'
                   f'<text x="{tx + 14:.1f}" y="{y + 29}" font-size="{21 if len(val) <= 6 else 17}" font-weight="700" fill="{GREEN}">{esc(val)}</text>'
                   f'<text x="{tx + 14:.1f}" y="{y + 47}" font-size="11" fill="{TEXT}">{esc(label)}</text>'
                   f'<text x="{tx + 14:.1f}" y="{y + 62}" font-size="9.5" fill="{DIM}">{esc(sub)}</text></g>')
    return "".join(out)


def project_panel(spec, mobile, flip):
    sc = spec["scene"]()
    w = 480 if mobile else 1000
    css = ".rv{animation:rv .7s ease-out backwards}@keyframes rv{from{opacity:0;transform:translateY(8px)}}" + sc.css

    def reveal(d, inner):
        return f'<g class="rv" style="animation-delay:{d:.2f}s">{inner}</g>'

    def pill(x, y):
        pw = len(spec["pill"]) * 6.4 + 34
        return reveal(.1, f'<rect x="{x + .5}" y="{y + .5}" width="{pw:.1f}" height="21" rx="10.5" fill="{BAR}" stroke="{BORDER}"/>'
                          f'<circle cx="{x + 13}" cy="{y + 11}" r="3" fill="{GREEN}"/>'
                          f'<text x="{x + 24}" y="{y + 15}" font-size="11" fill="{MUTED}">{esc(spec["pill"])}</text>')

    def title(x, y, size):
        return reveal(.2, f'<rect x="{x}" y="{y - size * .82:.1f}" width="3" height="{size * .95:.1f}" rx="1.5" fill="{GREEN}"/>'
                          f'<text x="{x + 14}" y="{y}" font-size="{size}" font-weight="700" fill="{TEXT}">{esc(spec["title"])}</text>')

    def tagline(x, y, lines, size, step):
        return reveal(.3, f'<g font-size="{size}" fill="{MUTED}">' + "".join(
            f'<text x="{x}" y="{y + i * step}">{esc(t)}</text>' for i, t in enumerate(lines)) + '</g>')

    def media(x, y, scale):
        return reveal(.15, f'<g transform="translate({x},{y}) scale({scale})">{scene_frame(sc)}{sc.body}</g>')

    parts = []
    if mobile:
        pad, cw = 16, w - 32
        parts += [pill(pad, 46), media(pad, 80, cw / 480)]
        ty = 80 + 120 * cw / 480 + 40
        parts.append(title(pad, ty, 24))
        lines = wrap(spec["tagline"], 13, cw)
        parts.append(tagline(pad, ty + 30, lines, 13, 20))
        ky = ty + 30 + len(lines) * 20 + 4
        parts.append(metric_tiles(spec["metrics"], pad, ky, cw, gap=10))
        chips_svg, bottom = chips_flow(spec["chips"], spec["mark"], pad, ky + 72 + 18, cw)
        h = bottom + 24
    else:
        mx, tx = (496, 24) if flip else (24, 540)
        col = 436
        parts += [pill(tx, 50), title(tx, 108, 28)]
        lines = wrap(spec["tagline"], 14, col)
        parts.append(tagline(tx, 140, lines, 14, 21))
        chips_svg, bottom = chips_flow(spec["chips"], spec["mark"], tx, 140 + len(lines) * 21 + 6, col)
        parts += [media(mx, 52, 1), metric_tiles(spec["metrics"], mx, 188, 480)]
        h = max(bottom, 260) + 28
    parts.append(f'<g class="rv" style="animation-delay:.6s">{chips_svg}</g>')
    h = int(math.ceil(h))
    right = "" if mobile else f"github.com/Pranav-0710/{spec['repo']}"
    body = chrome(0, 0, w, h, f"~/projects/{spec['folder']}", right) + "".join(parts)
    desc = (f"{spec['title']}. {spec['tagline']} "
            + " ".join(f"{v} {l} ({s})." for v, l, s in spec["metrics"])
            + f" Built with {', '.join(spec['chips'])}.")
    return doc(w, h, f"{spec['title']}: project panel", desc, css, body, sc.defs)


def animate_buttons():
    """Give the arrow on each link button a small nudge loop. Safe to run repeatedly."""
    for name in ("btn-linkedin", "btn-email"):
        path = os.path.join(OUT, name + ".svg")
        s = open(path, encoding="utf-8").read()
        if "class=\"ar\"" in s:
            continue
        s = s.replace("</title>", "</title>\n  <style>.ar{animation:ar 1.8s ease-in-out infinite}"
                                  "@keyframes ar{50%{transform:translate(2px,-2px)}}" + REDUCED + "</style>", 1)
        s = s.replace('fill="#8b949e">↗', 'fill="#39d353" class="ar">↗', 1)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(s)


def main():
    write("hero", hero(False))
    write("hero-mobile", hero(True))
    for name, cmd in PROMPTS.items():
        write(name, prompt(cmd, False))
        write(name + "-mobile", prompt(cmd, True))
    write("footer", footer(False))
    write("footer-mobile", footer(True))
    for name, fn in (("reliefroute", card_reliefroute), ("signal-hunters", card_signal)):
        write("card-" + name, render_card(fn()))
    for i, spec in enumerate(PROJECTS):
        write("project-" + spec["slug"], project_panel(spec, False, flip=False))   # flip=True mirrors a panel (scene right, text left)
        write("project-" + spec["slug"] + "-mobile", project_panel(spec, True, flip=False))
    animate_buttons()


if __name__ == "__main__":
    main()
