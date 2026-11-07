"""Text -> SVG path helpers (fontTools). Fonts are instanced once per weight and cached."""
import functools, os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

# Font sources: Blog's @fontsource-variable packages + Noto Sans TC (OFL). Override with env vars.
FS = os.environ.get("FONTSOURCE_DIR", os.path.expanduser("~/Web/Blog/node_modules/@fontsource-variable"))
NOTO = os.environ.get("NOTO_SANS_TC", os.path.expanduser("~/Library/Fonts/NotoSansTC[wght].ttf"))
FILES = {
    "display": f"{FS}/unbounded/files/unbounded-latin-wght-normal.woff2",
    "body": f"{FS}/bricolage-grotesque/files/bricolage-grotesque-latin-wght-normal.woff2",
    "mono": f"{FS}/jetbrains-mono/files/jetbrains-mono-latin-wght-normal.woff2",
    "cjk": NOTO,
}


@functools.lru_cache(maxsize=None)
def font(family, weight):
    f = TTFont(FILES[family])
    if "fvar" in f:
        axes = {a.axisTag: a for a in f["fvar"].axes}
        w = max(axes["wght"].minValue, min(axes["wght"].maxValue, weight))
        loc = {"wght": w}
        for tag, a in axes.items():
            if tag != "wght":
                loc[tag] = a.defaultValue
        f = instancer.instantiateVariableFont(f, loc)
    return f


class Face:
    """A primary font with CJK fallback."""

    def __init__(self, family, weight, size, cjk_weight=None):
        self.p = font(family, weight)
        self.c = font("cjk", cjk_weight or weight)
        self.size = size

    def _pick(self, ch):
        for f in (self.p, self.c):
            if ord(ch) in f.getBestCmap():
                return f
        return self.c

    def advance(self, ch):
        f = self._pick(ch)
        g = f.getBestCmap().get(ord(ch))
        if g is None:
            return self.size * 0.5
        return f["hmtx"][g][0] * self.size / f["head"].unitsPerEm

    def width(self, text, tracking=0):
        return sum(self.advance(ch) + tracking for ch in text) - (tracking if text else 0)

    def path(self, text, x, y, tracking=0):
        """Return path data for text with baseline at y."""
        out = []
        for ch in text:
            f = self._pick(ch)
            cmap = f.getBestCmap()
            g = cmap.get(ord(ch))
            s = self.size / f["head"].unitsPerEm
            if g is not None:
                pen = SVGPathPen(f.getGlyphSet(), ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
                f.getGlyphSet()[g].draw(TransformPen(pen, (s, 0, 0, -s, x, y)))
                out.append(pen.getCommands())
                x += f["hmtx"][g][0] * s
            else:
                x += self.size * 0.5
            x += tracking
        return " ".join(c for c in out if c)

    def cap(self):
        """Approximate cap height in px (for vertical centering)."""
        os2 = self.p["OS/2"]
        h = getattr(os2, "sCapHeight", 0) or self.p["head"].unitsPerEm * 0.7
        return h * self.size / self.p["head"].unitsPerEm


def wrap(face, text, max_w):
    """Greedy wrap: latin words stay together, CJK breaks per character."""
    tokens, buf = [], ""
    for ch in text:
        if ord(ch) < 0x2E80 and not ch.isspace():
            buf += ch
        else:
            if buf:
                tokens.append(buf); buf = ""
            tokens.append(ch)
    if buf:
        tokens.append(buf)
    lines, cur = [], ""
    for t in tokens:
        if face.width(cur + t) <= max_w or not cur or t in "，。、；：！？）":
            cur += t
        else:
            lines.append(cur.rstrip()); cur = t.lstrip()
    if cur:
        lines.append(cur.rstrip())
    return lines
