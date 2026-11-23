"""Generates the animated profile banner and the project/stack matrix, dark and light."""
import base64
import math
import sys

OUT = sys.argv[1]
SB = base64.b64encode(open("assets/fonts/chakra-sb.woff2", "rb").read()).decode()
RG = base64.b64encode(open("assets/fonts/chakra-r.woff2", "rb").read()).decode()

THEMES = {
    "dark": dict(board="#0E1A2B", dot="#1B2E46", trace="#2A4766", pad="#C99A35", lit="#FFD66E",
                 signal="#8FD3FF", text="#EAF0F7", muted="#93A7BF", ring="#35557A"),
    "light": dict(board="#F3F6FA", dot="#DDE5EF", trace="#B7C6D8", pad="#B8861B", lit="#E7A91C",
                  signal="#1E78C2", text="#10233A", muted="#52667E", ring="#B7C6D8"),
}

FONTS = f"""@font-face{{font-family:Chakra;font-weight:600;src:url(data:font/woff2;base64,{SB}) format('woff2')}}
@font-face{{font-family:Chakra;font-weight:400;src:url(data:font/woff2;base64,{RG}) format('woff2')}}"""

# ---------------------------------------------------------------- banner

W, H = 1200, 340
# Trace: board → cloud → screen, routed like a PCB track with 45° bends.
PTS = [(24, 278), (190, 278), (230, 238), (560, 238), (600, 278), (1000, 278), (1040, 238), (1176, 238)]
PADS = [((190, 278), "ESP32 firmware"), ((395, 238), "Firebase"), ((1040, 238), "Web and Android")]


def seglen(a, b):
    return math.dist(a, b)


TOTAL = sum(seglen(PTS[i], PTS[i + 1]) for i in range(len(PTS) - 1))


def frac_of(pt):
    """Fraction of the path length at which point pt (on the path) sits."""
    acc = 0.0
    for i in range(len(PTS) - 1):
        a, b = PTS[i], PTS[i + 1]
        L = seglen(a, b)
        # point on segment?
        if abs(seglen(a, pt) + seglen(pt, b) - L) < 0.5:
            return (acc + seglen(a, pt)) / TOTAL
        acc += L
    raise ValueError(pt)


