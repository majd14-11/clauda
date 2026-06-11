#!/usr/bin/env python3
"""Generates a self-contained interactive HTML study guide for Chapter 7 (Alkenes).
Images extracted from the source PDF are embedded as base64 data URIs so the final
index.html works as a single offline file."""
import base64, os, html

IMG_DIR = os.path.join(os.path.dirname(__file__), "images")

def img(objnum, caption="", cls=""):
    """Return an <figure> with the image (obj number) embedded as base64."""
    for ext in ("png", "jpg"):
        path = os.path.join(IMG_DIR, f"img_{objnum:03d}.{ext}")
        if os.path.exists(path):
            with open(path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            mime = "image/png" if ext == "png" else "image/jpeg"
            cap = f"<figcaption>{caption}</figcaption>" if caption else ""
            return (f'<figure class="fig {cls}">'
                    f'<img loading="lazy" src="data:{mime};base64,{b64}" alt="{html.escape(caption)}">'
                    f'{cap}</figure>')
    return f"<!-- missing img {objnum} -->"

def gallery(objnums, caption=""):
    inner = "".join(img(n) for n in objnums)
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f'<div class="gallery">{inner}{cap}</div>'

# ---------------------------------------------------------------------------
# The full HTML body is assembled from SECTIONS. Each section gets full prose
# explanations (written to go beyond the slide bullets) plus the matching
# figures extracted from the original deck.
# ---------------------------------------------------------------------------
PLACEHOLDER = "__BODY__"


HTML_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Chapter 7 — Alkenes | Master Study Guide</title>
<style>
:root{
  --bg:#0f1320; --panel:#171c2e; --panel2:#1e2438; --ink:#e8ecf6; --muted:#9aa6c4;
  --acc:#5dd6c0; --acc2:#7aa2ff; --warn:#ffb454; --bad:#ff6b81; --good:#52e0a0;
  --line:#2a3350; --chip:#243049;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  background:var(--bg);color:var(--ink);line-height:1.65;font-size:17px}
a{color:var(--acc2);text-decoration:none}
a:hover{text-decoration:underline}
header.hero{background:linear-gradient(135deg,#202a4a,#0f1320);padding:46px 22px 38px;text-align:center;border-bottom:1px solid var(--line)}
header.hero h1{margin:0 0 8px;font-size:2.1rem;letter-spacing:.3px}
header.hero p{margin:4px 0;color:var(--muted)}
.badge{display:inline-block;background:var(--chip);color:var(--acc);padding:3px 12px;border-radius:999px;font-size:.8rem;margin:6px 4px 0;border:1px solid var(--line)}
.wrap{max-width:920px;margin:0 auto;padding:0 20px}
.layout{display:flex;gap:26px;max-width:1240px;margin:0 auto;padding:0 20px}
nav.toc{position:sticky;top:0;align-self:flex-start;width:255px;max-height:100vh;overflow:auto;
  padding:22px 8px 40px;font-size:.92rem;flex:0 0 auto}
nav.toc h3{font-size:.75rem;text-transform:uppercase;letter-spacing:1.5px;color:var(--muted);margin:18px 0 8px}
nav.toc a{display:block;color:var(--muted);padding:5px 10px;border-radius:7px;border-left:2px solid transparent}
nav.toc a:hover{background:var(--panel);color:var(--ink);text-decoration:none}
nav.toc a.active{color:var(--acc);border-left-color:var(--acc);background:var(--panel)}
main{flex:1 1 auto;min-width:0;padding:26px 0 80px}
section.topic{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:24px 26px;margin:0 0 26px;scroll-margin-top:14px}
section.topic h2{margin:0 0 6px;font-size:1.5rem;color:var(--acc)}
section.topic h2 .sec{color:var(--muted);font-size:.95rem;font-weight:600}
h3.sub{color:var(--acc2);margin:22px 0 8px;font-size:1.15rem}
h4.sub{color:#cdd6ee;margin:16px 0 6px}
p{margin:10px 0}
ul,ol{margin:10px 0 10px 4px;padding-left:22px}
li{margin:6px 0}
.fig{margin:16px 0;background:#fff;border-radius:12px;padding:10px;text-align:center;border:1px solid var(--line)}
.fig img{max-width:100%;height:auto;border-radius:6px;display:block;margin:0 auto}
.fig figcaption,.gallery figcaption{color:var(--muted);font-size:.85rem;margin-top:8px;text-align:center}
.gallery{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin:16px 0;align-items:flex-start}
.gallery .fig{flex:1 1 240px;margin:0;max-width:100%}
.callout{border-radius:12px;padding:13px 16px;margin:16px 0;border:1px solid}
.key{background:rgba(93,214,192,.08);border-color:rgba(93,214,192,.4)}
.key::before{content:"🔑 KEY RULE";display:block;font-weight:700;color:var(--acc);font-size:.78rem;letter-spacing:1px;margin-bottom:4px}
.tip{background:rgba(122,162,255,.08);border-color:rgba(122,162,255,.4)}
.tip::before{content:"💡 EXAM TIP";display:block;font-weight:700;color:var(--acc2);font-size:.78rem;letter-spacing:1px;margin-bottom:4px}
.warnbox{background:rgba(255,180,84,.08);border-color:rgba(255,180,84,.45)}
.warnbox::before{content:"⚠️ WATCH OUT";display:block;font-weight:700;color:var(--warn);font-size:.78rem;letter-spacing:1px;margin-bottom:4px}
.mnem{background:rgba(82,224,160,.08);border-color:rgba(82,224,160,.4)}
.mnem::before{content:"🧠 MEMORY AID";display:block;font-weight:700;color:var(--good);font-size:.78rem;letter-spacing:1px;margin-bottom:4px}
table{width:100%;border-collapse:collapse;margin:16px 0;font-size:.93rem}
th,td{border:1px solid var(--line);padding:9px 11px;text-align:left;vertical-align:top}
th{background:var(--panel2);color:var(--acc)}
tr:nth-child(even) td{background:rgba(255,255,255,.02)}
code{background:var(--chip);padding:1px 6px;border-radius:5px;font-size:.92em;color:#ffd9a0}
.formula{background:var(--panel2);border:1px dashed var(--acc);border-radius:10px;padding:12px 16px;margin:14px 0;text-align:center;font-size:1.1rem}
.worked{background:var(--panel2);border-left:4px solid var(--acc2);border-radius:0 10px 10px 0;padding:12px 16px;margin:14px 0}
.worked b{color:var(--acc2)}
/* Quiz */
#quiz .q{background:var(--panel2);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:14px 0}
#quiz .q .qnum{color:var(--acc);font-weight:700;margin-right:6px}
#quiz .opt{display:block;padding:9px 12px;margin:7px 0;border:1px solid var(--line);border-radius:9px;cursor:pointer;transition:.15s}
#quiz .opt:hover{background:var(--panel)}
#quiz .opt.sel{border-color:var(--acc2);background:rgba(122,162,255,.12)}
#quiz .opt.correct{border-color:var(--good);background:rgba(82,224,160,.18)}
#quiz .opt.wrong{border-color:var(--bad);background:rgba(255,107,129,.16)}
#quiz input[type=text]{width:100%;padding:9px 12px;border-radius:9px;border:1px solid var(--line);background:var(--panel);color:var(--ink);font-size:1rem}
.expl{margin-top:10px;padding:10px 12px;border-radius:9px;background:rgba(93,214,192,.08);border:1px solid rgba(93,214,192,.3);font-size:.92rem;display:none}
.expl.show{display:block}
.btnrow{display:flex;gap:12px;flex-wrap:wrap;margin:18px 0}
button{background:var(--acc);color:#06231d;border:none;padding:11px 20px;border-radius:10px;font-size:1rem;font-weight:700;cursor:pointer}
button.ghost{background:transparent;color:var(--acc);border:1px solid var(--acc)}
button:hover{filter:brightness(1.08)}
#score{font-size:1.3rem;font-weight:800;margin:10px 0;display:none}
#score.show{display:block}
.flash{cursor:pointer;perspective:1000px;height:118px;margin:10px 0}
.flash-inner{position:relative;width:100%;height:100%;transition:transform .5s;transform-style:preserve-3d}
.flash.flip .flash-inner{transform:rotateY(180deg)}
.flash-front,.flash-back{position:absolute;inset:0;backface-visibility:hidden;border-radius:12px;display:flex;align-items:center;justify-content:center;padding:14px;text-align:center;border:1px solid var(--line)}
.flash-front{background:var(--panel2);font-weight:600}
.flash-back{background:rgba(93,214,192,.12);transform:rotateY(180deg);color:var(--ink);font-size:.95rem}
footer{text-align:center;color:var(--muted);padding:30px;border-top:1px solid var(--line);font-size:.9rem}
.progress-wrap{position:fixed;top:0;left:0;height:4px;width:100%;background:transparent;z-index:50}
.progress-bar{height:100%;width:0;background:linear-gradient(90deg,var(--acc),var(--acc2))}
@media(max-width:880px){nav.toc{display:none}.layout{padding:0 12px}}
</style>
</head>
<body>
<div class="progress-wrap"><div class="progress-bar" id="pbar"></div></div>
<header class="hero">
  <h1>Chapter 7 — Structure &amp; Synthesis of Alkenes</h1>
  <p>Comprehensive mastery guide &middot; built from the original lecture deck (Dr. Nisreen Alhaj)</p>
  <p style="font-size:.9rem">Sections 7-1 through 7-18 &middot; <em>rearrangements excluded as requested</em></p>
  <div>
    <span class="badge">Full explanations</span>
    <span class="badge">Original figures &amp; mechanisms</span>
    <span class="badge">40-question interactive quiz</span>
    <span class="badge">Flashcards</span>
  </div>
</header>
<div class="layout">
<nav class="toc" id="toc"></nav>
<main>
__BODY__
</main>
</div>
<footer>
  Made for your exam prep &middot; All figures extracted from your CH7 deck &middot; Good luck! 💪
</footer>
<script>
// Build TOC from sections
const toc=document.getElementById('toc');
let tocHTML='<h3>Contents</h3>';
document.querySelectorAll('section.topic').forEach(s=>{
  const h=s.querySelector('h2');
  const t=h.getAttribute('data-short')||h.textContent;
  tocHTML+=`<a href="#${s.id}">${t}</a>`;
});
toc.innerHTML=tocHTML;
const links=[...toc.querySelectorAll('a')];
const secs=[...document.querySelectorAll('section.topic')];
// scroll spy + progress bar
const pbar=document.getElementById('pbar');
window.addEventListener('scroll',()=>{
  const sc=document.documentElement.scrollTop;
  const h=document.documentElement.scrollHeight-document.documentElement.clientHeight;
  pbar.style.width=(sc/h*100)+'%';
  let cur=secs[0]?.id;
  secs.forEach(s=>{if(s.getBoundingClientRect().top<160)cur=s.id;});
  links.forEach(a=>a.classList.toggle('active',a.getAttribute('href')==='#'+cur));
});
// Flashcards
document.querySelectorAll('.flash').forEach(f=>f.addEventListener('click',()=>f.classList.toggle('flip')));
</script>
<script>
__QUIZJS__
</script>
</body>
</html>"""


# ===========================================================================
# SECTIONS  — each is (id, full-title, short-toc-label, html_body)
# ===========================================================================
SECTIONS = []
def S(id, title, short, body):
    SECTIONS.append((id, title, short, body))

# ---- 7-1 Structure -------------------------------------------------------
S("structure", "7-1 &nbsp;Structure of Alkenes", "7-1 Structure", f"""
<p>An <b>alkene</b> is a hydrocarbon that contains at least one <b>carbon&ndash;carbon double bond
(C=C)</b>. Because it holds fewer hydrogens than the corresponding alkane, an alkene is called
<b>unsaturated</b>. The C=C is the <b>functional group</b> — the reactive heart of the molecule —
so almost everything in this chapter flows from understanding it.</p>

{img(36,"Ethylene (ethene), the simplest alkene — the C=C functional group.")}

<h3 class="sub">The double bond = one &sigma; bond + one &pi; bond</h3>
<ul>
<li>Each doubly-bonded carbon is <b>sp&sup2; hybridized</b>.</li>
<li>The three sp&sup2; orbitals lie in a plane <b>120&deg;</b> apart &rarr; <b>trigonal-planar</b> geometry.</li>
<li>The leftover, un-hybridized <b>p orbital</b> on each carbon overlaps <b>side-to-side</b> to form the <b>&pi; bond</b>. This sideways overlap is what locks the geometry (no free rotation).</li>
</ul>

{gallery([35,37],"Orbital picture of ethylene: sp&sup2; framework (&sigma;) plus the side-on p-orbital overlap that makes the &pi; bond.")}

<div class="callout key">A &pi; bond cannot rotate without breaking. That rigidity is the entire reason
<b>cis&ndash;trans (geometric) isomerism</b> exists (Section 7-5).</div>

<h3 class="sub">Why the double bond is shorter</h3>
<p>sp&sup2; orbitals carry <b>more <i>s</i>-character</b> than sp&sup3; orbitals, so the bonding electrons sit
closer to the nuclei. Add the extra &pi; overlap pulling the carbons together and the bond contracts:</p>
<table>
<tr><th>Bond</th><th>Hybridization</th><th>Length</th><th>Notes</th></tr>
<tr><td>C&ndash;C (alkane)</td><td>sp&sup3;</td><td>1.54 &Aring;</td><td>single, freely rotating</td></tr>
<tr><td>C=C (alkene)</td><td>sp&sup2;</td><td><b>1.33 &Aring;</b></td><td>shorter, stronger, rigid</td></tr>
</table>
<div class="callout tip">If a question asks &ldquo;which is shorter/stronger,&rdquo; remember: more <i>s</i>-character +
&pi; overlap &rarr; <b>shorter &amp; stronger</b> bond, but the &pi; component is weaker than a &sigma;, which is
why alkenes are reactive toward addition.</div>
""")

# ---- 7-2 Elements of Unsaturation ---------------------------------------
S("unsat", "7-2 &nbsp;Elements of Unsaturation (Degree of Unsaturation)", "7-2 Unsaturation", f"""
<p>Four names, <b>one idea</b>: Elements of Unsaturation = Degree of Unsaturation = Unsaturation Number =
<b>Index of Hydrogen Deficiency (IHD)</b>. Each &ldquo;element&rdquo; tells you the molecule is missing
<b>two hydrogens</b> relative to the fully saturated formula.</p>

{gallery([44,45,46],"A double bond OR a ring each remove two hydrogens — both count as one element of unsaturation.")}

<ul>
<li><b>Saturated</b> = holds the maximum number of H (reacts with no more H&#8322;).</li>
<li>1 double bond = <b>1</b> element &nbsp;&bull;&nbsp; 1 ring = <b>1</b> element &nbsp;&bull;&nbsp; 1 triple bond = <b>2</b> elements.</li>
</ul>

<h4 class="sub">The formula</h4>
<div class="formula">Elements of Unsaturation = <b>[ (2C + 2) &minus; H ] / 2</b></div>
<p>where the saturated reference for hydrocarbons is <code>C&#8345;H&#8322;&#8345;&#8330;&#8322;</code>. In words:
<i>find the max possible H, see how many are missing, and halve it.</i></p>

<div class="callout warnbox">This count <b>cannot tell you</b> whether the unsaturation comes from a
<b>double bond</b> or a <b>ring</b> — it only gives the total. You need the structure to know which.</div>

<h3 class="sub">Dealing with heteroatoms (atoms that aren&rsquo;t C or H)</h3>
{gallery([64,75,76,83],"Halogens count as H; oxygen is ignored; nitrogen counts as half a carbon.")}
<table>
<tr><th>Atom</th><th>Rule</th><th>Why</th></tr>
<tr><td><b>Halogen</b> (F, Cl, Br, I)</td><td>Count as <b>hydrogen</b></td><td>monovalent — it just replaces an H</td></tr>
<tr><td><b>Oxygen</b> (O)</td><td><b>Ignore it</b></td><td>divalent — inserts into a chain/bond without changing C or H counts</td></tr>
<tr><td><b>Nitrogen</b> (N)</td><td>Count as <b>&frac12; carbon</b></td><td>trivalent — adds only 1 H, vs 2 H per added C</td></tr>
</table>
<div class="callout mnem">&ldquo;<b>Halogens act like H, Oxygen is invisible, Nitrogen is half a Carbon.</b>&rdquo;</div>

<h3 class="sub">Worked examples</h3>
<div class="worked"><b>C&#8324;H&#8325;Br&#8323;:</b> treat the 3 Br as 3 H &rarr; effectively C&#8324;H&#8328;.
Saturated C&#8324; would be C&#8324;H&#8321;&#8320;. Missing 2 H &rarr; <b>1 element of unsaturation</b>.</div>
<div class="worked"><b>The slide&rsquo;s nitrogen example:</b> a compound counted as C&#8324;&#46;&#8325;H&#8321;&#8321;
(N treated as &frac12; C). Max H = 2(4.5)+2 = 11. The compound shown leads to 11 &minus; 7 = 4 missing,
4 / 2 = <b>2 elements of unsaturation</b>.</div>
{gallery([90,91,97],"Putting it together: combining the halogen / oxygen / nitrogen rules in one calculation.")}
<div class="callout tip">Exam shortcut for a quick sanity check: an aromatic ring (benzene) is always
<b>4</b> (3 C=C + 1 ring); a C&equiv;C or C&equiv;N is <b>2</b>; each C=O or C=C is <b>1</b>.</div>
""")

# ---- 7-3 Nomenclature ----------------------------------------------------
S("nomen", "7-3 &nbsp;Nomenclature of Alkenes", "7-3 Naming", f"""
<p>IUPAC naming of an alkene follows the alkane rules with a few double-bond-specific twists.</p>
<ol>
<li><b>Pick the longest chain that <u>contains</u> the C=C.</b> The double bond must be in the parent chain even if a longer chain exists elsewhere.</li>
<li>Change the alkane suffix <code>-ane</code> &rarr; <b><code>-ene</code></b>.</li>
<li><b>Number from the end nearest the double bond</b> so the C=C gets the <b>lowest locant</b> possible.</li>
<li>In a <b>ring</b>, the double bond is <i>assumed</i> to be between <b>C1 and C2</b> — no number needed for a single ring double bond.</li>
</ol>
{gallery([103,104,105],"Choosing and numbering the parent chain so the double bond gets the lowest locant.")}

<h3 class="sub">More than one double bond</h3>
<table>
<tr><th># of C=C</th><th>Suffix</th></tr>
<tr><td>2</td><td>-a<b>diene</b></td></tr>
<tr><td>3</td><td>-a<b>triene</b></td></tr>
<tr><td>4</td><td>-a<b>tetraene</b></td></tr>
</table>
<p>Use a <b>locant for every</b> double bond, and the prefixes <b>di-, tri-, tetra-</b> before
<code>-ene</code>. In rings, give the double bonds the lowest set of numbers.</p>
{gallery([109,112],"Naming dienes / trienes: number every double bond and use di-, tri-, tetra-.")}

<h3 class="sub">Alkenes as substituents — &ldquo;alkenyl&rdquo; groups</h3>
<p>When the C=C sits on a branch, the group is named as a substituent (an <b>alkenyl</b> group):</p>
<table>
<tr><th>Common name</th><th>Structure</th></tr>
<tr><td><b>Vinyl</b> (ethenyl)</td><td>CH&#8322;=CH&ndash;</td></tr>
<tr><td><b>Allyl</b> (2-propenyl)</td><td>CH&#8322;=CH&ndash;CH&#8322;&ndash;</td></tr>
<tr><td><b>Methylene</b></td><td>=CH&#8322; (or a bridging &ndash;CH&#8322;&ndash;)</td></tr>
<tr><td><b>Phenyl</b></td><td>C&#8326;H&#8325;&ndash; (benzene ring as substituent)</td></tr>
</table>
{gallery([118,119],"The common alkenyl substituents: vinyl, allyl, methylene, phenyl.")}
<div class="callout tip">Vinyl vs allyl trips people up: <b>vinyl</b> = the carbon <i>is</i> part of the C=C;
<b>allyl</b> = a CH&#8322; <i>next to</i> a C=C. Allyl &rArr; &ldquo;<b>a</b>llyl has an <b>a</b>djacent CH&#8322;.&rdquo;</div>
""")

# ---- 7-5 Cis/Trans & E/Z -------------------------------------------------
S("cistrans", "7-5 &nbsp;Cis&ndash;Trans &amp; E&ndash;Z Nomenclature", "7-5 Cis/Trans, E/Z", f"""
<p>Because the &pi; bond blocks rotation, the two ends of a C=C are locked &mdash; giving
<b>geometric (cis&ndash;trans) isomers</b>. A double bond that can show this is called <b>stereogenic</b>.</p>

<h3 class="sub">The cis&ndash;trans system</h3>
<ul>
<li><b>cis</b> = the two like / main groups are on the <b>same side</b> of the double bond.</li>
<li><b>trans</b> = the two like / main groups are on <b>opposite sides</b>.</li>
</ul>
{gallery([131,132],"cis vs trans: same side vs opposite sides of the C=C.")}
<div class="callout warnbox">The simple cis/trans labels break down when each carbon carries <b>two different</b>
groups (nothing obvious is &ldquo;the same&rdquo;). That&rsquo;s why we need the rigorous E&ndash;Z system.</div>

<h3 class="sub">The E&ndash;Z system (uses Cahn&ndash;Ingold&ndash;Prelog priorities)</h3>
<ol>
<li>On <b>each</b> double-bond carbon, rank its two groups by <b>CIP priority</b> (higher atomic number wins; if tied, move to the next atoms outward).</li>
<li>Look at where the <b>two higher-priority</b> groups end up:</li>
</ol>
<table>
<tr><th>Label</th><th>German</th><th>Meaning</th><th>High-priority groups are&hellip;</th></tr>
<tr><td><b>Z</b></td><td><i>zusammen</i></td><td>together</td><td>on the <b>same side</b></td></tr>
<tr><td><b>E</b></td><td><i>entgegen</i></td><td>opposite</td><td>on <b>opposite sides</b></td></tr>
</table>
{gallery([138,139,140,141,142,143],"Assigning CIP priorities on each carbon, then deciding E vs Z.")}
<div class="callout mnem"><b>&ldquo;Z = same Zide.&rdquo;</b> If the two high-priority groups are on the same side, it&rsquo;s Z.</div>
{gallery([150,151,152],"Worked E/Z assignments from the deck.")}
{img(160,"Summary of cis/trans and E/Z relationships.")}
""")

# ---- 7-7 Physical Properties --------------------------------------------
S("physical", "7-7 &nbsp;Physical Properties of Alkenes", "7-7 Physical Props", f"""
<h3 class="sub">A. Boiling points &amp; densities</h3>
<p>Alkenes behave a lot like the matching alkanes:</p>
<ul>
<li>but-1-ene, <i>cis</i>-but-2-ene, <i>trans</i>-but-2-ene and <i>n</i>-butane all boil near <b>0&nbsp;&deg;C</b>.</li>
<li><b>Boiling point rises smoothly with molecular weight</b> (bigger &rarr; more London dispersion forces).</li>
<li><b>More branching &rarr; more volatile &rarr; lower boiling point</b> (branched molecules have less surface contact).</li>
<li><b>Densities &asymp; 0.6&ndash;0.7 g/cm&sup3;</b> &mdash; lighter than water, so they float and are insoluble in water.</li>
</ul>
{img(166,"Boiling points of C4 isomers cluster near 0 °C; density ≈ 0.6–0.7 g/cm³.")}

<h3 class="sub">B. Polarity</h3>
<ul>
<li>Alkyl groups donate a little electron density to the sp&sup2; carbons, giving a small bond dipole.</li>
<li>In a <b>cis</b> alkene the two dipoles partly <b>add up</b> &rarr; a <b>net dipole</b> &rarr; slightly polar.</li>
<li>In a <b>trans</b> alkene the dipoles point oppositely and <b>cancel</b> &rarr; little/no net dipole.</li>
</ul>
<div class="callout key">Cis alkenes have the <b>larger dipole moment</b>, so the <b>cis isomer boils higher</b> than the trans.
(Trans, however, is usually the more <i>stable</i> isomer — don&rsquo;t confuse stability with boiling point.)</div>
{gallery([183,184,185],"cis dipoles reinforce → polar, higher b.p.; trans dipoles cancel → nonpolar.")}
<p>Overall alkenes are <b>relatively nonpolar</b> and <b>insoluble in water</b>.</p>
""")

# ---- 7-8 Stability -------------------------------------------------------
S("stability", "7-8 &nbsp;Stability of Alkenes", "7-8 Stability", f"""
<h3 class="sub">A. Heats of hydrogenation — how we measure stability</h3>
<p>To compare two alkenes we convert each to the <b>same product</b> (the alkane) and measure the heat
released. Adding H&#8322; across the C=C (<b>hydrogenation</b>) is exothermic; the heat given off is the
<b>heat of hydrogenation</b>.</p>
{img(191,"Heats of hydrogenation: the more stable alkene starts lower, so it releases LESS heat.")}
<div class="callout key">The <b>more stable</b> alkene sits at <b>lower energy</b>, so it releases <b>less heat</b> on
hydrogenation &rarr; a <b>lower heat of hydrogenation</b> means a <b>more stable</b> alkene.</div>
<div class="worked"><b>cis vs trans-2-butene:</b> they hydrogenate to the same butane.
<i>trans</i> releases 115.5 and <i>cis</i> releases ~120 kJ/mol; the slide gives the gap as
<b>&asymp; 11.3 kJ/mol (2.7 kcal/mol)</b> in favor of the more-substituted/trans arrangement &mdash;
i.e. <i>trans</i>-2-butene is the more stable isomer.</div>
{img(197,"More substituted double bonds have lower heats of hydrogenation (more stable).")}

<h3 class="sub">B. Substitution effects — why &ldquo;more substituted = more stable&rdquo;</h3>
<p>The most stable double bonds carry the <b>most alkyl groups</b>. Two reasons:</p>
<ol>
<li><b>Electronic (hyperconjugation):</b> alkyl groups are mildly <b>electron-donating</b> and feed electron density into the &pi; system, stabilizing it.</li>
<li><b>Steric:</b> bulky groups want to be <b>far apart</b>. An alkane separates them by ~109.5&deg;; a double bond opens that to ~<b>120&deg;</b>, relieving strain — and the most substituted alkene spreads the bulk best.</li>
</ol>
{gallery([201,204],"Alkyl groups donate electron density and prefer the wider 120° separation of a C=C.")}
<div class="formula">Stability: tetra- &gt; tri- &gt; di- &gt; mono-substituted &gt; ethylene</div>
{gallery([210,211,212],"trans separates the alkyl groups farther than cis → trans is generally more stable.")}
<div class="callout key">Between geometric isomers, <b>trans is usually more stable than cis</b> because its alkyl
groups are farther apart (less steric strain).</div>
{img(217,"Comparative stabilities scale.")}

<h3 class="sub">D. Stability of cycloalkenes &amp; ring strain</h3>
<ul>
<li>A ring only changes the stability picture if it introduces <b>ring strain</b> — from a <b>small ring</b> or a <b>trans double bond inside a ring</b>.</li>
<li>Rings that are <b>5-membered or larger</b> hold a (cis) double bond comfortably and react like normal chain alkenes.</li>
<li>In <b>small</b> cycloalkenes the <b>cis isomer is more stable</b> (trans would be hugely strained).</li>
<li>A ring needs <b>&ge; 8 carbons</b> to support a <b>stable trans double bond</b> (<i>trans</i>-cyclooctene is the smallest isolable one).</li>
<li>For <b>cyclodecene and larger</b>, the trans double bond is <b>almost as stable as the cis</b>.</li>
</ul>
{gallery([225,231,232],"Ring size vs the ability to hold a (cis or trans) double bond.")}

<h3 class="sub">E. Bredt&rsquo;s Rule</h3>
<div class="callout key"><b>Bredt&rsquo;s Rule:</b> a <b>bridged bicyclic</b> compound cannot have a double bond at a
<b>bridgehead</b> carbon (unless the rings are large). The bridgehead can&rsquo;t reach the planar,
120&deg; sp&sup2; geometry a C=C needs, so such an arrangement is <b>too strained / not stable</b>.</div>
{gallery([238,239,240],"A bridgehead double bond cannot achieve planarity → a Bredt's-rule violation.")}
{gallery([246,247],"Stable vs unstable (rule-violating) bridgehead arrangements.")}

<h3 class="sub">F. Conjugated vs isolated double bonds</h3>
<table>
<tr><th>Type</th><th>Arrangement</th><th>Interaction</th><th>Stability</th></tr>
<tr><td><b>Conjugated</b></td><td>C=C&ndash;C=C (separated by <b>exactly one</b> single bond)</td><td>&pi; systems overlap &amp; interact</td><td><b>extra-stable</b></td></tr>
<tr><td><b>Isolated</b></td><td>separated by <b>two or more</b> single bonds</td><td>little interaction</td><td>normal</td></tr>
</table>
{gallery([253,254,255,256],"Conjugated double bonds (one single bond apart) interact and gain stability.")}
{img(262,"Conjugation lowers the energy of the π system.")}
<div class="callout mnem">&ldquo;<b>Conjugated = connected.</b>&rdquo; One single bond between two C=C lets the &pi; clouds talk to each
other, and that delocalization is stabilizing.</div>
""")

# ---- 7-9 Formation / elimination overview --------------------------------
S("formation", "7-9 &nbsp;Formation of Alkenes by Elimination", "7-9 Formation", f"""
<p>The major way to <b>make</b> alkenes is <b>elimination</b>: two atoms/groups leave from adjacent carbons
and a <b>new &pi; bond</b> forms.</p>
{img(268,"The four elimination routes to alkenes.")}
<table>
<tr><th>Method</th><th>What leaves</th><th>Conditions</th></tr>
<tr><td><b>E2 dehydrohalogenation</b></td><td>H and X (as HX)</td><td>strong base</td></tr>
<tr><td><b>E1 dehydrohalogenation</b></td><td>H and X (as HX)</td><td>weak base / ionizing solvent</td></tr>
<tr><td><b>Dehalogenation</b> of vicinal dibromides</td><td>two X (as X&#8322;)</td><td>e.g. Zn or I&#8315;</td></tr>
<tr><td><b>Dehydration</b> of alcohols</td><td>H and OH (as H&#8322;O)</td><td>acid catalyst, heat</td></tr>
</table>
<div class="callout key"><b>Dehydrohalogenation</b> = elimination of a <b>proton (H&#8314;) + a halide (X&#8315;)</b>
from an alkyl halide to give an alkene. It can go by either the E1 or E2 pathway.</div>
{gallery([276,277],"Loss of two groups from adjacent carbons creates the new π bond.")}
""")

# ---- 7-9A Zaitsev --------------------------------------------------------
S("zaitsev", "7-9A &nbsp;Zaitsev&rsquo;s Rule (Regiochemistry)", "7-9A Zaitsev", f"""
<div class="callout key"><b>Zaitsev&rsquo;s Rule:</b> when more than one alkene can form, the <b>more highly
substituted (more stable) alkene is the major product.</b></div>
<p>This follows directly from Section 7-8: more substituted = more stable, so the transition state leading
to it is lower in energy. The Zaitsev product is also called the <b>more-substituted</b> product.</p>
{gallery([281,284,285],"With several β-hydrogens available, removing the one that gives the more substituted alkene wins.")}
{gallery([292,293],"Zaitsev orientation: the more substituted alkene predominates.")}
<div class="callout tip">Keep this paired with its opposite (Section 7-12): a normal base &rarr; <b>Zaitsev</b>;
a <b>bulky</b> base &rarr; <b>Hofmann</b> (least substituted).</div>
""")

# ---- 7-10 E1 -------------------------------------------------------------
S("e1", "7-10 &nbsp;The E1 Reaction (Unimolecular Elimination)", "7-10 E1", f"""
<p>E1 = <b>E</b>limination, <b>1</b>st order. The rate depends only on the substrate:
<code>rate = k[substrate]</code>.</p>
<h3 class="sub">Mechanism (two steps)</h3>
<ol>
<li><b>Slow / rate-determining:</b> the leaving group departs, forming a <b>carbocation</b>.</li>
<li><b>Fast:</b> a base plucks a proton off a carbon <b>adjacent</b> (&beta;) to the C&#8314;; that carbon
<b>rehybridizes to sp&sup2;</b> and the electrons flow into the <b>new &pi; bond</b>.</li>
</ol>
{gallery([299,300,301],"E1: ionize to a carbocation, then lose a β-proton to form the π bond.")}
<ul>
<li>Favored by: <b>3&deg; &gt; 2&deg;</b> substrates, <b>weak bases</b>, <b>good ionizing (polar protic) solvents</b>, heat.</li>
<li>Regiochemistry follows <b>Zaitsev</b> (most substituted alkene major).</li>
</ul>

<h3 class="sub">A. Competition between E1 and S<sub>N</sub>1</h3>
<div class="callout key">Any time a <b>carbocation</b> forms it can go <b>two ways</b> — substitution (S<sub>N</sub>1) or
elimination (E1) — so E1 <b>almost always competes with S<sub>N</sub>1</b> and you get <b>mixtures</b>.</div>
{gallery([307,308],"The same carbocation partitions between SN1 (substitution) and E1 (elimination).")}
<p><b>Solvolysis</b> (&ldquo;solvo&rdquo; = solvent, &ldquo;lysis&rdquo; = cleavage) is the special case where the
<b>solvent itself</b> acts as the weak base/nucleophile and reacts with the substrate.</p>
{gallery([314,315,316,322],"Because both pathways share the carbocation, product mixtures are typical of E1/SN1 systems.")}
""")

# ---- 7-11 E2 -------------------------------------------------------------
S("e2", "7-11 &nbsp;The E2 Reaction (Bimolecular Elimination)", "7-11 E2", f"""
<p>E2 = <b>E</b>limination, <b>2</b>nd order: <code>rate = k[substrate][base]</code>. It needs a
<b>strong base</b>.</p>
<h3 class="sub">Mechanism (one concerted step)</h3>
<p>Everything happens <b>at once</b>: the base grabs the &beta;-proton, the new &pi; bond forms, and the
leaving group leaves — all in a <b>single step</b> with no intermediate.</p>
{img(328,"Concerted E2: proton removal, π-bond formation, and loss of the leaving group happen together.")}
<ul>
<li>Reactivity / product distribution reflects the <b>greater stability of more-substituted double bonds</b> &rarr; normally <b>Zaitsev</b>.</li>
<li>On a <b>tertiary</b> substrate, <b>no substitution</b> is seen: the S<sub>N</sub>2 path is <b>blocked</b> because the 3&deg; carbon is <b>too hindered</b> for backside attack — so a strong base on a 3&deg; halide gives clean E2.</li>
</ul>
{gallery([335,336,337],"E2 on a hindered substrate: SN2 is blocked, elimination dominates.")}
{gallery([343,344],"Mixtures can still arise when several different β-hydrogens are available.")}
""")

# ---- 7-12 Bulky base / Hofmann ------------------------------------------
S("hofmann", "7-12 &nbsp;Bulky Bases &amp; Hofmann Orientation", "7-12 Hofmann", f"""
<p>You can <b>steer</b> an E2 toward the <i>less</i> substituted alkene by choosing the base.</p>
<ol>
<li>If a substrate is <b>prone to substitution</b>, switch to a <b>bulky base</b> to suppress S<sub>N</sub>2 and favor elimination.</li>
<li>Bulky bases (e.g. potassium <i>tert</i>-butoxide, KOtBu) drive eliminations that <b>break Zaitsev&rsquo;s rule</b> and give the <b>Hofmann product</b>.</li>
</ol>
{gallery([350,351],"A bulky base can't reach the crowded internal proton, so it takes a less-hindered one.")}
<h3 class="sub">Why the Hofmann product forms</h3>
<p><b>Steric hindrance</b> stops the big base from reaching the proton that would give the most-substituted
(Zaitsev) alkene. Instead it removes a <b>less hindered</b> proton — usually the one that gives the
<b>least substituted</b> alkene, the <b>Hofmann product</b>.</p>
{img(357,"Bulky base abstracts the accessible proton → least-substituted (Hofmann) alkene.")}
<div class="callout key">Small/unhindered base &rarr; <b>Zaitsev</b> (more substituted). &nbsp;&nbsp;Bulky base &rarr;
<b>Hofmann</b> (less substituted).</div>
<div class="callout mnem"><b>&ldquo;Big Base &rarr; Baby alkene (Hofmann).&rdquo;</b> A bulky base makes the smaller, less-substituted alkene.</div>
{gallery([361,367],"Comparing Zaitsev vs Hofmann outcomes for the same substrate.")}
""")

# ---- 7-13 Dehydration (rearrangement excluded) ---------------------------
S("dehydration", "7-13 &nbsp;Synthesis by Dehydration of Alcohols", "7-13 Dehydration", f"""
<p>Heating an alcohol with acid eliminates water (<b>dehydration</b>) to give an alkene.</p>
{img(373,"Acid-catalyzed dehydration: an alcohol loses H2O to form an alkene.")}
<ul>
<li><b>Catalysts:</b> concentrated <b>H&#8322;SO&#8324;</b> or <b>H&#8323;PO&#8324;</b>.</li>
<li><b>Le Chatelier trick:</b> distill the <b>low-boiling alkene out as it forms</b> to pull the equilibrium forward and boost the yield.</li>
<li>Goes by an <b>E1 mechanism</b> (protonate OH &rarr; lose water to a carbocation &rarr; lose a &beta;-proton).</li>
<li><b>Obeys Zaitsev&rsquo;s rule</b> — the more substituted alkene is the major product.</li>
</ul>
<h3 class="sub">Key mechanism (E1 dehydration)</h3>
<ol>
<li><b>Protonation:</b> acid protonates the &ndash;OH, turning a poor leaving group into <b>&ndash;OH&#8322;&#8314;</b> (water — an excellent leaving group).</li>
<li><b>Ionization:</b> water leaves &rarr; <b>carbocation</b> (rate-determining).</li>
<li><b>Deprotonation:</b> a base (often the solvent / HSO&#8324;&#8315;) removes a &beta;-proton &rarr; the <b>&pi; bond</b> forms and the catalyst is regenerated.</li>
</ol>
{gallery([379,380,381,382],"The three-step acid-catalyzed (E1) dehydration mechanism.")}
{gallery([389,395,396,397],"Worked dehydration examples following Zaitsev orientation.")}
{gallery([401,402],"Additional dehydration practice from the deck.")}
<div class="callout warnbox">Because dehydration runs through a free carbocation, <b>carbocation rearrangements</b> are
common in the full treatment. <i>(Per your request, the rearrangement details are intentionally left out
of this guide.)</i></div>
""")

# ---- 7-14 Stereochemistry of E2 -----------------------------------------
S("e2stereo", "7-14 &nbsp;Stereochemistry of the E2 Reaction", "7-14 E2 Stereo", f"""
<p>E2 has a strict <b>geometry requirement</b>: the &beta;-H and the leaving group must lie in the
<b>same plane</b> (coplanar) so their orbitals can line up as the &pi; bond forms.</p>
{img(408,"E2 needs the H and leaving group coplanar — anti (180°) is strongly preferred.")}
<table>
<tr><th>Geometry</th><th>Dihedral (H&ndash;C&ndash;C&ndash;LG)</th><th>Notes</th></tr>
<tr><td><b>Anti-coplanar</b> (anti-periplanar)</td><td><b>180&deg;</b></td><td><b>Strongly preferred</b> — staggered, lowest-energy transition state</td></tr>
<tr><td><b>Syn-coplanar</b> (syn-periplanar)</td><td><b>0&deg;</b></td><td>Possible but higher energy (eclipsed); only when the ring/rigid system forbids anti</td></tr>
</table>
{gallery([414,415,416,417,418,419,420,421],"Newman-projection analysis of anti- vs syn-coplanar E2 eliminations.")}
<div class="callout key">Default assumption on an exam: <b>E2 goes anti-periplanar.</b> This controls which &beta;-H is
removed and therefore the <b>stereochemistry of the alkene</b> produced.</div>
""")

# ---- 7-18 Comparison -----------------------------------------------------
S("compare", "7-18 &nbsp;E1 vs E2 &mdash; and Substitution vs Elimination", "7-18 Compare All", f"""
<p>The big-picture decision table tying together everything (and S<sub>N</sub>1 / S<sub>N</sub>2 from before):</p>
<table>
<tr><th>Reagent</th><th>Order</th><th>Substitution</th><th>Elimination</th></tr>
<tr><td><b>Strong base / nucleophile</b></td><td>bimolecular</td><td>S<sub>N</sub>2</td><td><b>E2</b></td></tr>
<tr><td><b>Weak base / nucleophile</b></td><td>unimolecular</td><td>S<sub>N</sub>1</td><td><b>E1</b></td></tr>
</table>
{gallery([425,429],"Strong base/nucleophile → bimolecular (SN2 vs E2).")}
{gallery([433,438,439],"Weak base/nucleophile → unimolecular (SN1 vs E1).")}
<div class="callout key">Because S<sub>N</sub>1 and E1 share a carbocation, the <b>unimolecular</b> reactions give
<b>mixtures</b> you can&rsquo;t control well — which is exactly why <b>unimolecular reactions are rarely used
for synthesis</b>.</div>
{gallery([443,447,448],"Unimolecular reactions give poorly controlled mixtures.")}

<h3 class="sub">E1 vs E2 at a glance</h3>
<table>
<tr><th>Feature</th><th>E1</th><th>E2</th></tr>
<tr><td>Steps</td><td>2 (carbocation intermediate)</td><td>1 (concerted)</td></tr>
<tr><td>Rate law</td><td>k[substrate]</td><td>k[substrate][base]</td></tr>
<tr><td>Base</td><td>weak</td><td>strong</td></tr>
<tr><td>Substrate</td><td>3&deg; &gt; 2&deg;</td><td>3&deg; &gt; 2&deg; &gt; 1&deg;</td></tr>
<tr><td>Stereochem</td><td>not specific</td><td><b>anti-periplanar</b></td></tr>
<tr><td>Regiochem</td><td>Zaitsev</td><td>Zaitsev (Hofmann with bulky base)</td></tr>
<tr><td>Competes with</td><td>S<sub>N</sub>1</td><td>S<sub>N</sub>2</td></tr>
<tr><td>Rearrangements</td><td>possible</td><td>none</td></tr>
</table>
{gallery([452,453,457],"Final summary comparison of the elimination pathways.")}
""")


# ===========================================================================
# FLASHCARDS  (quick-recall pairs)
# ===========================================================================
FLASHCARDS = [
    ("Hybridization & geometry of a C=C carbon?", "sp&sup2;, trigonal planar, ~120&deg; bond angles."),
    ("C=C bond length vs C&ndash;C?", "1.33 &Aring; (alkene) vs 1.54 &Aring; (alkane) — shorter & stronger."),
    ("Formula for elements of unsaturation?", "(2C + 2 &minus; H) / 2  (treat halogen as H, ignore O, N = &frac12; C)."),
    ("Heteroatom rules for IHD?", "Halogen &rarr; count as H &nbsp;|&nbsp; Oxygen &rarr; ignore &nbsp;|&nbsp; Nitrogen &rarr; &frac12; carbon."),
    ("Z vs E?", "Z = high-priority groups on the SAME side (zusammen). E = opposite sides (entgegen)."),
    ("Which boils higher, cis or trans alkene?", "cis — it has the larger dipole moment."),
    ("Which is more stable, cis or trans?", "Usually trans — alkyl groups are farther apart (less strain)."),
    ("Heat of hydrogenation vs stability?", "Lower heat of hydrogenation = MORE stable alkene."),
    ("Most stable degree of substitution?", "Tetra- > tri- > di- > mono-substituted > ethylene."),
    ("Smallest ring with a stable trans C=C?", "8 carbons (trans-cyclooctene)."),
    ("Bredt's rule?", "No double bond at a bridgehead of a (small) bridged bicyclic system."),
    ("Conjugated vs isolated double bonds?", "Conjugated = one single bond apart (interact, extra stable); isolated = 2+ single bonds apart."),
    ("Zaitsev's rule?", "The more-substituted (more stable) alkene is the major elimination product."),
    ("E1 rate law & steps?", "rate = k[substrate]; 2 steps via a carbocation."),
    ("E2 rate law & steps?", "rate = k[substrate][base]; 1 concerted step; needs a strong base."),
    ("Bulky base gives which product?", "Hofmann — the LEAST substituted alkene."),
    ("Required E2 geometry?", "Anti-periplanar (H and leaving group coplanar at 180&deg;)."),
    ("Dehydration catalysts & mechanism?", "Conc. H&#8322;SO&#8324; / H&#8323;PO&#8324;; E1 mechanism; obeys Zaitsev."),
    ("Why no SN2 on a 3&deg; halide?", "Too sterically hindered for backside attack — so a strong base gives clean E2."),
    ("What is solvolysis?", "The solvent itself acts as the weak base/nucleophile (solvo = solvent, lysis = cleavage)."),
]

# ===========================================================================
# QUIZ  — 40 questions.  mc: (stem, [options], correct_index, explanation)
#                        fill: (stem, [accepted...], explanation)
# ===========================================================================
MC = "mc"; FILL = "fill"
QUIZ = [
 (MC,"The carbons of a C=C double bond are:",
   ["sp&sup3;, tetrahedral","sp&sup2;, trigonal planar","sp, linear","sp&sup3;d, see-saw"],1,
   "Double-bond carbons are sp&sup2; hybridized and trigonal planar (~120&deg;)."),
 (MC,"Approximate length of a C=C bond in an alkene:",
   ["1.54 &Aring;","1.10 &Aring;","1.33 &Aring;","1.20 &Aring;"],2,
   "C=C &asymp; 1.33 &Aring;, shorter than the 1.54 &Aring; C&ndash;C single bond."),
 (MC,"sp&sup2; orbitals differ from sp&sup3; orbitals in that they have:",
   ["more p-character","more s-character","no s-character","identical character"],1,
   "More s-character pulls electrons closer, helping shorten/strengthen the bond."),
 (MC,"How many elements of unsaturation are in C&#8325;H&#8328;?",
   ["0","1","2","3"],2,
   "(2&middot;5+2&minus;8)/2 = (12&minus;8)/2 = 2."),
 (MC,"When counting unsaturation, a nitrogen atom is treated as:",
   ["a hydrogen","ignored","half a carbon","a full carbon"],2,
   "N is trivalent, so it counts as &frac12; a carbon."),
 (MC,"When counting unsaturation, oxygen is:",
   ["counted as carbon","ignored","counted as hydrogen","counted as half a carbon"],1,
   "Divalent O slots in without changing C or H counts — ignore it."),
 (MC,"A halogen atom, for unsaturation counting, is treated as:",
   ["half a carbon","a carbon","a hydrogen","ignored"],2,
   "Monovalent halogens simply replace an H, so count them as H."),
 (MC,"Benzene (C&#8326;H&#8326;) has how many elements of unsaturation?",
   ["2","3","4","6"],2,
   "(2&middot;6+2&minus;6)/2 = 4 — three C=C plus one ring."),
 (MC,"In naming, the parent chain must:",
   ["be the longest chain in the molecule","contain the C=C even if not the longest","avoid the double bond","always be a ring"],1,
   "The chosen chain must include the double bond, then be as long as possible."),
 (MC,"The double bond is numbered so that it gets:",
   ["the highest locant","an even locant","the lowest locant","locant 2 always"],2,
   "Number from the end nearest the C=C to give the lowest locant."),
 (MC,"In a ring with one double bond, the double bond is assumed between:",
   ["C1 and C2","C2 and C3","the two most substituted carbons","C1 and C3"],0,
   "Ring double bonds are taken as C1&ndash;C2 (no locant needed)."),
 (MC,"The CH&#8322;=CH&ndash;CH&#8322;&ndash; substituent is called:",
   ["vinyl","allyl","methylene","phenyl"],1,
   "Allyl = a CH&#8322; adjacent to a C=C."),
 (MC,"The CH&#8322;=CH&ndash; substituent is called:",
   ["allyl","vinyl","phenyl","methylene"],1,
   "Vinyl (ethenyl) = the carbon is part of the C=C itself."),
 (MC,"A double bond capable of cis&ndash;trans isomerism is called:",
   ["chiral","stereogenic","racemic","meso"],1,
   "Such a double bond is termed stereogenic."),
 (MC,"In the E&ndash;Z system, Z means the two higher-priority groups are:",
   ["on opposite sides","on the same side","always the larger groups","trans"],1,
   "Z (zusammen) = high-priority groups on the same side."),
 (MC,"E/Z priorities are assigned using:",
   ["Markovnikov's rule","the Zaitsev rule","Cahn&ndash;Ingold&ndash;Prelog rules","Hund's rule"],2,
   "CIP rules rank groups by atomic number."),
 (MC,"Which boils at a HIGHER temperature?",
   ["trans-2-butene","cis-2-butene","they are equal","neither is polar"],1,
   "cis has the larger dipole moment, so it boils higher."),
 (MC,"Increased branching in alkenes causes:",
   ["higher boiling point","lower boiling point","higher density","no change"],1,
   "More branching &rarr; more volatile &rarr; lower boiling point."),
 (MC,"Typical density range of alkenes:",
   ["0.6&ndash;0.7 g/cm&sup3;","1.0 g/cm&sup3;","1.5&ndash;1.6 g/cm&sup3;","2.0 g/cm&sup3;"],0,
   "About 0.6&ndash;0.7 g/cm&sup3; — they float on water."),
 (MC,"A more stable alkene has a ______ heat of hydrogenation:",
   ["higher","lower","zero","negative infinite"],1,
   "Starting lower in energy, it releases less heat &rarr; lower heat of hydrogenation."),
 (MC,"The most stable alkene is generally:",
   ["ethylene","monosubstituted","disubstituted","tetrasubstituted"],3,
   "More alkyl substitution = more stable; tetrasubstituted is most stable."),
 (MC,"Two reasons more-substituted alkenes are more stable:",
   ["resonance and aromaticity","hyperconjugation (electron donation) and reduced steric strain","hydrogen bonding and dipoles","ring strain and angle strain"],1,
   "Alkyl groups donate electron density (hyperconjugation) and the 120&deg; geometry spreads bulk apart."),
 (MC,"Between geometric isomers, the more stable one is usually:",
   ["cis","trans","they're always equal","depends only on MW"],1,
   "trans keeps alkyl groups farther apart (less steric strain)."),
 (MC,"Smallest ring that can hold a STABLE trans double bond:",
   ["3 carbons","5 carbons","6 carbons","8 carbons"],3,
   "trans-Cyclooctene (8 C) is the smallest stable trans-cycloalkene."),
 (MC,"In small cycloalkenes, the more stable isomer is:",
   ["trans","cis","neither exists","both equal"],1,
   "Small rings can't accommodate a strained trans C=C, so cis is more stable."),
 (MC,"Bredt's rule forbids a double bond:",
   ["in any ring","at a bridgehead of a bridged bicyclic system","that is conjugated","that is cis"],1,
   "A bridgehead can't reach planar sp&sup2; geometry in small bridged bicyclics."),
 (MC,"Conjugated double bonds are separated by:",
   ["no bonds","exactly one single bond","two single bonds","an oxygen"],1,
   "C=C&ndash;C=C: one single bond between them allows &pi; interaction."),
 (MC,"Conjugated dienes are ____ than isolated dienes:",
   ["less stable","more stable","equal in stability","always aromatic"],1,
   "Conjugation delocalizes the &pi; electrons and lowers the energy."),
 (MC,"Zaitsev's rule predicts the major product is the:",
   ["least substituted alkene","more substituted alkene","cis alkene only","smallest fragment"],1,
   "More substituted = more stable = major (Zaitsev)."),
 (MC,"Dehydrohalogenation removes:",
   ["H&#8322;O","X&#8322;","H&#8314; and X&#8315; (HX)","CO&#8322;"],2,
   "Loss of a proton and a halide (HX) gives the alkene."),
 (MC,"The E1 rate law is:",
   ["k[substrate][base]","k[substrate]","k[base]","k[substrate]&sup2;"],1,
   "E1 is first order — only the substrate appears (RDS = ionization)."),
 (MC,"The E2 rate law is:",
   ["k[substrate]","k[base]","k[substrate][base]","zero order"],2,
   "E2 is bimolecular (second order)."),
 (MC,"The rate-determining step of E1 is:",
   ["proton removal","carbocation formation (ionization)","&pi;-bond formation","base approach"],1,
   "Forming the carbocation is slow and rate-determining."),
 (MC,"E1 almost always competes with:",
   ["S<sub>N</sub>2","E2","S<sub>N</sub>1","radical halogenation"],2,
   "Both E1 and S<sub>N</sub>1 share the carbocation intermediate."),
 (MC,"A bulky base (e.g. potassium tert-butoxide) favors the:",
   ["Zaitsev product","Hofmann product","substitution product","rearranged product"],1,
   "Steric bulk forces removal of a less-hindered proton &rarr; least-substituted (Hofmann) alkene."),
 (MC,"A strong base on a tertiary alkyl halide gives mainly:",
   ["S<sub>N</sub>2","clean E2","S<sub>N</sub>1","no reaction"],1,
   "S<sub>N</sub>2 is blocked by steric hindrance, so E2 dominates."),
 (MC,"The preferred geometry for E2 is:",
   ["syn-coplanar","anti-periplanar","gauche","eclipsed"],1,
   "Anti-periplanar (180&deg;) gives the lowest-energy, staggered transition state."),
 (MC,"Acid-catalyzed dehydration of an alcohol proceeds by:",
   ["E2","E1","S<sub>N</sub>2","radical"],1,
   "Protonate OH, lose water to a carbocation, then lose a &beta;-proton (E1)."),
 (MC,"The two acids used to catalyze dehydration are:",
   ["HCl and HBr","H&#8322;SO&#8324; and H&#8323;PO&#8324;","HF and HI","HNO&#8323; and HClO&#8324;"],1,
   "Concentrated sulfuric or phosphoric acid."),
 (MC,"Unimolecular reactions are rarely used for synthesis because they:",
   ["are too slow","give poorly controlled product mixtures","need expensive catalysts","only work at 0 K"],1,
   "S<sub>N</sub>1/E1 share a carbocation and give mixtures you can't control."),
 # --- fill-in-the-blank ---
 (FILL,"The functional group of an alkene is the ______ (3 words).",
   ["carbon carbon double bond","carbon-carbon double bond","c c double bond","double bond","c=c","carbon carbon double","cc double bond"],
   "The carbon&ndash;carbon double bond (C=C)."),
 (FILL,"&ldquo;Index of hydrogen ________&rdquo; is another name for elements of unsaturation.",
   ["deficiency"],
   "Index of Hydrogen Deficiency (IHD)."),
 (FILL,"The German word behind &ldquo;Z&rdquo; is ________ (meaning together).",
   ["zusammen"],
   "Z = zusammen = together (same side)."),
 (FILL,"A bulky base produces the ________ product (least substituted alkene).",
   ["hofmann","hoffmann"],
   "Hofmann product = least-substituted alkene."),
 (FILL,"Removing the elements of water from an alcohol is called ________.",
   ["dehydration"],
   "Dehydration (acid-catalyzed)."),
]


# ===========================================================================
# ASSEMBLE
# ===========================================================================
def render_sections():
    out = []
    # intro / how-to-use
    out.append(f"""
<section class="topic" id="how">
  <h2 data-short="How to use this">How to use this guide</h2>
  <p>This single file rebuilds your entire CH7 deck into a mastery resource: every topic has
  <b>expanded explanations</b>, the <b>original figures and mechanisms</b> pulled straight from the slides,
  exam tips, mnemonics, worked calculations, then <b>flashcards</b> and a <b>40-question interactive quiz</b>
  that grades itself.</p>
  <ul>
   <li>Use the left menu to jump around (it tracks where you are).</li>
   <li>Click any <b>flashcard</b> to flip it.</li>
   <li>In the quiz, pick answers then hit <b>Check answers</b> — you&rsquo;ll get a score and a why-explanation on every question.</li>
  </ul>
  <div class="callout warnbox">As you asked, <b>carbocation rearrangements are intentionally excluded.</b>
  Everything else from sections 7-1 to 7-18 is covered.</div>
</section>""")
    for sid, title, short, body in SECTIONS:
        out.append(f'<section class="topic" id="{sid}">\n'
                   f'  <h2 data-short="{short}">{title}</h2>\n{body}\n</section>')
    # flashcards
    cards = "".join(
        f'<div class="flash"><div class="flash-inner">'
        f'<div class="flash-front">{q}</div>'
        f'<div class="flash-back">{a}</div></div></div>'
        for q, a in FLASHCARDS)
    out.append(f"""
<section class="topic" id="flashcards">
  <h2 data-short="Flashcards">Rapid-Recall Flashcards</h2>
  <p>Click a card to reveal the answer. Great for the night before.</p>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px">{cards}</div>
</section>""")
    # quiz
    qhtml = []
    for i, item in enumerate(QUIZ):
        if item[0] == MC:
            _, stem, opts, _, expl = item
            opthtml = "".join(
                f'<label class="opt" data-q="{i}" data-i="{j}">{chr(65+j)}. {o}</label>'
                for j, o in enumerate(opts))
            qhtml.append(f'<div class="q" data-type="mc" data-q="{i}">'
                         f'<p><span class="qnum">Q{i+1}.</span>{stem}</p>{opthtml}'
                         f'<div class="expl" id="expl{i}"></div></div>')
        else:
            _, stem, _, expl = item
            qhtml.append(f'<div class="q" data-type="fill" data-q="{i}">'
                         f'<p><span class="qnum">Q{i+1}.</span>{stem}</p>'
                         f'<input type="text" data-q="{i}" placeholder="type your answer&hellip;" autocomplete="off">'
                         f'<div class="expl" id="expl{i}"></div></div>')
    out.append(f"""
<section class="topic" id="quiz">
  <h2 data-short="&#9733; QUIZ (40 Q)">&#9733; Interactive Quiz &mdash; 40 Questions</h2>
  <p>Answer everything, then grade yourself. Each question explains the correct answer.</p>
  {''.join(qhtml)}
  <div class="btnrow">
    <button onclick="gradeQuiz()">Check answers</button>
    <button class="ghost" onclick="resetQuiz()">Reset</button>
  </div>
  <div id="score"></div>
</section>""")
    return "\n".join(out)

# ---- quiz JS (answers embedded) ------------------------------------------
import json
ANSWERS = []
for item in QUIZ:
    if item[0] == MC:
        ANSWERS.append({"type": "mc", "correct": item[3], "expl": item[4]})
    else:
        ANSWERS.append({"type": "fill", "accept": [a.lower().strip() for a in item[2]], "expl": item[3]})

QUIZJS = """
const ANS = __ANSDATA__;
let selected = {};
document.querySelectorAll('#quiz .opt').forEach(o=>{
  o.addEventListener('click',()=>{
    const q=o.dataset.q;
    document.querySelectorAll('.opt[data-q="'+q+'"]').forEach(x=>x.classList.remove('sel'));
    o.classList.add('sel'); selected[q]=parseInt(o.dataset.i);
  });
});
function norm(s){return (s||'').toLowerCase().trim().replace(/[.,;:!]+$/,'').replace(/\\s+/g,' ');}
function gradeQuiz(){
  let score=0,total=ANS.length;
  ANS.forEach((a,i)=>{
    const expl=document.getElementById('expl'+i);
    let ok=false;
    if(a.type==='mc'){
      document.querySelectorAll('.opt[data-q="'+i+'"]').forEach(o=>{
        o.classList.remove('correct','wrong');
        const idx=parseInt(o.dataset.i);
        if(idx===a.correct)o.classList.add('correct');
        else if(selected[i]===idx)o.classList.add('wrong');
      });
      ok = selected[i]===a.correct;
    }else{
      const inp=document.querySelector('input[data-q="'+i+'"]');
      const v=norm(inp.value);
      ok = a.accept.some(x=>norm(x)===v || (v.length>2 && norm(x).includes(v)));
      inp.style.borderColor = ok? 'var(--good)':'var(--bad)';
    }
    if(ok)score++;
    expl.innerHTML='<b>'+(ok?'\\u2705 Correct.':'\\u274c Not quite.')+'</b> '+a.expl;
    expl.classList.add('show');
  });
  const pct=Math.round(score/total*100);
  const el=document.getElementById('score');
  let msg = pct>=90?'\\ud83c\\udfc6 Outstanding \\u2014 exam-ready!':pct>=75?'\\ud83d\\udcaa Strong \\u2014 review the misses.':pct>=50?'\\ud83d\\udcd6 Getting there \\u2014 revisit the weak topics above.':'\\ud83d\\udd01 Re-read the sections and try again.';
  el.textContent='You scored '+score+' / '+total+'  ('+pct+'%)  \\u2014  '+msg;
  el.classList.add('show');
  el.scrollIntoView({behavior:'smooth',block:'center'});
}
function resetQuiz(){
  selected={};
  document.querySelectorAll('#quiz .opt').forEach(o=>o.classList.remove('sel','correct','wrong'));
  document.querySelectorAll('#quiz input').forEach(i=>{i.value='';i.style.borderColor='';});
  document.querySelectorAll('#quiz .expl').forEach(e=>{e.classList.remove('show');e.innerHTML='';});
  const el=document.getElementById('score');el.classList.remove('show');el.textContent='';
  window.scrollTo({top:document.getElementById('quiz').offsetTop-10,behavior:'smooth'});
}
""".replace("__ANSDATA__", json.dumps(ANSWERS))

html_doc = HTML_HEAD.replace(PLACEHOLDER, render_sections()).replace("__QUIZJS__", QUIZJS)
outpath = os.path.join(os.path.dirname(__file__), "index.html")
with open(outpath, "w", encoding="utf-8") as f:
    f.write(html_doc)
print(f"Wrote {outpath}  ({len(html_doc)/1024/1024:.2f} MB)")
print(f"Sections: {len(SECTIONS)} | Flashcards: {len(FLASHCARDS)} | Quiz Qs: {len(QUIZ)}")
