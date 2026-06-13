#!/usr/bin/env python3
"""
Generator for problem_7-17.html - a self-contained worked solution with both
mechanisms (SN1 and E1) drawn as inline SVG.

Problem 7-17 (Wade): Solvolysis of 2-bromo-2,3,3-trimethylbutane in methanol.
"""
import os, html

OUT = os.path.join(os.path.dirname(__file__), "problem_7-17.html")

# ---------------------------------------------------------------------------
# SVG primitives
# ---------------------------------------------------------------------------
DEFS = '''<defs>
  <marker id="arr-red" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="9" markerHeight="9" orient="auto">
    <path d="M0,0 L10,5 L0,10 z" fill="#e23636"/></marker>
  <marker id="arr-blk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="9" markerHeight="9" orient="auto">
    <path d="M0,0 L10,5 L0,10 z" fill="#1a1a1a"/></marker>
  <marker id="arr-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="9" markerHeight="9" orient="auto">
    <path d="M0,0 L10,5 L0,10 z" fill="#1f6feb"/></marker>
</defs>'''

def molecule_skeleton(ox, oy, sub2_above="CH<tspan baseline-shift='sub' font-size='13'>3</tspan>",
                     sub2_below="Br", sub3_above="CH<tspan baseline-shift='sub' font-size='13'>3</tspan>",
                     sub3_below="CH<tspan baseline-shift='sub' font-size='13'>3</tspan>",
                     c2_label="C", c2_super="", sub2_below_color="#1a1a1a",
                     show_c2_below_bond=True, c2_below_dy=70, sub2_above_extra="",
                     sub2_above_double=False, sub2_above_dy=70):
    """Draws the 4-carbon chain (CH3)-C-C-(CH3) with up/down substituents on C2 and C3.

    Coordinate frame (local, then translated by ox/oy):
      C1 = (40, 140)    main chain CH3 left
      C2 = (140, 140)   central left carbon
      C3 = (260, 140)   central right carbon
      C4 = (360, 140)   main chain CH3 right
      sub2_above at (140, 60); sub2_below at (140, 220)
      sub3_above at (260, 60); sub3_below at (260, 220)
    """
    parts = [f'<g transform="translate({ox},{oy})">']
    # ----- atom labels -----
    parts.append('<g font-family="Arial, sans-serif" font-size="20" fill="#1a1a1a" '
                 'text-anchor="middle">')
    parts.append('<text x="40" y="146">CH<tspan baseline-shift="sub" font-size="13">3</tspan></text>')
    sup = f'<tspan baseline-shift="super" font-size="15" fill="#1f6feb" font-weight="bold">{c2_super}</tspan>' if c2_super else ""
    parts.append(f'<text x="140" y="146" font-weight="bold">{c2_label}{sup}</text>')
    parts.append(f'<text x="260" y="146" font-weight="bold">C</text>')
    parts.append('<text x="360" y="146">CH<tspan baseline-shift="sub" font-size="13">3</tspan></text>')

    # substituent labels
    if sub2_above:
        parts.append(f'<text x="140" y="{146-sub2_above_dy}" fill="#1a1a1a">{sub2_above}</text>')
    if sub2_above_extra:
        parts.append(sub2_above_extra)
    if sub2_below:
        parts.append(f'<text x="140" y="{146+c2_below_dy}" fill="{sub2_below_color}" font-weight="bold">{sub2_below}</text>')
    if sub3_above:
        parts.append(f'<text x="260" y="76">{sub3_above}</text>')
    if sub3_below:
        parts.append(f'<text x="260" y="216">{sub3_below}</text>')
    parts.append('</g>')

    # ----- bonds -----
    parts.append('<g stroke="#1a1a1a" stroke-width="2" fill="none">')
    # C1-C2 (horizontal)
    parts.append('<line x1="60" y1="140" x2="124" y2="140"/>')
    # C2-C3 (horizontal)
    parts.append('<line x1="156" y1="140" x2="244" y2="140"/>')
    # C3-C4 (horizontal)
    parts.append('<line x1="276" y1="140" x2="340" y2="140"/>')
    # C2 vertical bonds
    if sub2_above:
        if sub2_above_double:
            parts.append(f'<line x1="136" y1="132" x2="136" y2="{146-sub2_above_dy+18}"/>')
            parts.append(f'<line x1="144" y1="132" x2="144" y2="{146-sub2_above_dy+18}"/>')
        else:
            parts.append(f'<line x1="140" y1="132" x2="140" y2="{146-sub2_above_dy+18}"/>')
    if sub2_below and show_c2_below_bond:
        parts.append(f'<line x1="140" y1="152" x2="140" y2="{146+c2_below_dy-18}"/>')
    # C3 vertical bonds
    if sub3_above:
        parts.append('<line x1="260" y1="132" x2="260" y2="64"/>')
    if sub3_below:
        parts.append('<line x1="260" y1="152" x2="260" y2="204"/>')
    parts.append('</g>')
    parts.append('</g>')
    return "".join(parts)


