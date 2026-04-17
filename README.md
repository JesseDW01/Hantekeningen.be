# Hantekeningen.be

Portfolio en winkel voor een Vlaamse cartoonist en graphic novel schrijver.

**Live URL:** https://hantekeningen-be.netlify.app

## Tech Stack

- [Astro](https://astro.build/) — static site generator
- [Tailwind CSS v4](https://tailwindcss.com/) — styling
- [Snipcart](https://snipcart.com/) — e-commerce (digitale downloads + fysieke producten)
- [Netlify](https://www.netlify.com/) — hosting & forms

## Project Structure

```text
/
├── public/
│   └── images/          # Product- en portfolio-afbeeldingen
├── src/
│   ├── components/      # Astro componenten (PaperCard, InkButton, ...)
│   ├── data/            # Statische JSON data (producten, portfolio)
│   ├── layouts/         # Astro layouts
│   ├── lib/             # Data helpers
│   ├── pages/           # Astro pagina's
│   ├── styles/          # Global CSS + Tailwind thema
│   └── types/           # TypeScript interfaces
├── scripts/             # Python tools for comic processing
├── netlify.toml         # Netlify build config
└── package.json
```

## Commands

| Command             | Action                                           |
| :------------------ | :----------------------------------------------- |
| `npm install`       | Installeert dependencies                         |
| `npm run dev`       | Start dev server op `localhost:4321`             |
| `npm run build`     | Bouwt productie-site naar `./dist/`              |
| `npm run preview`   | Preview de build lokaal                          |
| `npx astro check`   | TypeScript validatie                             |

## Deploy

```bash
npm run build
netlify deploy --prod
```

## Snipcart Setup

De site gebruikt momenteel een **test API key** voor Snipcart.

Om live te gaan:

1. Maak een account aan op [snipcart.com](https://snipcart.com/)
2. Genereer je **Public API Key**
3. Vervang de test key in `src/pages/winkel.astro`:
   ```html
   <div hidden id="snipcart" data-api-key="JOUW-ECHTE-KEY" ...></div>
   ```
4. Configureer in het Snipcart dashboard:
   - Valuta: **EUR**
   - Taal: **nl**
   - Verzendregels voor fysieke producten
   - Digitale downloads voor PDF-producten

## Content beheren

Producten en portfolio-items zijn opgeslagen als statische JSON:

- `src/data/products.json` — product catalogus
- `src/data/portfolio.json` — portfolio highlights

Pas deze bestanden aan en herdeploy om wijzigingen live te zetten.

## Aesthetic

Handgetekend vierkant papier, inkt-zwart op papier-wit. De stijl wordt gerealiseerd via custom Tailwind kleuren (`paper`, `ink`, `graphite`) en hand-getekende CSS border effects.

---

## Comic Processing Pipeline

Custom Python-gebaseerde tools om handgetekende strips te digitaliseren voor hoge kwaliteit drukwerk.

### Setup

```bash
cd scripts
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 1. Pagina's optimaliseren (`process_comic_pages.py`)

Digitaliseer foto's of scans van originele tekeningen. Dit proces verwijderet onregelmatige belichting, corrigeert perspectief, en maakt de achtergrond transparant.

- **Modi:**
  - `python process_comic_pages.py` — Behoudt de originele penkleur (vivid blue).
  - `python process_comic_pages.py --bw` — Converteert naar zacht zwart-wit (grayscale).

### 2. Binder-gaten verwijderen (`remove_comic_holes.py`)

Een optionele post-processing stap die specifiek zoekt naar binder-gaten (ringfolder holes) en deze chirurgisch verwijdert uit de transparante PNGs.

Gebruik:
```bash
python remove_comic_holes.py
```

### 3. Boek genereren (`create_comic_book.py`)

Bundelt de bewerkte pagina's in digitale formaten.

- **PDF:** Hoge kwaliteit, drukklaar, behoudt transparantie (gebruikt `img2pdf`).
- **EPUB:** Geoptimaliseerd voor digitale comic readers en e-readers.

Gebruik:
```bash
python create_comic_book.py --web
```
*(De boeken verschijnen automatisch in de hoofdmap `albums/`). De `--web` vlag zorgt voor een geoptimaliseerde, kleinere PDF voor online gebruik.*

