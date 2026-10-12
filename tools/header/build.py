"""Build assets/header.svg, the animated profile header.

    python3 layers.py   # once, or whenever the pills or the cursor move
    python3 build.py    # writes ../../assets/header.svg

Text is outlined from the fonts, so none ship with the SVG. The fonts are
not in this repo (Clash Display's license doesn't allow it); point these at
your copies with HEADER_CLASH, HEADER_GEIST_MONO and HEADER_INTER.
"""
import base64, os, sys
from outline import Face
HERE=os.path.dirname(os.path.abspath(__file__))
def art(name):
    return base64.b64encode(open(os.path.join(HERE,'art',name),'rb').read()).decode()
CL=Face(os.environ.get('HEADER_CLASH','/home/claude/portfolio/assets/fonts/ClashDisplay-Variable.woff'),600)
GM=Face(os.environ.get('HEADER_GEIST_MONO','/mnt/skills/examples/canvas-design/canvas-fonts/GeistMono-Regular.ttf'))
IN=Face(os.environ.get('HEADER_INTER','/usr/share/fonts/opentype/inter/Inter-Regular.otf'))
def r(d):
    import re; return re.sub(r'-?\d+\.\d+', lambda m: ('%.1f'%float(m.group())).rstrip('0').rstrip('.'), d)
T=lambda f,t,s,x,y,lh=None: r(f.path(t,s,x,y,lh)[0])
NINJA=['M362.723 24.0911C471.15 6.91786 575.27 49.163 641.921 126.732C661.698 112.064 681.373 101.529 699.594 90.7209C719.493 78.9177 739.019 66.0804 759.477 45.6034C781.466 23.5937 793.881 7.89819 809.013 -8.05729C823.482 -23.3149 838.114 -36.003 859.717 -45.8588C867.283 -49.3107 876.216 -45.9757 879.668 -38.4096C883.119 -30.8436 879.783 -21.9123 872.217 -18.4604C855.406 -10.7906 843.848 -1.02246 830.865 12.667C818.545 25.6587 802.248 45.4026 780.783 66.888C757.787 89.9059 735.849 104.232 714.959 116.624C695.552 128.135 678.145 137.414 660.397 150.522C661.8 152.526 663.181 154.548 664.537 156.589C690.315 156.278 714.822 160.028 738.16 163.818C762.548 167.779 785.541 171.755 809.544 172.302C834.183 172.863 848.274 169.167 867.482 167.799C886.363 166.455 904.601 168.472 927.792 181.912C934.988 186.082 937.44 195.296 933.27 202.491C929.1 209.686 919.887 212.138 912.691 207.968C895.57 198.046 883.55 196.846 869.621 197.838C856.018 198.807 834.745 203 808.859 202.41C782.338 201.806 757.093 197.404 733.332 193.545C715.913 190.716 699.186 188.156 682.366 187.144C696.434 214.858 706.471 245.21 711.595 277.562C737.94 443.894 624.457 600.09 458.125 626.434C291.792 652.779 135.597 539.296 109.252 372.964C82.908 206.631 196.391 50.4358 362.723 24.0911ZM367.434 53.8375C217.53 77.5803 115.256 218.348 138.999 368.252C162.741 518.157 303.509 620.432 453.414 596.69C603.318 572.947 705.594 432.178 681.851 282.273C658.108 132.368 517.339 30.0949 367.434 53.8375ZM520.342 176.994C576.47 168.105 629.178 206.4 638.068 262.528C646.958 318.657 608.663 371.365 552.535 380.255L292.263 421.478C236.134 430.367 183.426 392.073 174.536 335.945C165.646 279.816 203.941 227.107 260.069 218.217L520.342 176.994ZM264.781 247.963C225.08 254.251 197.994 291.533 204.282 331.233C210.57 370.934 247.851 398.02 287.551 391.732L547.824 350.509C587.524 344.221 614.61 306.94 608.323 267.24C602.035 227.539 564.753 200.452 525.053 206.74L264.781 247.963Z',
'M341.22 345.77C360.738 342.679 374.054 324.351 370.963 304.833C367.871 285.316 349.543 272 330.026 275.091C310.509 278.182 297.192 296.51 300.284 316.028C303.375 335.545 321.703 348.861 341.22 345.77Z',
'M482.578 323.381C502.096 320.29 515.412 301.962 512.32 282.445C509.229 262.927 490.901 249.611 471.384 252.702C451.866 255.794 438.55 274.122 441.641 293.639C444.733 313.156 463.061 326.473 482.578 323.381Z']
OHIO='M4.4 5.33L11.73 5.07L13.07 5.87L14.53 6.67L15.87 6.93L16.67 7.47L18.67 6.93L21.33 6.8L23.6 4.93L26.27 3.87L27.73 3.33V12.93L27.2 14.8L26.53 16.93L25.73 19.07L24 21.33L22 22.67L21.07 23.2L19.47 24.67L18.53 25.87L17.2 28.4L16.4 28.67L16 27.87L14.27 26.4L12.53 27.2H10.53L9.6 26.4L7.6 26L6 23.87H4.27L4.4 5.33Z'
LOGO='M25 7V8.71L10.86 22.86H22.86V15.57H21.14L25 11.71V25H7V23.71L15.14 15.57H9.14V18.14L7 20.29V7H25ZM9.14 9.14V13.43H17.29L21.57 9.14H9.14Z'
CURSOR='M18.3252 25.877L13.579 11.4732C13.1883 10.2877 14.3321 9.17152 15.5077 9.591L30.1147 14.8031C31.445 15.2778 31.4417 17.1604 30.1096 17.6304L24.652 19.5558C24.2736 19.6894 23.9644 19.969 23.7937 20.3321L21.1072 26.0458C20.5301 27.2733 18.7496 27.1652 18.3252 25.877Z'

