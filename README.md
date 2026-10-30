# Bassi di Jacopo Napoli su doppio rigo

Trascrizione su doppio rigo degli 80 bassi di *Bassi per lo studio dell'armonia complementare* di Jacopo Napoli, pronti per gli esercizi di armonizzazione.

**[Bassi_completi.pdf](Bassi_completi.pdf)**: copertina, indice e 80 esercizi.

## ⚠️ Attenzione: trascrizione fatta da una AI

La trascrizione dal PDF originale a MusicXML è stata fatta da un'intelligenza artificiale e **può contenere errori** (note, alterazioni, durate, chiavi, tempi, pause, legature).
**Controlla ogni esercizio contro l'originale prima di usarlo.**

## Contenuto

- `musicxml/` – i 80 file sorgente `basso_01.musicxml` … `basso_80.musicxml`. Correggi qui gli errori.
- `build.py` – converte MusicXML → LilyPond → PDF e lo unisce alla copertina.
- `copertina.tex` / `copertina.pdf` – copertina (XeLaTeX).

## Rigenerare il PDF

Servono `lilypond` (con `musicxml2ly`), `pdfunite` (poppler-utils) e il font EB Garamond.

```sh
python3 build.py   # scrive Bassi_completi.pdf
```

## Segnalare errori

Apri una issue o una pull request indicando il numero dell'esercizio e la battuta.

## Diritti

L'opera originale appartiene ai rispettivi titolari; questo repository contiene solo la trascrizione e non include la scansione originale.