# ---------------------------------------------------------------------------
# Specific molecule fragments (each rendered at translate(ox, oy))
# ---------------------------------------------------------------------------
def substrate(ox=0, oy=0):
    """(CH3)2C(Br)-C(CH3)3 — 2-bromo-2,3,3-trimethylbutane."""
    return molecule_skeleton(ox, oy, sub2_below="Br", sub2_below_color="#a0392f")

def cation(ox=0, oy=0):
    """(CH3)2C(+)-C(CH3)3 carbocation."""
    return molecule_skeleton(ox, oy, sub2_below="", c2_super="+", show_c2_below_bond=False)

def oxonium(ox=0, oy=0):
    """C2 carries -O(+)(H)(CH3) instead of Br."""
    extra = ''
    sub2_below_html = '<tspan font-size="22">O</tspan><tspan baseline-shift="super" font-size="14" fill="#1f6feb" font-weight="bold">+</tspan>'
    s = molecule_skeleton(ox, oy, sub2_below=sub2_below_html, sub2_below_color="#0e7c66",
                          show_c2_below_bond=True, c2_below_dy=70)
    # add H and CH3 branches off the O
    extra_svg = f'''<g transform="translate({ox},{oy})">
        <text x="178" y="218" font-family="Arial" font-size="18" fill="#1a1a1a">H</text>
        <text x="170" y="260" font-family="Arial" font-size="18" fill="#1a1a1a">CH<tspan baseline-shift="sub" font-size="12">3</tspan></text>
        <line x1="155" y1="212" x2="170" y2="212" stroke="#1a1a1a" stroke-width="2"/>
        <line x1="148" y1="225" x2="172" y2="248" stroke="#1a1a1a" stroke-width="2"/>
    </g>'''
    return s + extra_svg

def ether(ox=0, oy=0):
    """C2 carries -OCH3 instead of Br (final SN1 product)."""
    s = molecule_skeleton(ox, oy, sub2_below="O", sub2_below_color="#0e7c66",
                          show_c2_below_bond=True, c2_below_dy=70)
    extra = f'''<g transform="translate({ox},{oy})">
      <text x="170" y="260" font-family="Arial" font-size="18" fill="#1a1a1a">CH<tspan baseline-shift="sub" font-size="12">3</tspan></text>
      <line x1="148" y1="225" x2="172" y2="248" stroke="#1a1a1a" stroke-width="2"/>
    </g>'''
    return s + extra

def alkene_product(ox=0, oy=0):
    """CH2=C(CH3)-C(CH3)3 — 2,3,3-trimethyl-1-butene.
    Replace top-CH3 of C2 with =CH2 (double bond)."""
    sub_above = 'CH<tspan baseline-shift="sub" font-size="13">2</tspan>'
    return molecule_skeleton(ox, oy, sub2_above=sub_above, sub2_below="",
                             show_c2_below_bond=False,
                             sub2_above_double=True, sub2_above_dy=70)

def methanol(ox, oy, lone_pairs=True, label="methanol"):
    """Draws CH3-O-H with two lone pairs on O.

    Layout (local):
      CH3 at (20, 30); O at (90, 30); H at (140, 30)
      lone pairs above and below O
    """
    pieces = [f'<g transform="translate({ox},{oy})" font-family="Arial, sans-serif">']
    pieces.append('<text x="20" y="36" font-size="18" text-anchor="middle">'
                  'H<tspan baseline-shift="sub" font-size="11">3</tspan>C</text>')
    pieces.append('<text x="90" y="36" font-size="20" font-weight="bold" fill="#0e7c66" text-anchor="middle">O</text>')
    pieces.append('<text x="140" y="36" font-size="18" text-anchor="middle">H</text>')
    pieces.append('<line x1="38" y1="30" x2="78" y2="30" stroke="#1a1a1a" stroke-width="2"/>')
    pieces.append('<line x1="102" y1="30" x2="130" y2="30" stroke="#1a1a1a" stroke-width="2"/>')
    if lone_pairs:
        pieces.append('<text x="90" y="14" font-size="22" fill="#0e7c66" text-anchor="middle" font-weight="bold">··</text>')
        pieces.append('<text x="90" y="58" font-size="22" fill="#0e7c66" text-anchor="middle" font-weight="bold">··</text>')
    pieces.append('</g>')
    return "".join(pieces)

