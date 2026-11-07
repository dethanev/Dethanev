"""Generate the Neubrutalism README SVGs (light + dark). Text is converted to paths."""
import math, os, sys
from textpath import Face, wrap

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..", "assets", "readme")
os.makedirs(OUT, exist_ok=True)

# Tokens from dethanev.app Blog src/styles/global.css
THEMES = {
    "light": dict(bg="#fff7e6", ink="#0a0a0f", paper="#ffffff", muted="#6b6b78", on="#0a0a0f",
                  pink="#ff5c8a", yellow="#fcec52", lime="#b8e14a", violet="#7b61ff", cyan="#2de2e6", blue="#58c7ff",
                  name_fg="#180b10"),
    "dark": dict(bg="#0e0e14", ink="#eee6d3", paper="#1a1a22", muted="#9a9aab", on="#0a0a0f",
                 pink="#e76f9f", yellow="#d9c34f", lime="#91bd5c", violet="#8777dc", cyan="#45b9bd", blue="#4d9fc7",
                 name_fg="#eee6d3"),
}

PROJECTS = [
    ("algolab", "AlgoLab", "演算法視覺化實驗室", "在瀏覽器裡執行 Python，逐步回放演算法的執行過程。", ["Nuxt", "Pyodide"], "algolab.dethanev.app", "yellow"),
    ("quizlab", "QuizLab", "智慧考題學習實驗室", "從考題出發理解概念的學習空間。\n純前端 PWA，資料只存在自己的裝置。", ["Nuxt", "IndexedDB"], "quizlab.dethanev.app", "lime"),
    ("driveworth", "DriveWorth", "駕值觀", "購車與養車成本評估工具，\n從買車到保養，每一分錢都算清楚。", ["Flutter", "FastAPI"], "GitHub", "cyan"),
    ("hawkguard", "HawkGuard", "反詐騙 App", "跨平台反詐騙 App，提供風險提示，\n也能回報與分享詐騙案例。", ["Flutter", "Dart"], "GitHub", "blue"),
    ("linkpet", "LinkPet", "空間運算寵物", "SwiftUI 打造的陪伴型寵物，\n結合本機語言模型、語音和 AR。", ["SwiftUI", "ARKit"], "iOS", "violet"),
    ("blog", "Blog", "dethanev.app", "開發筆記、專案紀錄、近況頁，還有做東西時踩到的坑。", ["Astro", "MDX"], "dethanev.app", "pink"),
]
BUTTONS = [("blog", "Blog", "pink"), ("algolab", "AlgoLab", "yellow"), ("quizlab", "QuizLab", "lime")]
HEADINGS = [("projects", "01", "精選專案"), ("stack", "02", "常用技術")]
STACK = ["Swift", "Dart", "Python", "TypeScript", "Java", "C",
         "Flutter", "Nuxt", "Astro", "FastAPI", "SwiftUI", "ARKit",
         "Docker", "Proxmox", "Cloudflare", "Supabase", "PostgreSQL", "Ollama"]
STACK_COLORS = ["yellow", "cyan", "pink", "lime", "blue", "violet"]
STACK_ROT = [-2, 0, 1.5, 0, -1, 0]


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:g}" height="{h:g}" viewBox="0 0 {w:g} {h:g}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n')


def box(x, y, w, h, fill, t, sw=3, shadow=6, r=4):
    """Neubrutalist box: hard shadow + fill + ink stroke (stroke kept inside the box)."""
    i = sw / 2
    s = ""
    if shadow:
        s += f'<rect x="{x+shadow:g}" y="{y+shadow:g}" width="{w:g}" height="{h:g}" rx="{r}" fill="{t["ink"]}"/>'
    s += (f'<rect x="{x+i:g}" y="{y+i:g}" width="{w-sw:g}" height="{h-sw:g}" rx="{r}" fill="{fill}" '
          f'stroke="{t["ink"]}" stroke-width="{sw}"/>')
    return s


def p(d, fill, extra=""):
    return f'<path d="{d}" fill="{fill}"{extra}/>' if d else ""