PILL=art('pill-dark.png'); PILLL=art('pill-light.png')
GHD=art('gh-dark.png'); GHL=art('gh-light.png')
# Static layers from layers.py: dots and the pills' slabs and shadows, and the
# cursor's shadow. Bitmaps, so a frame never re-blurs or redraws them.
GROUNDD=art('ground-dark.png'); GROUNDL=art('ground-light.png'); CSHADOW=art('cursor-shadow.png')
from gh import GH, CAT, TAIL, BODY
NJ_TAIL='M24.8001 12.2666L29.6668 9.33329M25.4668 14.1333L30.3334 15.1999'
NJ_HEAD='M25.6667 16.6666C25.6667 22.7418 20.7419 27.6666 14.6667 27.6666C8.59162 27.6666 3.66675 22.7418 3.66675 16.6666C3.66675 10.5915 8.59162 5.66663 14.6667 5.66663C20.7419 5.66663 25.6667 10.5915 25.6667 16.6666ZM9.66675 12.3333H19.6667C21.5077 12.3333 23.0001 13.8257 23.0001 15.6666C23.0001 17.5076 21.5077 19 19.6667 19H9.66675C7.8258 19 6.33341 17.5076 6.33341 15.6666C6.33341 13.8257 7.8258 12.3333 9.66675 12.3333Z'
STEP=.05
def typed(text, x, top, start, cls, caret_cls, hl=None):
    gl=CL.glyphs(text,64,x,top,72); parts=[]; carets=[]; segs=[]
    for i,(ch,d,x0,x1) in enumerate(gl):
        t=start+i*STEP
        if d: parts.append(f'<path class="{cls} g" style="animation-delay:{t:.2f}s" d="{r(d)}"/>')
        carets.append(f'<rect class="k {caret_cls} kb" style="animation-delay:{t:.2f}s" x="{x1:.1f}" y="{top+8}" width="4" height="56"/>')
        if hl:
            a=hl[0] if i==0 else x0-1; b=hl[1] if i==len(gl)-1 else x1+1
            rx=' rx="4"' if i in (0,len(gl)-1) else ''
            if i==0: b=x1+1
            segs.append(f'<rect class="lime g" style="animation-delay:{t:.2f}s" x="{a:.1f}" y="{top}" width="{b-a:.1f}" height="72"{rx}/>')
    return '\n  '.join(segs+parts), '\n  '.join(carets), start+len(gl)*STEP, gl[-1][3]
L1,K1,e1,_=typed('Graphic design. UX/UI.',86,179,.5,'t1','k1')
L2,K2,e2,_=typed('Product. And yes,',86,250,e1+.1,'t1','k2')
L3,K3,e3,end3=typed('I ship code too.',96,321,e2+.1,'ink','k3',hl=(86,563))
eyebrow=T(GM,'Product Designer + Design Engineer',20,64,135,34)
l1=T(CL,'Graphic design. UX/UI.',64,86,179,72); l2=T(CL,'Product. And yes,',64,86,250,72); l3=T(CL,'I ship code too.',64,96,321,72)
size=T(GM,'625 × 138',11.78,420,415,16.3); blev=T(GM,'Blev',13,798,441,18)
loc=T(GM,'Columbus, Ohio',20,110,528,34); url=T(IN,'zachblevins.com',22,894,519,27)

svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630" role="img" aria-label="Zach Blevins, Product Designer + Design Engineer in Columbus, Ohio. Graphic design. UX/UI. Product. And yes, I ship code too.">
  <!-- Built from the GitHub card in the Figma library (Social page). Text is set in Clash Display, Geist Mono and Inter, then outlined, so no fonts ship with it. -->
  <defs>
    <linearGradient id="rim" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#d7ff38"/><stop offset=".35" stop-color="#38e1ff"/><stop offset=".65" stop-color="#ff4fd8"/><stop offset="1" stop-color="#ffb238"/>
    </linearGradient>
  </defs>
  <style>
    .bg{{fill:#0e0f10}} .ninja{{fill:#fff;fill-opacity:.05}}
    .nj{{fill:none;stroke:#d7ff38;stroke-width:2.67;stroke-linecap:round;stroke-linejoin:round}} .nje{{fill:#d7ff38}} .ghrim{{fill:none;stroke:none}}
    .t1{{fill:#fff}} .t3{{fill:#fff;fill-opacity:.5}} .ink{{fill:#0e0f10}} .lime{{fill:#d7ff38}}
    .eb{{animation:fadein .3s .2s both}}
    .g{{animation:on .01s both}} @keyframes on{{from{{opacity:0}}to{{opacity:1}}}}
    .k{{fill:#d7ff38;opacity:0}} .k3,.kend{{fill:#0e0f10}}
    .kb{{animation:blip .05s}} @keyframes blip{{from,to{{opacity:1}}}}
    .kend{{animation:endblink 1.6s}} @keyframes endblink{{0%,30%,60%{{opacity:1}}15%,45%,75%,100%{{opacity:0}}}}
    .sel{{fill:#fff;fill-opacity:.3}} .box{{animation:fadein .2s .4s both}}
    .side{{transform-box:view-box;transform-origin:0 181px;animation:grows 2.5s .4s both}}
    .low{{animation:growl 2.5s .4s both}}
    .handle{{fill:#0e0f10;stroke:#d7ff38;stroke-width:2}}
    @keyframes grows{{0%,52%{{transform:scaleY(.339)}}58%,90%{{transform:scaleY(.656)}}96%,100%{{transform:scaleY(1)}}}}
    @keyframes growl{{0%,52%{{transform:translateY(-148px)}}58%,90%{{transform:translateY(-77px)}}96%,100%{{transform:translateY(0)}}}}
    .tag{{fill:#2b2c2d}} .size{{animation:fadein .3s 3.6s both}}
    .cursor{{animation:glide 1.3s 3.4s cubic-bezier(.3,.7,.2,1) both}}
    .cur{{fill:#0e0f10;stroke:#fff;stroke-opacity:.95;stroke-linejoin:round}} .btag{{fill:#d7ff38;fill-opacity:.92}}
    /* after it lands, the cursor wanders: it glides to a spot, rests there for a few seconds, then moves on.
       Both axes share one clock so every move starts and stops cleanly; a different ease on each axis bends the path a little.
       While it rests, two slow sine-like loops on different clocks keep a hand's worth of drift in it. */
    .wx{{animation:wx 36s 5s infinite;animation-timing-function:cubic-bezier(.5,0,.3,1)}}
    .wy{{animation:wy 36s 5s infinite;animation-timing-function:cubic-bezier(.3,0,.5,1)}}
    .wmx{{animation:wmx 2.9s 5s ease-in-out infinite alternate}} .wmy{{animation:wmy 3.7s 5s ease-in-out infinite alternate}}
    @keyframes wx{{0%,10%{{transform:translateX(0px)}}14.5%,26%{{transform:translateX(-180px)}}30.5%,42%{{transform:translateX(-430px)}}46.5%,58%{{transform:translateX(-115px)}}63%,75%{{transform:translateX(212px)}}79.5%,90%{{transform:translateX(60px)}}94.5%,100%{{transform:translateX(0px)}}}}
    @keyframes wy{{0%,10%{{transform:translateY(0px)}}14.5%,26%{{transform:translateY(-150px)}}30.5%,42%{{transform:translateY(-58px)}}46.5%,58%{{transform:translateY(95px)}}63%,75%{{transform:translateY(-228px)}}79.5%,90%{{transform:translateY(40px)}}94.5%,100%{{transform:translateY(0px)}}}}
    @keyframes wmx{{from{{transform:translateX(-3px)}}to{{transform:translateX(3px)}}}}
    @keyframes wmy{{from{{transform:translateY(-2.5px)}}to{{transform:translateY(2.5px)}}}}
    .drift{{animation:drift 9s ease-in-out infinite;transform-box:view-box;transform-origin:848px 323px}}
    /* the tail wags in short bursts around the hip, on its own clock */
    .tail{{animation:wag 6s 2s infinite;transform-box:view-box;transform-origin:772px 524px}}
    @keyframes wag{{0%,52%,100%{{transform:rotate(0)}}60%{{transform:rotate(7deg)}}68%{{transform:rotate(-4deg)}}76%{{transform:rotate(6deg)}}84%{{transform:rotate(-2deg)}}92%{{transform:rotate(1deg)}}}}
    .njin{{animation:fadein .3s .5s both}}
    .njtail{{animation:sway 3.2s 1s ease-in-out infinite;transform-box:view-box;transform-origin:24.8px 13.5px}}
    @keyframes sway{{0%,100%{{transform:rotate(0)}}25%{{transform:rotate(-14deg)}}60%{{transform:rotate(9deg)}}}}
    .njeye{{transform-box:fill-box;transform-origin:center;animation:blink 4.2s 1.8s infinite}}
    .eye{{transform-box:fill-box;transform-origin:center;animation:blink 5s 1.5s infinite}}
    .ohio{{fill:none;stroke:#d7ff38;stroke-width:2.67;stroke-linecap:round;stroke-linejoin:round}}
    .slabtint{{fill:#fff;fill-opacity:.06}} .pill-l{{display:none}}
    .glass{{fill:#fff;fill-opacity:.035}} .gsheen{{fill:url(#sheen)}}
    .refl{{fill:#fff;opacity:.55}} .rr{{fill:#ff4f6e}} .rc{{fill:#3fe7ff}} .fringe{{opacity:.45;mix-blend-mode:screen}}
    .bev{{fill:none;stroke:#000;stroke-opacity:.55;stroke-width:3}}
    .rim{{fill:none;stroke:#fff;stroke-opacity:.9;stroke-width:1.4}} .rimc{{fill:none;stroke:url(#ends);stroke-width:1.6;opacity:.35}}
    .logo{{fill:#fff;fill-opacity:.8}}
    @keyframes draw{{to{{stroke-dashoffset:0}}}} @keyframes fade{{to{{opacity:1}}}} @keyframes wipe{{to{{transform:scaleX(1)}}}}
    @keyframes glide{{from{{transform:translate(380px,160px);opacity:0}}to{{transform:translate(0,0);opacity:1}}}} @keyframes fadein{{from{{opacity:0}}}}
    @keyframes drift{{0%,100%{{transform:translate(0,0) rotate(0)}}50%{{transform:translate(-10px,8px) rotate(-1.5deg)}}}}
    @keyframes blink{{0%,90%,100%{{transform:scaleY(1)}}93%,95%{{transform:scaleY(.08)}}}}
    @media (prefers-color-scheme: light){{
      .bg{{fill:#fff}}  .ninja{{fill:#0e0f10;fill-opacity:.05}}
      .t1{{fill:#0e0f10}} .t3{{fill:#0e0f10;fill-opacity:.6}}
      .sel{{fill:#0e0f10}} .handle{{fill:#d7ff38;stroke:#0e0f10}} .tag{{fill:#ececec}} .k1,.k2{{fill:#0e0f10}}
      .cur{{fill:#0e0f10;stroke:#fff}} .ohio{{stroke:#0e0f10}} .nj{{stroke:#0e0f10}} .nje{{fill:#0e0f10}} .ghrim{{stroke:#0e0f10;stroke-opacity:.12;stroke-width:1}} .slabtint{{fill:#0e0f10;fill-opacity:.04}} .pill-d{{display:none}} .pill-l{{display:inline}} .glass{{fill:#0e0f10;fill-opacity:.02}} .refl{{fill:#0e0f10;opacity:.4}} .fringe{{mix-blend-mode:multiply;opacity:.35}} .bev{{stroke:#fff;stroke-opacity:.9}} .rim{{stroke:#0e0f10;stroke-opacity:.25}} .logo{{fill:#0e0f10}}
    }}
    @media (prefers-reduced-motion: reduce){{
      *{{animation:none!important}}
    }}
  </style>

  <rect class="bg" width="1200" height="630"/>
  <!-- the GitHub mark, drifting. The cat is the negative space, so it is drawn as its own shape in two pieces, body and tail, and the tail wags. No clip paths, so WebKit cannot misplace anything. -->
  <g class="drift"><g transform="translate(536 3)">
    <circle class="ninja" cx="312" cy="319.7" r="311.9"/>
    <path class="bg" d="{BODY}"/>
  </g><g class="tail"><g transform="translate(536 3)">
    <path class="bg" d="{TAIL}"/>
  </g></g></g>
  <!-- dots, and the slab and shadow under each pill, pre-rendered by layers.py -->
  <image class="pill-d" href="data:image/png;base64,{GROUNDD}" width="1200" height="630"/>
  <image class="pill-l" href="data:image/png;base64,{GROUNDL}" width="1200" height="630"/>

  <!-- eyebrow and headline, in a Figma selection -->
  <path class="t3 eb" d="{eyebrow}"/>
  <g class="njin" transform="translate(480 136)">
    <g class="njtail"><path class="nj" d="{NJ_TAIL}"/></g>
    <path class="nj" d="{NJ_HEAD}"/>
    <circle class="nje njeye" cx="11.4667" cy="15.6667" r="1.6"/><circle class="nje njeye" cx="17.8667" cy="15.6667" r="1.6"/>
  </g>
  {L1}
  {L2}
  {L3}
  <!-- the caret steps along with each letter, then blinks at the end -->
  {K1}
  {K2}
  {K3}
  <rect class="k kend" x="{end3:.1f}" y="329" width="4" height="56" style="animation-delay:{e3:.2f}s"/>
  <!-- the selection grows a line at a time as the headline types -->
  <g class="box">
    <rect class="sel" x="68" y="180" width="739" height="2"/>
    <g class="side"><rect class="sel" x="68" y="180" width="2" height="226"/><rect class="sel" x="805" y="180" width="2" height="226"/></g>
    <g class="low"><rect class="sel" x="68" y="404" width="739" height="2"/><g class="handle"><rect x="65" y="399" width="10" height="10"/><rect x="800" y="399" width="10" height="10"/></g></g>
    <g class="handle"><rect x="65" y="178" width="10" height="10"/><rect x="800" y="178" width="10" height="10"/></g>
  </g>
  <g class="size"><rect class="tag" x="412" y="413" width="78" height="20" rx="5"/><path class="t1" d="{size}"/></g>

  <!-- location and site -->
  <path class="ohio" transform="translate(64 529)" d="{OHIO}"/>
  <path class="t3" d="{loc}"/>
  <!-- the pills, on the slabs drawn into the ground layer -->
  <rect x="870" y="68" width="262" height="56" rx="28" class="slabtint"/>
  <image class="pill-d" href="data:image/png;base64,{PILL}" x="870" y="68" width="262" height="56"/>
  <image class="pill-l" href="data:image/png;base64,{PILLL}" x="870" y="68" width="262" height="56"/>
  <rect x="806" y="504" width="326" height="56" rx="28" class="slabtint"/>
  <image class="pill-d" href="data:image/png;base64,{GHD}" x="806" y="504" width="326" height="56"/>
  <image class="pill-l" href="data:image/png;base64,{GHL}" x="806" y="504" width="326" height="56"/>
  <path class="ghrim" d="M1100 504.5H1104A27.5 27.5 0 0 1 1104 559.5H1100"/>
  <!-- multiplayer cursor -->
  <g class="cursor"><g class="wx"><g class="wy"><g class="wmx"><g class="wmy">
    <image href="data:image/png;base64,{CSHADOW}" x="740" y="404" width="120" height="82"/>
    <path class="cur" transform="translate(755.94 424.24)" d="{CURSOR}"/>
    <rect class="btag" x="790" y="439" width="48" height="22" rx="8"/><path class="ink" d="{blev}"/>
  </g></g></g></g></g>
</svg>
'''
out=sys.argv[1] if len(sys.argv)>1 else os.path.join(HERE,'..','..','assets','header.svg')
open(out,'w').write(svg); print(out, len(svg))