def banner(t):
    c = THEMES[t]
    d = "M" + " L".join(f"{x} {y}" for x, y in PTS)
    run = 0.72  # share of the cycle the pulse is travelling; the rest is a pause
    dur = 4.2
    glows = []
    css_pad = []
    for i, ((x, y), label) in enumerate(PADS):
        f = frac_of((x, y)) * run * 100
        css_pad.append(
            f"@keyframes p{i}{{0%,{max(f-2,0):.1f}%{{opacity:0}}{f:.1f}%{{opacity:1}}{min(f+14,99):.1f}%,100%{{opacity:0}}}}"
            f".g{i}{{animation:p{i} {dur}s linear infinite}}"
        )
        anchor = "middle"
        glows.append(f"""
  <g>
    <rect x="{x-22}" y="{y-11}" width="44" height="22" rx="5" fill="{c['pad']}"/>
    <rect class="glow g{i}" x="{x-22}" y="{y-11}" width="44" height="22" rx="5" fill="{c['lit']}"/>
    <circle cx="{x}" cy="{y}" r="4.5" fill="{c['board']}"/>
    <text x="{x}" y="{y+40 if y > 250 else y-24}" text-anchor="{anchor}" class="lab">{label}</text>
  </g>""")
    # via grid
    dots = "".join(
        f'<circle cx="{x}" cy="{y}" r="1.4"/>' for x in range(36, W, 28) for y in range(30, H, 28)
        if not (40 < y < 200 and x < 860)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">SK Arif Hossain</title>
<desc id="d">I build the whole path: firmware on the board, the cloud in between, the app in your hand. A signal travels along a circuit trace from an ESP32 pad to Firebase to a web and Android pad.</desc>
<style>
{FONTS}
.name{{font:600 62px Chakra,'Segoe UI',sans-serif;fill:{c['text']};letter-spacing:-.5px}}
.tag{{font:400 22px Chakra,'Segoe UI',sans-serif;fill:{c['text']}}}
.meta{{font:400 17px Chakra,'Segoe UI',sans-serif;fill:{c['muted']}}}
.lab{{font:400 15px Chakra,'Segoe UI',sans-serif;fill:{c['muted']}}}
.glow{{opacity:0}}
.pulse{{stroke-dasharray:46 1000;stroke-dashoffset:1000;animation:run {dur}s linear infinite}}
@keyframes run{{0%{{stroke-dashoffset:1000}}{run*100:.0f}%,100%{{stroke-dashoffset:-46}}}}
{''.join(css_pad)}
@media (prefers-reduced-motion:reduce){{.pulse{{display:none}}.glow{{animation:none;opacity:.55}}}}
</style>
<rect width="{W}" height="{H}" rx="18" fill="{c['board']}"/>
<g fill="{c['dot']}">{dots}</g>
<text x="56" y="112" class="name">SK Arif Hossain</text>
<text x="58" y="156" class="tag">I build the whole path: firmware on the board, the cloud in between,</text>
<text x="58" y="186" class="tag">and the app in your hand.</text>
<text x="58" y="72" class="meta" dy="-24">B.Tech IT 2027, IoT intern at Maxbridge Solutions, Kolkata</text>
<path d="{d}" fill="none" stroke="{c['trace']}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>
<path class="pulse" d="{d}" pathLength="1000" fill="none" stroke="{c['signal']}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>
{''.join(glows)}
</svg>"""


# ---------------------------------------------------------------- stack matrix

COLS = ["Hardware", "Cloud", "Web", "Android", "AI"]
ROWS = [
    ("Haven", "ESP32 relay controller", {0, 1, 2, 3}),
    ("ExamSphere", "Exam-prep platform", {1, 2, 3}),
    ("Kairos", "Offline music player", {3}),
    ("CareerPilot", "Resume-to-job AI agent", {1, 2, 4}),
    ("StudyPilot", "Multi-model Chrome extension", {2, 4}),
    ("SignBridge", "Sign language prototype", {2, 4}),
]


def matrix(t):
    c = THEMES[t]
    MW, top, rh = 1200, 64, 50
    MH = top + rh * len(ROWS) + 18
    x0, cw = 560, 124
    parts = []
    for j, col in enumerate(COLS):
        parts.append(f'<text x="{x0 + j*cw}" y="40" text-anchor="middle" class="col">{col}</text>')
    for i, (name, desc, cells) in enumerate(ROWS):
        y = top + i * rh + rh / 2
        parts.append(f'<line x1="32" x2="{MW-32}" y1="{y - rh/2}" y2="{y - rh/2}" stroke="{c["dot"]}"/>')
        parts.append(f'<text x="40" y="{y+7}" class="row">{name}</text>')
        parts.append(f'<text x="220" y="{y+6}" class="desc">{desc}</text>')
        # trace linking the layers this project touches
        on = sorted(cells)
        if len(on) > 1:
            parts.append(f'<line x1="{x0+on[0]*cw}" x2="{x0+on[-1]*cw}" y1="{y}" y2="{y}" stroke="{c["trace"]}" stroke-width="4"/>')
        for j in range(len(COLS)):
            cx = x0 + j * cw
            if j in cells:
                parts.append(f'<rect x="{cx-16}" y="{y-9}" width="32" height="18" rx="4" fill="{c["pad"]}"/><circle cx="{cx}" cy="{y}" r="3.6" fill="{c["board"]}"/>')
            else:
                parts.append(f'<circle cx="{cx}" cy="{y}" r="5" fill="none" stroke="{c["ring"]}" stroke-width="1.5"/>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{MW}" height="{MH}" viewBox="0 0 {MW} {MH}" role="img" aria-labelledby="mt">
<title id="mt">Which layers each project covers: Haven covers hardware, cloud, web and Android. ExamSphere covers cloud, web and Android. Kairos is Android. CareerPilot covers cloud, web and AI. StudyPilot and SignBridge cover web and AI.</title>
<style>
{FONTS}
.col{{font:400 16px Chakra,'Segoe UI',sans-serif;fill:{c['muted']}}}
.row{{font:600 21px Chakra,'Segoe UI',sans-serif;fill:{c['text']}}}
.desc{{font:400 17px Chakra,'Segoe UI',sans-serif;fill:{c['muted']}}}
</style>
<rect width="{MW}" height="{MH}" rx="18" fill="{c['board']}"/>
{''.join(parts)}
</svg>"""


for t in THEMES:
    open(f"{OUT}/banner-{t}.svg", "w").write(banner(t))
    open(f"{OUT}/stack-{t}.svg", "w").write(matrix(t))
print("written")