def star(cx, cy, ro, ri, n=5, rot=-90):
    pts = []
    for k in range(n * 2):
        r = ro if k % 2 == 0 else ri
        a = math.radians(rot + k * 180 / n)
        pts.append(f"{cx + r*math.cos(a):.1f},{cy + r*math.sin(a):.1f}")
    return " ".join(pts)


def write(name, theme, content):
    path = os.path.join(OUT, f"{name}-{theme}.svg")
    with open(path, "w") as f:
        f.write(content)


# ---------- banner ----------
def banner(t):
    W, H, S = 900, 230, 6
    bw, bh = W - S, H - S
    name = Face("display", 900, 78)
    s = box(0, 0, bw, bh, t["bg"], t)
    s += f'<clipPath id="c"><rect x="3" y="3" width="{bw-6}" height="{bh-6}" rx="3"/></clipPath><g clip-path="url(#c)">'
    # cyan block peeking from the bottom-right edge
    s += (f'<g transform="rotate(-14 {bw-70} {bh-8})">'
          + box(bw - 120, bh - 30, 100, 50, t["cyan"], t, sw=3, shadow=3) + '</g>')
    s += '</g>'
    # name with pink box (Blog Hero .hero-title em: pink fill, 4px ink ring, 10px hard shadow)
    tw = name.width("Dethanev", tracking=-1.5)
    padx, pt, pb = 0.15 * name.size, 0.12 * name.size, 0.08 * name.size
    cap = name.cap()
    x0, base = 48, bh / 2 + cap / 2 - 4
    top = base - cap - pt - 6
    bx, bwid, bht = x0 - padx, tw + padx * 2, cap + pt + pb + 18
    s += f'<rect x="{bx+10:.1f}" y="{top+10:.1f}" width="{bwid:.1f}" height="{bht:.1f}" fill="{t["ink"]}"/>'
    s += f'<rect x="{bx-4:.1f}" y="{top-4:.1f}" width="{bwid+8:.1f}" height="{bht+8:.1f}" fill="{t["ink"]}"/>'
    s += f'<rect x="{bx:.1f}" y="{top:.1f}" width="{bwid:.1f}" height="{bht:.1f}" fill="{t["pink"]}"/>'
    s += p(name.path("Dethanev", x0, base, tracking=-1.5), t["name_fg"])
    # yellow star sticker
    cx, cy = bw - 92, 70
    s += f'<g transform="rotate(-8 {cx} {cy})">'
    s += f'<circle cx="{cx+3}" cy="{cy+3}" r="33" fill="{t["ink"]}"/><circle cx="{cx}" cy="{cy}" r="31.5" fill="{t["yellow"]}" stroke="{t["ink"]}" stroke-width="3"/>'
    s += f'<polygon points="{star(cx, cy, 14, 6)}" fill="{t["on"]}"/></g>'
    # lime handle sticker
    tag = Face("mono", 700, 15)
    hw = tag.width("@dethanev") + 24
    hx, hy = bw - 300, bh - 70
    s += f'<g transform="rotate(5 {hx+hw/2} {hy+17})">' + box(hx, hy, hw, 36, t["lime"], t, sw=3, shadow=3)
    s += p(tag.path("@dethanev", hx + 12, hy + 23), t["on"]) + '</g>'
    return svg(W, H, s, "Dethanev")


# ---------- buttons ----------
def button(label, color, t):
    f = Face("display", 700, 15)
    tw = f.width(label)
    W, H, S = tw + 32 + 18, 44, 3
    s = box(0, 0, W - S, H - S, t[color], t, sw=2.5, shadow=S)
    base = (H - S) / 2 + f.cap() / 2
    s += p(f.path(label, 16, base), t["on"])
    ax, ay = 16 + tw + 8, base - f.cap() + 1   # arrow ↗
    a = f.cap() - 2
    s += (f'<path d="M{ax:.1f} {ay+a:.1f} L{ax+a:.1f} {ay:.1f} M{ax+2:.1f} {ay:.1f} L{ax+a:.1f} {ay:.1f} L{ax+a:.1f} {ay+a-2:.1f}" '
          f'fill="none" stroke="{t["on"]}" stroke-width="2.2" stroke-linecap="square"/>')
    return svg(W, H, s, label)


