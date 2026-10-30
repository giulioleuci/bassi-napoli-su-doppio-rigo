#!/usr/bin/env python3
"""MusicXML -> LilyPond -> Bassi_completi.pdf (copertina + indice + esercizi di seguito)."""
import re, subprocess
from pathlib import Path

N = 80
ROOT = Path(__file__).parent
OUT = ROOT / "build"
OUT.mkdir(exist_ok=True)

HEAD = r'''\version "2.24.4"
\pointAndClickOff
#(set-global-staff-size 24)
\paper {
  paper-width = 21\cm  paper-height = 29.7\cm
  top-margin = 1.2\cm  bottom-margin = 1.2\cm
  left-margin = 1.2\cm right-margin = 1.2\cm
  indent = 0
  first-page-number = 2
  print-first-page-number = ##t
  system-system-spacing.basic-distance = 22
  system-system-spacing.padding = 4
  score-system-spacing.basic-distance = 22
  score-system-spacing.padding = 4
  ragged-bottom = ##t
  tagline = ##f
  oddHeaderMarkup = \markup \fill-line { " " \fromproperty #'page:page-number-string }
  evenHeaderMarkup = \markup \fill-line { " " \fromproperty #'page:page-number-string }
  bookTitleMarkup = ##f
  scoreTitleMarkup = ##f
  #(define fonts (set-global-fonts #:roman "EB Garamond" #:factor (/ staff-height pt 20)))
}
'''

# spazio proporzionale alla durata: ogni movimento in battere ha la stessa larghezza,
# una nota lunga occupa tanti movimenti quanti ne copre, le note di passaggio si stringono.
def vn(n):
    return "V" + "".join(chr(97 + int(d)) for d in f"{n:02d}")


def score(n, beat):
    v = vn(n)
    return f'''
\\markup \\vspace #3
\\score {{
  \\new PianoStaff \\with {{
    instrumentName = \\markup \\override #'(font-name . "DejaVu Sans Bold") \\fontsize #5 "{n}"
    shortInstrumentName = ""
  }} << \\new Staff {{ \\label #'b{n:02d} \\{v}a }} \\new Staff {{ \\{v}b }} >>
  \\layout {{
    indent = 1.9\\cm
    short-indent = 0
    \\context {{ \\Score
      proportionalNotationDuration = #(ly:make-moment 5/{beat * 14})
      \\override SpacingSpanner.uniform-stretching = ##t
    }}
  }}
}}
'''

defs, scores = [], []
for n in range(1, N + 1):
    ly = OUT / f"b{n:02d}.ly"
    xml = ROOT / "musicxml" / f"basso_{n:02d}.musicxml"
    subprocess.run(["musicxml2ly", "-o", str(ly), str(xml)], check=True, capture_output=True)
    m = re.search(r"PartPOneVoiceOne =.*?(?=% The score definition)", ly.read_text(), re.S).group(0)
    m = re.sub(r"\\(break|pageBreak)\b", "", m)
    m = m.replace("PartPOneVoiceOne", vn(n) + "a").replace("PartPOneVoiceTwo", vn(n) + "b")
    defs.append(m)
    beat = int(re.search(r"<beat-type>(\d+)", xml.read_text()).group(1))
    scores.append(score(n, beat))

DOTS = '"· · · · · · · ·"'
def col(a):
    rows = " ".join(f"\\override #'(line-width . 15) \\fill-line {{ \\bold \"{n}\" {DOTS} "
                    f"\\page-ref #'b{n:02d} \"000\" \"?\" }}" for n in range(a, a + 20))
    return f"\\column {{ {rows} }}"


VLINE = "\\override #'(thickness . 0.5) \\draw-line #'(0 . -52)"
index = (r'''\bookpart {
  \markup \vspace #2
  \markup \fontsize #8 "Indice"
  \markup \vspace #2
  \markup \line { ''' + f" \\hspace #1.5 {VLINE} \\hspace #1.5 ".join(col(a) for a in (1, 21, 41, 61)) + " }\n}")

(OUT / "all.ly").write_text(HEAD + "\n".join(defs) + "\n\\book {\n" + index
                            + "\n\\bookpart {\n" + "".join(scores) + "}\n}\n")
subprocess.run(["lilypond", "-o", str(OUT / "all"), str(OUT / "all.ly")], check=True)
subprocess.run(["pdfunite", str(ROOT / "copertina.pdf"), str(OUT / "all.pdf"),
                str(ROOT / "Bassi_completi.pdf")], check=True)