def methyloxonium(ox, oy):
    """CH3-O(+)H2 — protonated methanol (after acting as base)."""
    pieces = [f'<g transform="translate({ox},{oy})" font-family="Arial, sans-serif">']
    pieces.append('<text x="20" y="36" font-size="18" text-anchor="middle">'
                  'H<tspan baseline-shift="sub" font-size="11">3</tspan>C</text>')
    pieces.append('<text x="90" y="36" font-size="20" font-weight="bold" fill="#0e7c66" text-anchor="middle">O</text>')
    pieces.append('<text x="106" y="20" font-size="14" font-weight="bold" fill="#1f6feb">+</text>')
    pieces.append('<text x="140" y="20" font-size="18" text-anchor="middle">H</text>')
    pieces.append('<text x="140" y="52" font-size="18" text-anchor="middle">H</text>')
    pieces.append('<line x1="38" y1="30" x2="78" y2="30" stroke="#1a1a1a" stroke-width="2"/>')
    pieces.append('<line x1="100" y1="22" x2="128" y2="14" stroke="#1a1a1a" stroke-width="2"/>')
    pieces.append('<line x1="100" y1="38" x2="128" y2="46" stroke="#1a1a1a" stroke-width="2"/>')
    pieces.append('</g>')
    return "".join(pieces)

def bromide(ox, oy):
    """:Br:⁻ — bromide ion with lone pairs."""
    return f'''<g transform="translate({ox},{oy})" font-family="Arial, sans-serif">
      <text x="0" y="36" font-size="22" font-weight="bold" fill="#a0392f">Br</text>
      <text x="36" y="22" font-size="14" font-weight="bold" fill="#1f6feb">−</text>
      <text x="14" y="20" font-size="16" fill="#a0392f" font-weight="bold">··</text>
      <text x="14" y="58" font-size="16" fill="#a0392f" font-weight="bold">··</text>
      <text x="-6" y="36" font-size="16" fill="#a0392f" font-weight="bold">··</text>
    </g>'''

def reaction_arrow(ox, oy, label_top="", label_bottom=""):
    """Standard reaction arrow → with optional labels above/below."""
    pieces = [f'<g transform="translate({ox},{oy})">']
    pieces.append('<line x1="0" y1="20" x2="80" y2="20" stroke="#1a1a1a" stroke-width="2" marker-end="url(#arr-blk)"/>')
    if label_top:
        pieces.append(f'<text x="40" y="10" text-anchor="middle" font-size="13" fill="#666" font-style="italic">{label_top}</text>')
    if label_bottom:
        pieces.append(f'<text x="40" y="38" text-anchor="middle" font-size="13" fill="#666" font-style="italic">{label_bottom}</text>')
    pieces.append('</g>')
    return "".join(pieces)

def plus_sign(ox, oy):
    return f'<text x="{ox}" y="{oy}" font-family="Arial" font-size="28" font-weight="bold" fill="#1a1a1a" text-anchor="middle">+</text>'

def curly_arrow(x1, y1, x2, y2, cx, cy, color="#e23636", w=2):
    return (f'<path d="M{x1},{y1} Q{cx},{cy} {x2},{y2}" fill="none" '
            f'stroke="{color}" stroke-width="{w}" marker-end="url(#arr-red)"/>')

def label_text(x, y, text, size=14, color="#666", anchor="middle", italic=True):
    style = ' font-style="italic"' if italic else ''
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Arial" '
            f'font-size="{size}" fill="{color}"{style}>{text}</text>')

# ---------------------------------------------------------------------------
# Mechanism panels
# ---------------------------------------------------------------------------
def panel_step1():
    """Ionization: substrate → carbocation + bromide."""
    svg = [f'<svg viewBox="0 0 1020 320" class="mech" xmlns="http://www.w3.org/2000/svg">{DEFS}']
    # Substrate at (10, 20). With ox=10, oy=20:
    #   C2 label at (150, 166); C2-Br bond from (150, 172) to (150, 218); Br label at (150, 236)
    svg.append(substrate(10, 20))
    svg.append(label_text(150, 295, "2-bromo-2,3,3-trimethylbutane"))
    # Curved arrow: C-Br bond pair going onto Br
    svg.append(curly_arrow(155, 188, 155, 228, 195, 208))
    svg.append(label_text(220, 200, "bond pair → Br", color="#e23636", anchor="start", size=12))
    # Reaction arrow
    svg.append(reaction_arrow(420, 140, label_top="slow · RDS",
                              label_bottom="ionization"))
    # Cation at (530, 20)
    svg.append(cation(530, 20))
    svg.append(label_text(670, 295, "tertiary carbocation (3°)"))
    # Plus sign
    svg.append(plus_sign(910, 175))
    # Bromide
    svg.append(bromide(940, 145))
    svg.append(label_text(960, 220, ":Br⁻", color="#a0392f", italic=False, size=12))
    svg.append('</svg>')
    return "\n".join(svg)

