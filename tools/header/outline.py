"""Lay out a line of text with a font's advances and GPOS pair kerning, return an SVG path."""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.varLib import instancer

class Face:
    def __init__(self, path, wght=None):
        f = TTFont(path)
        if wght is not None and 'fvar' in f:
            f = instancer.instantiateVariableFont(f, {'wght': wght})
        self.f = f; self.upm = f['head'].unitsPerEm
        self.cmap = f.getBestCmap(); self.gs = f.getGlyphSet(); self.hmtx = f['hmtx']
        self.asc = f['hhea'].ascent; self.desc = f['hhea'].descent
        self.kern = self._pairs()
    def _pairs(self):
        kern = {}
        if 'GPOS' not in self.f: return kern
        gpos = self.f['GPOS'].table
        if not gpos.LookupList: return kern
        feats = [fr.Feature for fr in gpos.FeatureList.FeatureRecord if fr.FeatureTag == 'kern']
        idx = sorted({i for ft in feats for i in ft.LookupListIndex})
        for li in idx:
            lk = gpos.LookupList.Lookup[li]
            for st in lk.SubTable:
                if lk.LookupType == 9: st = st.ExtSubTable
                if getattr(st, 'LookupType', 2) != 2 and lk.LookupType not in (2, 9): continue
                if not hasattr(st, 'Format'): continue
                cov = st.Coverage.glyphs
                if st.Format == 1:
                    for i, g1 in enumerate(cov):
                        for pvr in st.PairSet[i].PairValueRecord:
                            v = pvr.Value1; x = getattr(v, 'XAdvance', 0) if v else 0
                            if x: kern.setdefault((g1, pvr.SecondGlyph), x)
                elif st.Format == 2:
                    c1 = st.ClassDef1.classDefs; c2 = st.ClassDef2.classDefs
                    self._cls = getattr(self, '_cls', [])
                    self._cls.append((set(cov), c1, c2, st.Class1Record))
        return kern
    def pair(self, a, b):
        if (a, b) in self.kern: return self.kern[(a, b)]
        for cov, c1, c2, recs in getattr(self, '_cls', []):
            if a in cov:
                r = recs[c1.get(a, 0)].Class2Record[c2.get(b, 0)]
                v = r.Value1; x = getattr(v, 'XAdvance', 0) if v else 0
                if x: return x
        return 0
    def glyphs(self, text, size, x, top, line_h=None):
        """One path per character: (char, d, x_start, x_end)."""
        s = size / self.upm
        content = (self.asc - self.desc) * s
        lh = line_h if line_h is not None else content
        base = top + (lh - content) / 2 + self.asc * s
        names = [self.cmap.get(ord(c), '.notdef') for c in text]
        out = []; pen_x = x
        for i, g in enumerate(names):
            sp = SVGPathPen(self.gs)
            self.gs[g].draw(TransformPen(sp, (s, 0, 0, -s, pen_x, base)))
            adv = self.hmtx[g][0]
            if i + 1 < len(names): adv += self.pair(g, names[i + 1])
            out.append((text[i], sp.getCommands(), pen_x, pen_x + adv * s))
            pen_x += adv * s
        return out
    def path(self, text, size, x, top, line_h=None):
        s = size / self.upm
        content = (self.asc - self.desc) * s
        lh = line_h if line_h is not None else content
        base = top + (lh - content) / 2 + self.asc * s
        names = [self.cmap.get(ord(c), '.notdef') for c in text]
        out = []; pen_x = x
        for i, g in enumerate(names):
            sp = SVGPathPen(self.gs)
            tp = TransformPen(sp, (s, 0, 0, -s, pen_x, base))
            self.gs[g].draw(tp)
            d = sp.getCommands()
            if d: out.append(d)
            adv = self.hmtx[g][0]
            if i + 1 < len(names): adv += self.pair(g, names[i + 1])
            pen_x += adv * s
        return ' '.join(out), pen_x - x
