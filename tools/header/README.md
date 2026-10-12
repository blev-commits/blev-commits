# Header

The animated header at the top of the profile, `assets/header.svg`, built from the GitHub card in my Figma library (Social page).

```bash
python3 layers.py   # pre-renders the static layers into art/ (needs playwright)
python3 build.py    # writes ../../assets/header.svg
```

- `build.py` lays out the text, outlines it, and writes the SVG with its CSS animation.
- `layers.py` turns the dots, the pills' slabs and shadows, and the cursor's shadow into PNGs. GitHub shows the header as an image, which gets repainted whole on every frame, so anything static and costly is cheaper as a bitmap.
- `outline.py` turns a line of text into an SVG path, kerning included.
- `gh.py` is the GitHub mark, plus the cat cut into body and tail so the tail can wag.
- `art/` holds the glass pills exported from Figma and the layers from `layers.py`.

The fonts aren't in the repo. Set `HEADER_CLASH`, `HEADER_GEIST_MONO` and `HEADER_INTER` to your own copies of Clash Display (variable), Geist Mono and Inter.