def panel_sn1_attack():
    """SN1 step 2: methanol attacks the carbocation."""
    svg = [f'<svg viewBox="0 0 1140 360" class="mech" xmlns="http://www.w3.org/2000/svg">{DEFS}']
    # Cation at (10, 30). C2+ label at (150, 176).
    svg.append(cation(10, 30))
    svg.append(label_text(150, 305, "carbocation"))
    svg.append(plus_sign(390, 180))
    # Methanol at (420, 220): O label at (510, 250); top lone pair ~ (510, 236); bottom ~ (510, 278)
    svg.append(methanol(420, 220))
    svg.append(label_text(490, 308, "methanol  (nucleophile)"))
    # Curved arrow from methanol TOP lone pair up & left to C2+
    svg.append(curly_arrow(508, 232, 158, 184, 320, 90))
    svg.append(label_text(330, 80, "O lone pair attacks C⁺", color="#e23636"))
    # Reaction arrow
    svg.append(reaction_arrow(640, 170, label_top="fast"))
    # Oxonium product at right
    svg.append(oxonium(740, 30))
    svg.append(label_text(880, 305, "oxonium intermediate"))
    svg.append('</svg>')
    return "\n".join(svg)

def panel_sn1_deprot():
    """SN1 step 3: a second methanol deprotonates the oxonium."""
    svg = [f'<svg viewBox="0 0 1140 360" class="mech" xmlns="http://www.w3.org/2000/svg">{DEFS}']
    # Oxonium at (10, 30). With ox=10, oy=30:
    #   C2 at (150, 176), O label at (150, 246), O-H bond from (165, 242) to (180, 242), H at (188, 248)
    svg.append(oxonium(10, 30))
    svg.append(label_text(150, 320, "oxonium intermediate"))
    svg.append(plus_sign(400, 270))
    # Second methanol at (430, 270): O at (520, 300); top lone pair ~ y=286; bottom ~ y=328
    svg.append(methanol(430, 270))
    svg.append(label_text(500, 358, "another methanol  (acts as base)"))
    # Arrow ① — MeOH lone pair (top, ~520, 286) up & LEFT to the oxonium-H at (188, 248)
    svg.append(curly_arrow(516, 282, 198, 252, 360, 200))
    svg.append(label_text(360, 188, "①  base grabs the H⁺", color="#e23636"))
    # Arrow ② — O–H bond electrons collapse back onto O on the oxonium
    # O-H bond is from (165, 242) to (180, 242). Show arrow from bond midpoint to O.
    svg.append(curly_arrow(178, 235, 162, 235, 170, 218))
    svg.append(label_text(170, 208, "②  O–H electrons → O", color="#e23636", size=12))
    # Reaction arrow
    svg.append(reaction_arrow(640, 170, label_top="fast"))
    # Final ether product
    svg.append(ether(740, 30))
    svg.append(label_text(880, 320, "2-methoxy-2,3,3-trimethylbutane"))
    svg.append(plus_sign(945, 290))
    svg.append(methyloxonium(960, 280))
    svg.append(label_text(1030, 350, "(CH₃OH₂⁺)", color="#9aa6c4", size=11))
    svg.append('</svg>')
    return "\n".join(svg)

def panel_e1():
    """E1 step 2: methanol removes a β-H from a methyl on C2; π bond forms."""
    svg = [f'<svg viewBox="0 0 1100 380" class="mech" xmlns="http://www.w3.org/2000/svg">{DEFS}']
    # Cation at (10, 130). With ox=10, oy=130:
    #   C2+ label at (150, 276); top-CH3 (β-C) label at (150, 206)
    #   C2-Cβ bond from (150, 262) to (150, 224)
    svg.append(cation(10, 130))
    svg.append(label_text(150, 370, "carbocation (3° at C2)"))
    # Show one β-H explicitly to the left of the β-CH3 to anchor the arrows
    # β-CH3 label is at (150, 206). Add an explicit H at (108, 198) bonded to β-C.
    svg.append('<text x="108" y="200" font-family="Arial" font-size="18" fill="#1a1a1a">H</text>')
    svg.append('<line x1="124" y1="195" x2="138" y2="200" stroke="#1a1a1a" stroke-width="2"/>')
    svg.append(label_text(78, 200, "β-H", color="#0e7c66", size=12))
    # Methanol at (10, 30): O at (100, 60); top dots ~y=44; bottom dots ~y=88
    svg.append(methanol(10, 30))
    svg.append(label_text(80, 18, "methanol  (acts as base)"))
    # Arrow ① — methanol bottom lone pair down & right to β-H
    svg.append(curly_arrow(102, 96, 116, 192, 80, 150))
    svg.append(label_text(60, 145, "①", size=22, color="#e23636", italic=False))
    # Arrow ② — Cβ-H bond electrons flow into the C2-Cβ bond, becoming the π bond
    # C-H bond runs from (124, 195) to (138, 200). Send electrons toward C2-Cβ bond region (~150, 240).
    svg.append(curly_arrow(132, 208, 148, 250, 130, 230))
    svg.append(label_text(170, 240, "②  forms π bond", color="#e23636", size=12))
    # Reaction arrow
    svg.append(reaction_arrow(420, 250, label_top="loses β-H",
                              label_bottom="builds C=C"))
    # Alkene product at (530, 130)
    svg.append(alkene_product(530, 130))
    svg.append(label_text(670, 370, "2,3,3-trimethyl-1-butene"))
    svg.append(plus_sign(900, 260))
    svg.append(methyloxonium(920, 250))
    svg.append(label_text(990, 320, "(CH₃OH₂⁺)", color="#9aa6c4", size=11))
    svg.append('</svg>')
    return "\n".join(svg)


