# Draft: Hantekeningen.be Cartoonist Site

## Requirements (confirmed)
- Target user: cartoonist and graphic novel writer
- Goal: spread work + sell in digital and printed formats
- Infrastructure preference: Netim (domain) → Netlify (hosting) → Hetzner VPS (backend)

## Requirements (confirmed)
- Target user: cartoonist and graphic novel writer
- Goal: spread work + sell in digital and printed formats
- Site structure: 2 pages
  1. **Main page** (`/`) with sections: hero (home), portfolio highlight, about, contact
  2. **Shop page** (`/winkel`) with Snipcart-powered product grid
- Aesthetic: hand-drawn square paper, black ink on white
- Language: Flemish/Dutch only
- Infrastructure: Netlify (static hosting), no Hetzner VPS for now

## Technical Decisions
- **Framework**: Astro (static multi-page, fast, simple)
- **E-commerce**: Snipcart (static-friendly, digital + physical, EUR support, Dutch language)
- **Hosting**: Netlify with Git-based deploys
- **Styling**: Tailwind CSS + custom SVG/paper textures
- **Contact form**: Netlify Forms
- **Content**: Astro content collections / static data for portfolio highlights and products

## Test Strategy
- No dedicated test framework needed for this simple static site
- Verification via agent-executed QA: Playwright for visual/functional checks, Bash for build verification

## Scope Boundaries
- **INCLUDE**:
  - Astro project scaffolding
  - Tailwind + custom paper/ink styling system
  - Main page with 4 sections (hero, portfolio highlight, about, contact)
  - Shop page with Snipcart integration
  - Netlify form setup
  - Dutch copy and placeholder content structure
  - Build + deploy to Netlify
- **EXCLUDE**:
  - Hetzner VPS backend
  - Full separate portfolio page (only highlight section on main page)
  - Blog/news section
  - Newsletter signup backend
  - Custom auth or user accounts
  - Full CMS integration (keep it simple static/Markdown)