# ---------- section heading ----------
def heading(num, text, t):
    n = Face("mono", 700, 15)
    f = Face("display", 800, 17, cjk_weight=800)
    nw, tw = n.width(num), f.width(text)
    W, H, S = 14 + nw + 10 + tw + 16 + 3, 46, 3
    s = box(0, 0, W - S, H - S, t["bg"], t, sw=2.5, shadow=S)
    base = (H - S) / 2 + 6
    s += p(n.path(num, 14, base), t["muted"])
    s += p(f.path(text, 14 + nw + 10, base + 0.5), t["ink"])
    return svg(W, H, s, f"{num} {text}")


# ---------- project card ----------
def card(proj, t):
    _, name, sub, desc, chips, url, color = proj
    W, H, S = 440, 192, 6
    cw, ch = W - S, H - S
    s = box(0, 0, cw, ch, t["paper"], t)
    # header strip
    s += f'<path d="M3 7 Q3 3 7 3 L{cw-7} 3 Q{cw-3} 3 {cw-3} 7 L{cw-3} 52 L3 52 Z" fill="{t[color]}"/>'
    s += f'<rect x="1.5" y="52" width="{cw-3}" height="3" fill="{t["ink"]}"/>'
    nf = Face("display", 800, 19)
    s += p(nf.path(name, 18, 36, tracking=-0.2), t["on"])
    sf = Face("mono", 600, 12, cjk_weight=500)
    s += p(sf.path(sub, cw - 18 - sf.width(sub), 34), t["on"], ' fill-opacity="0.78"')
    # description
    df = Face("body", 400, 15, cjk_weight=400)
    mw = cw - 36 - 16          # leave room for hanging CJK punctuation
    lines = desc.split("\n") if "\n" in desc else wrap(df, desc, mw)
    while len(lines) > 1 and df.width(lines[-1]) < mw * 0.35 and mw > 200:   # avoid orphan last line
        mw -= 10
        lines = wrap(df, desc, mw)
    for k, line in enumerate(lines[:2]):
        s += p(df.path(line, 18, 86 + k * 24), t["ink"])
    # chips + url
    cf = Face("mono", 600, 12)
    x, y = 18, ch - 44
    for c in chips:
        w = cf.width(c) + 20
        s += f'<rect x="{x+1:g}" y="{y+1:g}" width="{w-2:g}" height="24" rx="12" fill="{t["bg"]}" stroke="{t["ink"]}" stroke-width="2"/>'
        s += p(cf.path(c, x + 10, y + 17), t["ink"])
        x += w + 8
    s += p(cf.path(url, cw - 18 - cf.width(url), y + 17), t["muted"])
    return svg(W, H, s, f"{name}：" + desc.replace("\n", ""))


# ---------- stack stickers ----------
def stack(t):
    W, S = 900, 6
    f = Face("mono", 700, 14)
    pad, gap, rowh = 24, 12, 44
    x, y, items = pad, pad, []
    for k, label in enumerate(STACK):
        w = f.width(label) + 22
        if x + w > W - S - pad:
            x, y = pad, y + rowh
        items.append((k, label, x, y, w)); x += w + gap
    H = y + rowh + pad - 10 + S
    s = box(0, 0, W - S, H - S, t["bg"], t)
    for k, label, x, y, w in items:
        c, r = STACK_COLORS[k % 6], STACK_ROT[k % 6]
        s += f'<g transform="rotate({r} {x+w/2:.1f} {y+15})">' + box(x, y, w, 32, t[c], t, sw=2, shadow=2)
        s += p(f.path(label, x + 11, y + 21), t["on"]) + '</g>'
    return svg(W, H, s, "常用技術：" + "、".join(STACK))


for th, t in THEMES.items():
    write("banner", th, banner(t))
    for key, label, color in BUTTONS:
        write(f"btn-{key}", th, button(label, color, t))
    for key, num, text in HEADINGS:
        write(f"h-{key}", th, heading(num, text, t))
    for proj in PROJECTS:
        write(f"card-{proj[0]}", th, card(proj, t))
    write("stack", th, stack(t))
print("done", len(os.listdir(OUT)), "files")
