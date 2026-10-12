"""Pre-render the header's static layers as PNGs, so the SVG has nothing to
redraw from scratch on every frame.

GitHub shows the header as an image, and an animated SVG image is repainted
whole on every frame. Anything static but expensive (about 1,300 dots, the
pills' blurred shadows, the cursor's blurred shadow) is cheaper as a bitmap.

Writes, next to this file:
  art/ground-dark.png, art/ground-light.png   dots, plus the slab and shadow
                                              under each pill (1200x630 @2x)
  art/cursor-shadow.png                       the cursor and Blev tag's shadow

Run it before build.py whenever the pills or the cursor move.
Needs playwright with Chromium.
"""
import asyncio, os
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, 'art')
CURSOR = ('M18.3252 25.877L13.579 11.4732C13.1883 10.2877 14.3321 9.17152 15.5077 9.591L30.1147 14.8031'
          'C31.445 15.2778 31.4417 17.1604 30.1096 17.6304L24.652 19.5558C24.2736 19.6894 23.9644 19.969 '
          '23.7937 20.3321L21.1072 26.0458C20.5301 27.2733 18.7496 27.1652 18.3252 25.877Z')
# Each pill: x, y, width. Height 56, fully rounded.
PILLS = ((870, 68, 262), (806, 504, 326))
# Where the cursor shadow image sits in the header's coordinates.
SHADOW_BOX = (740, 404, 120, 82)


def ground(theme):
    dot = '#fff' if theme == 'dark' else '#0e0f10'
    slab = '#0e0f10' if theme == 'dark' else '#fff'
    slabs = ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="56" rx="28" fill="{slab}" filter="url(#shadow)"/>'
                    for x, y, w in PILLS)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  <defs>
    <pattern id="dots" x="16" y="16" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="1.2" cy="1.2" r="1.2" fill="{dot}" fill-opacity=".05"/></pattern>
    <filter id="shadow" x="-20%" y="-60%" width="140%" height="220%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000" flood-opacity=".25"/></filter>
  </defs>
  <rect width="1200" height="630" fill="url(#dots)"/>
  {slabs}
</svg>'''


def cursor_shadow():
    x, y, w, h = SHADOW_BOX
    # Only the shadow: the alpha blurred, offset and tinted, without the shape.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" width="{w}" height="{h}">
  <defs><filter id="s" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur in="SourceAlpha" stdDeviation="6"/><feOffset dy="4" result="b"/>
    <feFlood flood-color="#000" flood-opacity=".15"/><feComposite in2="b" operator="in"/></filter></defs>
  <g filter="url(#s)">
    <path transform="translate(755.94 424.24)" d="{CURSOR}"/>
    <rect x="790" y="439" width="48" height="22" rx="8"/>
  </g>
</svg>'''


async def render(svg, out, w, h):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2)
        await pg.set_content(f'<html><body style="margin:0;background:transparent">{svg}</body></html>')
        await pg.screenshot(path=out, omit_background=True, clip={'x': 0, 'y': 0, 'width': w, 'height': h})
        await b.close()


async def main():
    os.makedirs(ART, exist_ok=True)
    for theme in ('dark', 'light'):
        await render(ground(theme), os.path.join(ART, f'ground-{theme}.png'), 1200, 630)
    _, _, w, h = SHADOW_BOX
    await render(cursor_shadow(), os.path.join(ART, 'cursor-shadow.png'), w, h)
    for f in sorted(os.listdir(ART)):
        print(f, os.path.getsize(os.path.join(ART, f)))

if __name__ == '__main__':
    asyncio.run(main())