def panel_products():
    """Side-by-side display of the two final products."""
    svg = [f'<svg viewBox="0 0 880 280" class="mech" xmlns="http://www.w3.org/2000/svg">{DEFS}']
    svg.append(ether(20, 0))
    svg.append(label_text(160, 270, "S_N1 product:  2-methoxy-2,3,3-trimethylbutane", size=15, color="#1f6feb", italic=False))
    svg.append('<line x1="450" y1="20" x2="450" y2="240" stroke="#666" stroke-width="1" stroke-dasharray="6,6"/>')
    svg.append(alkene_product(490, 0))
    svg.append(label_text(640, 270, "E1 product:  2,3,3-trimethyl-1-butene", size=15, color="#16a365", italic=False))
    svg.append('</svg>')
    return "\n".join(svg)


def panel_substrate_analysis():
    """Annotated substrate showing key features."""
    svg = [f'<svg viewBox="0 0 760 320" class="mech" xmlns="http://www.w3.org/2000/svg">{DEFS}']
    svg.append(substrate(180, 30))
    # Annotations:
    # 1. Tertiary C* at C2
    svg.append('<text x="360" y="170" font-family="Arial" font-size="13" fill="#e23636" font-style="italic">3° carbon (will hold + after Br leaves)</text>')
    svg.append('<line x1="360" y1="166" x2="328" y2="166" stroke="#e23636" stroke-width="1"/>')
    # 2. Br is the leaving group (below C2)
    svg.append('<text x="120" y="252" font-family="Arial" font-size="13" fill="#a0392f" font-style="italic">leaving group</text>')
    svg.append('<line x1="200" y1="248" x2="305" y2="248" stroke="#a0392f" stroke-width="1"/>')
    # 3. β-H locations (highlight upper CH3 of C2)
    svg.append('<text x="490" y="100" font-family="Arial" font-size="13" fill="#0e7c66" font-style="italic">β-Hs only here (and on the lower-left CH₃)</text>')
    svg.append('<line x1="488" y1="96" x2="340" y2="96" stroke="#0e7c66" stroke-width="1"/>')
    # 4. C3 quaternary - no β-Hs
    svg.append('<text x="490" y="218" font-family="Arial" font-size="13" fill="#1f6feb" font-style="italic">C3 is quaternary  →  NO β-H this side</text>')
    svg.append('<line x1="488" y1="214" x2="460" y2="214" stroke="#1f6feb" stroke-width="1"/>')
    svg.append('</svg>')
    return "\n".join(svg)

# ---------------------------------------------------------------------------
# HTML page
# ---------------------------------------------------------------------------
HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Problem 7-17 — Solvolysis of 2-Bromo-2,3,3-trimethylbutane in Methanol</title>
<style>
:root{{--bg:#0f1320;--panel:#171c2e;--panel2:#1e2438;--ink:#e8ecf6;--muted:#9aa6c4;
  --acc:#5dd6c0;--acc2:#7aa2ff;--warn:#ffb454;--bad:#ff6b81;--good:#52e0a0;
  --line:#2a3350;--chip:#243049;}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  background:var(--bg);color:var(--ink);line-height:1.65;font-size:17px}}
a{{color:var(--acc2);text-decoration:none}}
a:hover{{text-decoration:underline}}
header.hero{{background:linear-gradient(135deg,#202a4a,#0f1320);padding:38px 22px 26px;
  text-align:center;border-bottom:1px solid var(--line)}}
header.hero h1{{margin:0 0 8px;font-size:1.85rem}}
header.hero p{{margin:6px 0;color:var(--muted)}}
.back{{display:inline-block;margin:6px 0;color:var(--acc);font-size:.9rem;
  border:1px solid var(--line);padding:4px 12px;border-radius:999px}}
main{{max-width:1080px;margin:0 auto;padding:24px 18px 80px}}
section{{background:var(--panel);border:1px solid var(--line);border-radius:14px;
  padding:22px 24px;margin:0 0 22px}}
section h2{{margin:0 0 6px;color:var(--acc);font-size:1.35rem}}
section h2 .num{{color:var(--muted);font-size:.95rem;font-weight:600;margin-right:6px}}
h3{{color:var(--acc2);margin:18px 0 6px;font-size:1.08rem}}
.problem{{background:var(--panel2);border-left:4px solid var(--acc);
  border-radius:0 12px 12px 0;padding:14px 18px;margin:6px 0 14px;font-size:.98rem}}
.callout{{border-radius:12px;padding:12px 16px;margin:14px 0;border:1px solid}}
.key{{background:rgba(93,214,192,.08);border-color:rgba(93,214,192,.4)}}
.key::before{{content:"🔑 KEY POINT";display:block;font-weight:700;color:var(--acc);
  font-size:.78rem;letter-spacing:1px;margin-bottom:4px}}
.tip{{background:rgba(122,162,255,.08);border-color:rgba(122,162,255,.4)}}
.tip::before{{content:"💡 INSIGHT";display:block;font-weight:700;color:var(--acc2);
  font-size:.78rem;letter-spacing:1px;margin-bottom:4px}}
.warn{{background:rgba(255,180,84,.08);border-color:rgba(255,180,84,.45)}}
.warn::before{{content:"⚠️ COMMON TRAP";display:block;font-weight:700;color:var(--warn);
  font-size:.78rem;letter-spacing:1px;margin-bottom:4px}}
.mech{{display:block;width:100%;height:auto;background:#fafbfc;border-radius:12px;
  padding:6px;border:1px solid var(--line);margin:14px 0}}
.steplabel{{display:inline-block;background:var(--chip);color:var(--acc);
  padding:3px 12px;border-radius:999px;font-size:.85rem;letter-spacing:.5px;
  border:1px solid var(--line);margin-right:8px}}
.legend{{display:flex;gap:12px;flex-wrap:wrap;font-size:.85rem;color:var(--muted);
  margin-top:8px}}
.legend span{{padding:3px 10px;border:1px solid var(--line);border-radius:999px}}
.legend .red{{color:#ff8b8b;border-color:#552a2a}}
.legend .blue{{color:#a0c0ff;border-color:#2a3a55}}
.legend .green{{color:#7adfb6;border-color:#2a4a3a}}
table{{width:100%;border-collapse:collapse;margin:14px 0;font-size:.94rem}}
th,td{{border:1px solid var(--line);padding:9px 11px;text-align:left;vertical-align:top}}
th{{background:var(--panel2);color:var(--acc)}}
tr:nth-child(even) td{{background:rgba(255,255,255,.02)}}
ul,ol{{margin:8px 0 8px 4px;padding-left:22px}}
li{{margin:5px 0}}
.products{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:8px}}
.products .card{{background:var(--panel2);border:1px solid var(--line);
  border-radius:10px;padding:12px}}
.products .card h4{{margin:0 0 6px;color:var(--acc2)}}
.products .card.green h4{{color:var(--good)}}
.formula{{background:var(--panel2);border:1px dashed var(--acc);border-radius:10px;
  padding:10px 14px;margin:10px 0;text-align:center;font-size:1.05rem}}
footer{{text-align:center;color:var(--muted);padding:26px;border-top:1px solid var(--line);
  font-size:.88rem;margin-top:16px}}
</style>
</head>
<body>
<header class="hero">
  <a class="back" href="index.html">← Back to main study guide</a>
  <h1>Problem 7-17 — Solution &amp; Mechanisms</h1>
  <p>Solvolysis of 2-bromo-2,3,3-trimethylbutane in methanol</p>
  <p style="font-size:.88rem">Why this substrate? It’s the textbook example of clean S<sub>N</sub>1 / E1 competition with <b>no rearrangement and no Hofmann/Zaitsev ambiguity.</b></p>
</header>
<main>

<section id="problem">
  <h2><span class="num">7-17</span>The problem</h2>
  <div class="problem">
    <p>S<sub>N</sub>1 substitution and E1 elimination frequently compete in the same reaction.</p>
    <p><b>(a)</b> Propose a mechanism and predict the products for the solvolysis of <b>2-bromo-2,3,3-trimethylbutane</b> in <b>methanol</b>.</p>
    <p><b>(b)</b> Compare the function of the solvent (methanol) in the E1 and S<sub>N</sub>1 reactions.</p>
  </div>
</section>

<section id="setup">
  <h2><span class="num">Setup</span>Recognize the substrate &amp; reaction type</h2>
  <p>Before drawing arrows, look hard at the substrate. Three features decide everything:</p>
  {panel_substrate_analysis()}
  <ol>
    <li><b>C2 is tertiary (3°)</b> and bears the leaving group (Br). 3° + a polar protic solvent (MeOH) ⇒ ionizes readily ⇒ <b>S<sub>N</sub>1 / E1</b> regime (not S<sub>N</sub>2 / E2).</li>
    <li><b>Methanol is a weak nucleophile and weak base</b> — exactly the condition that lets a carbocation form and then be intercepted. The word <i>solvolysis</i> means the solvent is doing the chemistry.</li>
    <li><b>C3 is quaternary, so it carries NO hydrogens.</b> The β-Hs that an E1 can remove can only come from the <b>two methyl groups attached to C2</b> (which are equivalent), so there is exactly <b>ONE possible alkene</b>. That removes the usual “Zaitsev vs Hofmann” headache.</li>
  </ol>
  <div class="callout key">Both pathways begin with the <b>same first step</b> — C–Br ionizes to a 3° carbocation. Once that cation exists, methanol can react with it in <b>two different ways</b>: as a <b>nucleophile</b> (→ S<sub>N</sub>1) or as a <b>base</b> (→ E1). That branching point is the whole problem.</div>
</section>

<section id="step1">
  <h2><span class="num">Step 1</span>Ionization (rate-determining, common to both)</h2>
  <p>The C–Br bond breaks <b>heterolytically</b>. Both electrons stay with bromine — the curved red arrow shows the bond-pair leaving with Br. C2 is left with an empty p orbital and a positive charge.</p>
  {panel_step1()}
  <div class="legend">
    <span class="red">Red curved arrow = movement of an electron pair</span>
    <span class="blue">Blue + / − = formal charge</span>
  </div>
  <ul>
    <li>This step is <b>slow / rate-determining</b> — it requires breaking a bond without any help from the nucleophile.</li>
    <li>The 3° carbocation that forms is <b>stable enough to live</b> long enough for methanol to find it (hyperconjugation + inductive donation from six surrounding methyls).</li>
    <li>kinetics: rate = k[substrate]  (<b>first order</b>, hence the “1” in S<sub>N</sub>1 / E1).</li>
  </ul>
</section>

<section id="sn1">
  <h2><span class="num">Pathway A</span>S<sub>N</sub>1 — methanol as <i>nucleophile</i></h2>
  <h3>Step 2a · Methanol uses an oxygen lone pair to attack C⁺</h3>
  {panel_sn1_attack()}
  <p>An oxygen lone pair on methanol drops onto the empty p-orbital at C2, forming a new <b>C–O bond</b>. Because oxygen now has <b>three bonds</b> (to its CH₃, to its H, and to C2), it carries a <b>formal +1</b> charge — this is an <b>oxonium ion</b>.</p>
  <h3>Step 2b · A second methanol takes the proton off the oxonium</h3>
  {panel_sn1_deprot()}
  <p>The oxonium is acidic (loss of H⁺ regenerates a neutral, stable ether). A <i>second</i> molecule of methanol grabs that proton — its lone pair attacks the H, the O–H bond electrons collapse back onto oxygen, and the catalyst-like role of methanol is complete.</p>
  <div class="callout tip">Notice that methanol appears <b>twice</b> in S<sub>N</sub>1: first as a <b>nucleophile</b> (forming the C–O bond), then as a <b>base</b> (removing the extra H from the resulting oxonium).</div>
  <div class="formula"><b>S<sub>N</sub>1 product</b> &nbsp;=&nbsp; (CH<sub>3</sub>)<sub>2</sub>C(OCH<sub>3</sub>)–C(CH<sub>3</sub>)<sub>3</sub>  &nbsp;=&nbsp; <b>2-methoxy-2,3,3-trimethylbutane</b> (a <i>tert</i>-alkyl methyl ether)</div>
</section>

<section id="e1">
  <h2><span class="num">Pathway B</span>E1 — methanol as <i>base</i></h2>
  <p>From the same carbocation, methanol can instead use its oxygen lone pair to grab a <b>β-hydrogen</b> (a hydrogen on a carbon adjacent to C⁺). The C–H bond electrons then flow into the empty p-orbital on C2, forming the new <b>π bond</b> of the alkene.</p>
  {panel_e1()}
  <p>Two arrows in one concerted-looking step:</p>
  <ol>
    <li><b>Arrow ①:</b> O lone pair (methanol) → β-H. Methanol is acting as a <b>Brønsted base</b>.</li>
    <li><b>Arrow ②:</b> C–H bond electrons → into the C–C bond, becoming the new C=C π bond.</li>
  </ol>
  <div class="callout warn">In the slide deck this looks identical to E2, but it’s genuinely E1: the carbocation already exists from Step 1. The “base step” here is the second, <b>fast</b> step — it doesn’t appear in the rate law.</div>
  <div class="formula"><b>E1 product</b> &nbsp;=&nbsp; CH<sub>2</sub>=C(CH<sub>3</sub>)–C(CH<sub>3</sub>)<sub>3</sub> &nbsp;=&nbsp; <b>2,3,3-trimethyl-1-butene</b></div>
  <div class="callout key">Because <b>C3 has no hydrogens</b>, β-elimination toward C3 is impossible. The only β-Hs sit on the two methyls bonded to C2, and those methyls are equivalent — so the E1 gives <b>exactly one alkene</b>. No Zaitsev/Hofmann competition here.</div>
</section>

<section id="products">
  <h2><span class="num">Products</span>What actually comes out of the flask</h2>
  <p>Solvolysis gives a <b>mixture of both products</b> — the relative amounts depend on temperature (higher T usually favors elimination) and on the exact solvent system. For (a), you should report:</p>
  {panel_products()}
  <div class="products">
    <div class="card">
      <h4>S<sub>N</sub>1 product</h4>
      2-methoxy-2,3,3-trimethylbutane<br>
      <span style="color:var(--muted);font-size:.9rem">(an unsymmetrical methyl tert-alkyl ether)</span>
    </div>
    <div class="card green">
      <h4>E1 product</h4>
      2,3,3-trimethyl-1-butene<br>
      <span style="color:var(--muted);font-size:.9rem">(only possible alkene — no β-H on C3)</span>
    </div>
  </div>
</section>

<section id="no-rearr">
  <h2><span class="num">Aside</span>Why we don’t need to worry about rearrangement here</h2>
  <p>Carbocation rearrangements happen when a 1,2-hydride or 1,2-methyl shift produces a <b>more stable</b> cation. Let's check that for our cation:</p>
  <ul>
    <li>The starting cation is already <b>3° at C2</b>: (CH<sub>3</sub>)<sub>2</sub>C<sup>+</sup>–C(CH<sub>3</sub>)<sub>3</sub>.</li>
    <li>A methyl could in principle migrate from C3 to C2. But the new cation at C3 — (CH<sub>3</sub>)<sub>3</sub>C–C<sup>+</sup>(CH<sub>3</sub>)<sub>2</sub> — is <b>also 3°</b> with the same neopentyl neighbor.</li>
    <li>So the rearrangement is <b>energetically degenerate</b> — there’s no driving force to do it, and even if it does, the cation is <b>chemically the same species</b>.</li>
  </ul>
  <div class="callout tip">That symmetry is exactly why Wade picked this substrate for Problem 7-17: it isolates the S<sub>N</sub>1 vs E1 partitioning <b>without</b> the noise from rearranged products.</div>
</section>

<section id="part-b">
  <h2><span class="num">Part (b)</span>The role of methanol in each pathway</h2>
  <p>Methanol uses an <b>oxygen lone pair</b> in <i>both</i> reactions — but it points that lone pair at <b>different targets</b>:</p>
  <table>
    <tr><th>Aspect</th><th>S<sub>N</sub>1 substitution</th><th>E1 elimination</th></tr>
    <tr><td><b>Methanol acts as a…</b></td><td><b>Nucleophile</b></td><td><b>Brønsted base</b></td></tr>
    <tr><td><b>Target of the O lone pair</b></td><td>The electrophilic carbon (C⁺)</td><td>A β-hydrogen (a proton on the carbon next to C⁺)</td></tr>
    <tr><td><b>New bond formed</b></td><td>C–O</td><td>O–H</td></tr>
    <tr><td><b>What forms in the product</b></td><td>An ether (after losing one extra H)</td><td>A C=C π bond</td></tr>
    <tr><td><b>Methanol used per molecule of product</b></td><td>2  (one attacks, one deprotonates the oxonium)</td><td>1  (acts only as base; goes off as CH<sub>3</sub>OH<sub>2</sub><sup>+</sup>)</td></tr>
    <tr><td><b>Why it works at all</b></td><td>O has lone pairs and is mildly nucleophilic</td><td>O has lone pairs and is mildly basic</td></tr>
  </table>
  <div class="callout key">Same molecule, same lone pair — different <b>destination</b>. That’s the entire essence of the S<sub>N</sub>1 / E1 partitioning, and the reason these two reactions <b>must</b> compete whenever a carbocation forms in a protic solvent.</div>
</section>

<section id="takeaways">
  <h2><span class="num">★</span>Exam-ready takeaways</h2>
  <ul>
    <li><b>Solvolysis of a 3° halide in a polar protic solvent</b> ⇒ assume <b>S<sub>N</sub>1 + E1 mixture</b>, never S<sub>N</sub>2 or E2.</li>
    <li>The <b>rate-determining step</b> is ionization. After that, products are decided by which of methanol’s two roles wins out.</li>
    <li>Methanol = <b>nucleophile</b> in S<sub>N</sub>1 (attacks C⁺), and = <b>base</b> in E1 (grabs a β-H).</li>
    <li>For this specific substrate: the 3° cation can’t rearrange to anything more stable, and only one alkene is geometrically possible (no β-H on C3) — so the answer is two clean products: <b>2-methoxy-2,3,3-trimethylbutane</b> and <b>2,3,3-trimethyl-1-butene</b>.</li>
    <li>If you’re asked “which dominates?”, remember the rule of thumb: <b>more heat → more elimination (E1)</b>; cooler conditions favor the substitution.</li>
  </ul>
</section>

</main>
<footer>
  Worked solution generated for your exam prep.<br>
  Mechanism drawings rendered as inline SVG — sharp at any zoom level.
</footer>
</body>
</html>
"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)

print(f"Wrote {OUT}  ({len(HTML)/1024:.1f} KB)")
