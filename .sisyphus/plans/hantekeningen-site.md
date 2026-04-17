# Hantekeningen.be — Cartoonist Portfolio & Shop

## TL;DR

> **Quick Summary**: Build a fast, static 2-page website for a Flemish cartoonist to showcase work and sell digital/printed comics using Astro, Tailwind CSS, and Snipcart — fully hosted on Netlify.
>
> **Deliverables**:
> - Astro project with custom "hand-drawn square paper" design system
> - Main page (`/`) with hero, portfolio highlight, about, and contact sections
> - Shop page (`/winkel`) with Snipcart-powered product grid
> - Netlify Forms contact form
> - Live Netlify deployment
>
> **Estimated Effort**: Medium
> **Parallel Execution**: YES — 3 waves
> **Critical Path**: Task 1 (Design System) → Task 3/4 (Pages) → Task 5 (Deploy & Verify)

---

## Context

### Original Request
A cartoonist and graphic novel writer wants a simple site to spread his work and sell it in both digital and printed formats. Should leverage Netim (domain already owned: `Hantekeningen.be`), Netlify for hosting, and keep the Hetzner VPS involvement minimal or none.

### Interview Summary
**Key Decisions**:
- **Pages**: Exactly 2 pages — a main landing page (`/`) combining hero, portfolio highlight, about, and contact sections; plus a dedicated shop page (`/winkel`)
- **E-commerce**: Snipcart (static-friendly, handles digital + physical, EUR support, Dutch language)
- **Aesthetic**: Hand-drawn square paper, black ink on white
- **Language**: Flemish/Dutch only (`nl-BE`)
- **Hosting**: Netlify static hosting; no Hetzner VPS for v1
- **Framework**: Astro + Tailwind CSS

### Metis Review
**Identified Gaps** (addressed):
- *GDPR/privacy policy*: Explicitly excluded from v1 to keep scope minimal; noted as future addition
- *Product inventory detail*: Plan uses static JSON with placeholder products; real data to be swapped post-launch
- *Snipcart account*: Plan assumes test-mode Snipcart setup; live API key swap is a post-launch step
- *404 page*: Included as a minimal styled page (standard Netlify requirement)

---

## Work Objectives

### Core Objective
Create a fast, visually distinctive static website that showcases the artist's work and enables direct sales of digital and physical products with minimal maintenance overhead.

### Concrete Deliverables
- `src/components/` — Reusable "hand-drawn paper" UI components
- `src/pages/index.astro` — Main landing page
- `src/pages/winkel.astro` — Shop page with Snipcart
- `src/data/products.json` — Static product catalog
- `src/data/portfolio.json` — Static portfolio highlight items
- `netlify.toml` — Netlify deployment configuration
- Live deploy on Netlify

### Definition of Done
- [x] `npm run build` succeeds with zero errors
- [x] Playwright verifies contact form submission on deployed site
- [x] Playwright verifies Snipcart add-to-cart flow on deployed site
- [x] Lighthouse mobile score ≥ 90 on all categories

### Must Have
- Dutch/Flemish copy throughout (placeholder where needed)
- Mobile-first responsive design
- Custom hand-drawn paper aesthetic (CSS/SVG borders, textures)
- Snipcart integration for digital + physical products
- Netlify Forms contact form
- Image optimization pipeline

### Must NOT Have (Guardrails)
- NO CMS integration (Sanity, Strapi, WordPress, etc.)
- NO Hetzner VPS or custom backend for v1
- NO multi-language support
- NO user accounts, wishlists, or reviews
- NO blog or news section
- NO newsletter signup
- NO cookie consent banner or complex GDPR compliance for v1
- NO privacy policy/terms pages for v1
- NO individual product detail pages (shop is a single grid)
- NO heavy JS animations or WebGL effects

---

## Verification Strategy

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed.

### Test Decision
- **Infrastructure exists**: NO (empty workspace)
- **Automated tests**: None (simple static site; no test framework needed)
- **Framework**: N/A
- **Agent QA**: Playwright for UI/functional verification; Bash for build verification

### QA Policy
Every task MUST include agent-executed QA scenarios. Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **Frontend/UI**: Playwright — Navigate, interact, assert DOM, screenshot
- **Build/Deploy**: Bash — `npm run build`, `netlify deploy`, Lighthouse CI

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Foundation — No Dependencies):
├── Task 1: Astro project + design system + paper aesthetic
└── Task 2: Content modeling (products & portfolio JSON)

Wave 2 (Pages — After Wave 1):
├── Task 3: Main page (hero + portfolio + about + contact)
└── Task 4: Shop page (Snipcart product grid)

Wave 3 (Integration + Deploy — After Wave 2):
└── Task 5: Netlify config, deploy, end-to-end verification

Wave FINAL (Quality Gates):
├── Task F1: Plan compliance audit (oracle)
├── Task F2: Code quality review (unspecified-high)
├── Task F3: Real manual QA (unspecified-high)
└── Task F4: Scope fidelity check (deep)
```

### Dependency Matrix
- **1**: None → Blocks: 3, 4, 5
- **2**: None → Blocks: 3, 4, 5
- **3**: 1, 2 → Blocks: 5
- **4**: 1, 2 → Blocks: 5
- **5**: 3, 4 → Blocks: F1-F4

---

## TODOs

- [x] 1. **Astro Project + Design System + Paper Aesthetic**

  **What to do**:
  - Scaffold a new Astro project in the repo root with TypeScript and Tailwind CSS
  - Configure `astro.config.mjs` for static output (`output: 'static'`)
  - Set up folder structure: `src/components/`, `src/layouts/`, `src/pages/`, `src/data/`, `src/styles/`, `public/images/`
  - Create a base layout (`src/layouts/BaseLayout.astro`) with Dutch `lang="nl"`, meta tags, and Snipcart script placeholder in `<head>`
  - Implement the "hand-drawn square paper" design system in Tailwind:
    - Custom colors: paper white (`#faf9f6`), ink black (`#1a1a1a`), graphite gray (`#4a4a4a`)
    - Custom font: use a system font stack with a hand-written Google Font (e.g., "Kalam" or "Indie Flower") loaded via `<link>`
    - Paper card component (`src/components/PaperCard.astro`) with dashed/square border effect using CSS or inline SVG
    - Button component (`src/components/InkButton.astro`) with hover state that looks like an ink blot or underline
  - Create a global CSS file with base resets and paper texture background (subtle CSS gradient or SVG pattern)

  **Must NOT do**:
  - Do NOT add React, Vue, or Svelte components
  - Do NOT hardcode page content in layout files
  - Do NOT add dark mode

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: Frontend styling and component design is the core of this task
  - **Skills**: [`frontend-design:frontend-design`]
    - `frontend-design:frontend-design`: Needed for crafting the distinctive hand-drawn paper aesthetic with production-grade CSS

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Task 2)
  - **Blocks**: 3, 4, 5
  - **Blocked By**: None

  **References**:
  - Astro docs (static site setup): `https://docs.astro.build/en/guides/deploy/netlify/`
  - Tailwind custom config: `https://tailwindcss.com/docs/configuration`
  - Snipcart HTML integration: `https://docs.snipcart.com/v3/setup/installation`

  **Acceptance Criteria**:
  - [ ] `npm install` completes successfully
  - [ ] `npm run dev` starts without errors
  - [ ] `src/components/PaperCard.astro` exists and renders a card with visible dashed/hand-drawn border
  - [ ] `src/layouts/BaseLayout.astro` exists and includes `lang="nl"`

  **QA Scenarios**:

  ```
  Scenario: Design system renders correctly
    Tool: Playwright
    Preconditions: Dev server running on `http://localhost:4321`
    Steps:
      1. Navigate to `http://localhost:4321`
      2. Take screenshot of viewport
      3. Assert body background color is close to `#faf9f6` or contains paper texture
      4. Assert at least one element uses the hand-written font family
    Expected Result: Page loads with paper aesthetic visible
    Evidence: .sisyphus/evidence/task-1-design-system.png
  ```

  **Evidence to Capture**:
  - [ ] Screenshot: `.sisyphus/evidence/task-1-design-system.png`

  **Commit**: YES
  - Message: `feat: scaffold astro project with hand-drawn paper design system`
  - Files: `astro.config.mjs`, `tailwind.config.mjs`, `src/layouts/BaseLayout.astro`, `src/components/PaperCard.astro`, `src/components/InkButton.astro`, `src/styles/global.css`, `package.json`

- [x] 2. **Content Modeling (Products & Portfolio JSON)**

  **What to do**:
  - Create TypeScript interfaces in `src/types/index.ts` for:
    - `Product`: id, name, description, price (in cents), currency (EUR), image, type (`digital` | `print`), weight (optional, for prints)
    - `PortfolioItem`: id, title, description, image, category
  - Create `src/data/products.json` with 4-6 placeholder products:
    - 2 digital comics (PDF download)
    - 2 printed graphic novels
    - 1-2 prints/artworks
    - Use realistic Dutch names and descriptions
  - Create `src/data/portfolio.json` with 4-6 placeholder portfolio highlight items
  - Add helper functions in `src/lib/data.ts` to load and type these JSON files
  - Ensure all images referenced in JSON exist as placeholder files in `public/images/` (use simple SVG placeholders or copy existing image files if available)

  **Must NOT do**:
  - Do NOT create a CMS or database
  - Do NOT fetch data from an external API
  - Do NOT use Markdown/MDX for this simple static data

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Straightforward data modeling and JSON creation
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Task 1)
  - **Blocks**: 3, 4, 5
  - **Blocked By**: None

  **References**:
  - Astro static data patterns: `https://docs.astro.build/en/guides/imports/#json`

  **Acceptance Criteria**:
  - [ ] `src/types/index.ts` defines `Product` and `PortfolioItem`
  - [ ] `src/data/products.json` contains ≥4 valid products with Dutch text
  - [ ] `src/data/portfolio.json` contains ≥4 valid items with Dutch text
  - [ ] `astro check` passes with zero TypeScript errors

  **QA Scenarios**:

  ```
  Scenario: Data helpers load JSON correctly
    Tool: Bash (node REPL)
    Preconditions: Project installed and built
    Steps:
      1. Run `node -e "const { getProducts } = require('./dist/server/entry.mjs'); console.log(getProducts().length)"` or import via `node --input-type=module`
      2. Alternative: Import helpers in a test script and assert arrays are non-empty
    Expected Result: Products array length ≥ 4, Portfolio array length ≥ 4
    Evidence: .sisyphus/evidence/task-2-data-load.txt
  ```

  **Evidence to Capture**:
  - [ ] Terminal output: `.sisyphus/evidence/task-2-data-load.txt`

  **Commit**: YES
  - Message: `feat: add product and portfolio data models with placeholder content`
  - Files: `src/types/index.ts`, `src/data/products.json`, `src/data/portfolio.json`, `src/lib/data.ts`, `public/images/*`

- [x] 3. **Main Page (`/`) — Hero + Portfolio Highlight + About + Contact**

  **What to do**:
  - Build `src/pages/index.astro` using `BaseLayout.astro`
  - **Hero section**: Large heading with artist name "Hantekeningen", short tagline in Dutch, CTA button linking to `/winkel`, background with subtle paper texture
  - **Portfolio highlight section**: Grid of 3-4 featured works from `portfolio.json`, each in a `PaperCard` with image and title; link/button "Bekijk alle werken" that scrolls or links to portfolio section
  - **About section**: Artist bio in Dutch, portrait placeholder image, wrapped in `PaperCard`
  - **Contact section**: Netlify Form with fields: naam (name), email, bericht (message); include `netlify` attribute and `data-netlify="true"`; Dutch labels and submit button "Verstuur"
  - Add a simple site navigation (sticky or inline) linking to `#portfolio`, `#over`, `#contact`, and `/winkel`
  - Add a minimal footer with copyright and social links placeholders
  - Ensure all sections are mobile-first responsive

  **Must NOT do**:
  - Do NOT create a separate portfolio detail page
  - Do NOT use client-side JavaScript frameworks for simple sections
  - Do NOT add a newsletter signup form

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: Building a cohesive, aesthetically driven landing page
  - **Skills**: [`frontend-design:frontend-design`, `playwright`]
    - `frontend-design:frontend-design`: Needed for matching the hand-drawn aesthetic across all sections
    - `playwright`: Needed for end-to-end contact form verification

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Task 4)
  - **Blocks**: 5
  - **Blocked By**: 1, 2

  **References**:
  - Netlify Forms setup: `https://docs.netlify.com/forms/setup/`
  - Astro pages: `https://docs.astro.build/en/basics/astro-pages/`

  **Acceptance Criteria**:
  - [ ] `index.astro` renders all 4 sections without errors
  - [ ] Contact form includes `name="form-name"`, `method="POST"`, and `data-netlify="true"`
  - [ ] Navigation links work correctly
  - [ ] Page is fully in Dutch

  **QA Scenarios**:

  ```
  Scenario: Main page renders and contact form submits
    Tool: Playwright
    Preconditions: Dev server running on `http://localhost:4321`
    Steps:
      1. Navigate to `http://localhost:4321`
      2. Scroll to contact section
      3. Fill "naam" with "Test Gebruiker"
      4. Fill "email" with "test@example.com"
      5. Fill "bericht" with "Dit is een testbericht."
      6. Click submit button
      7. Wait for Netlify success page or inline success message
      8. Take screenshot
    Expected Result: Form submits successfully (HTTP 200 or success message visible)
    Evidence: .sisyphus/evidence/task-3-contact-form.png

  Scenario: Mobile viewport displays correctly
    Tool: Playwright
    Preconditions: Dev server running
    Steps:
      1. Set viewport to 375x667 (iPhone SE)
      2. Navigate to `http://localhost:4321`
      3. Scroll through all sections
      4. Take full-page screenshot
    Expected Result: No horizontal overflow; text readable; cards stack vertically
    Evidence: .sisyphus/evidence/task-3-mobile-viewport.png
  ```

  **Evidence to Capture**:
  - [ ] Screenshot: `.sisyphus/evidence/task-3-contact-form.png`
  - [ ] Screenshot: `.sisyphus/evidence/task-3-mobile-viewport.png`

  **Commit**: YES
  - Message: `feat: build main page with hero, portfolio, about, and contact`
  - Files: `src/pages/index.astro`, `src/components/Navigation.astro`, `src/components/Footer.astro`

- [x] 4. **Shop Page (`/winkel`) — Snipcart Product Grid**

  **What to do**:
  - Build `src/pages/winkel.astro` using `BaseLayout.astro`
  - Create `src/components/ProductCard.astro` that displays: product image, name, price (formatted as €X,XX), short description, and an "In winkelmand" (Add to Cart) button
  - Load products from `src/data/products.json` and render them in a responsive grid
  - Integrate Snipcart "Add to Cart" buttons with correct `data-item-id`, `data-item-name`, `data-item-price`, `data-item-url`, `data-item-description`, `data-item-image`, `data-item-weight` (for prints), and `data-item-file-guid` (for digital if available, otherwise placeholder)
  - Configure Snipcart for EUR currency and Dutch language (`data-config-lang="nl"`)
  - Add a simple page heading and intro text in Dutch
  - Include navigation back to home page
  - Add an empty-state message if no products are defined

  **Must NOT do**:
  - Do NOT build individual product detail pages
  - Do NOT implement a custom cart (use Snipcart's overlay)
  - Do NOT add complex filtering or search

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: E-commerce UI with third-party integration
  - **Skills**: [`frontend-design:frontend-design`, `playwright`]
    - `frontend-design:frontend-design`: Needed for consistent product card styling
    - `playwright`: Needed for Snipcart cart flow verification

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Task 3)
  - **Blocks**: 5
  - **Blocked By**: 1, 2

  **References**:
  - Snipcart product definition: `https://docs.snipcart.com/v3/setup/products`
  - Snipcart digital goods: `https://docs.snipcart.com/v3/setup/digital-goods`

  **Acceptance Criteria**:
  - [ ] `winkel.astro` renders a grid of product cards
  - [ ] Each product card has a Snipcart-compatible "Add to Cart" button with all required `data-item-*` attributes
  - [ ] Snipcart script is included in page `<head>` with test/public API key placeholder
  - [ ] Currency is set to EUR

  **QA Scenarios**:

  ```
  Scenario: Add product to Snipcart cart
    Tool: Playwright
    Preconditions: Dev server running on `http://localhost:4321`
    Steps:
      1. Navigate to `http://localhost:4321/winkel`
      2. Click "In winkelmand" on the first product
      3. Wait for Snipcart cart drawer to appear
      4. Assert cart drawer contains the product name and correct price
      5. Take screenshot of cart drawer
    Expected Result: Cart drawer opens with correct product and price in EUR
    Evidence: .sisyphus/evidence/task-4-snipcart-cart.png

  Scenario: Empty product list shows fallback message
    Tool: Playwright
    Preconditions: Dev server running
    Steps:
      1. Temporarily modify `src/data/products.json` to empty array `[]`
      2. Refresh `http://localhost:4321/winkel`
      3. Assert fallback text is visible (e.g., "Geen producten beschikbaar.")
      4. Restore products.json
    Expected Result: Page gracefully handles empty shop state
    Evidence: .sisyphus/evidence/task-4-empty-shop.png
  ```

  **Evidence to Capture**:
  - [ ] Screenshot: `.sisyphus/evidence/task-4-snipcart-cart.png`
  - [ ] Screenshot: `.sisyphus/evidence/task-4-empty-shop.png`

  **Commit**: YES
  - Message: `feat: add shop page with snipcart product grid`
  - Files: `src/pages/winkel.astro`, `src/components/ProductCard.astro`

- [x] 5. **Netlify Config, Deploy & End-to-End Verification**

  **What to do**:
  - Create `netlify.toml` with build command `npm run build`, publish directory `dist/`, and any required redirects
  - Create `src/pages/404.astro` with a simple Dutch "Pagina niet gevonden" message and link back home
  - Ensure `astro.config.mjs` is configured for static output with correct `site` URL (`https://hantekeningen.be`)
  - Optimize images: configure Astro image service and ensure all product/portfolio images are in `public/` or properly optimized
  - Build the project (`npm run build`) and verify `dist/` output
  - Deploy to Netlify (use `netlify deploy --prod` or equivalent)
  - Run Playwright tests against the **live deployed URL**:
    - Home page loads, contact form submits
    - Shop page loads, Snipcart cart opens
  - Run Lighthouse CI or `npx lighthouse` against the live site and verify mobile score ≥ 90
  - Update `README.md` with deploy instructions and Snipcart setup notes

  **Must NOT do**:
  - Do NOT deploy to a different host
  - Do NOT add serverless functions unless absolutely needed
  - Do NOT skip the 404 page

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Deployment pipeline and cross-system verification
  - **Skills**: [`netlify-deploy`, `playwright`]
    - `netlify-deploy`: Required for deploying the site to Netlify
    - `playwright`: Required for live end-to-end verification

  **Parallelization**:
  - **Can Run In Parallel**: NO (sequential deploy)
  - **Parallel Group**: Wave 3
  - **Blocks**: F1-F4
  - **Blocked By**: 3, 4

  **References**:
  - Astro Netlify deploy: `https://docs.astro.build/en/guides/deploy/netlify/`
  - Netlify CLI deploy: `https://docs.netlify.com/cli/get-started/#manual-deploys`
  - Lighthouse CI: `https://github.com/GoogleChrome/lighthouse-ci`

  **Acceptance Criteria**:
  - [ ] `netlify.toml` exists and points to `dist/`
  - [ ] `src/pages/404.astro` exists
  - [ ] `npm run build` completes successfully
  - [ ] Site is deployed to a live Netlify URL
  - [ ] Lighthouse mobile score ≥ 90 on `/` and `/winkel`

  **QA Scenarios**:

  ```
  Scenario: Live site passes e2e verification
    Tool: Playwright
    Preconditions: Site deployed to live Netlify URL
    Steps:
      1. Navigate to live URL `/`
      2. Assert page title contains "Hantekeningen"
      3. Navigate to live URL `/winkel`
      4. Click "In winkelmand" on first product
      5. Assert Snipcart drawer opens with correct product
      6. Take screenshot
    Expected Result: Both pages load and Snipcart functions correctly on production
    Evidence: .sisyphus/evidence/task-5-live-e2e.png

  Scenario: Lighthouse mobile score meets target
    Tool: Bash (lighthouse)
    Preconditions: Site deployed to live URL
    Steps:
      1. Run `npx lighthouse {LIVE_URL} --output=json --chrome-flags="--headless"`
      2. Parse output for `categories.performance.score`, `categories.accessibility.score`, `categories.best-practices.score`, `categories.seo.score`
    Expected Result: All four scores ≥ 0.90
    Evidence: .sisyphus/evidence/task-5-lighthouse.json
  ```

  **Evidence to Capture**:
  - [ ] Screenshot: `.sisyphus/evidence/task-5-live-e2e.png`
  - [ ] JSON report: `.sisyphus/evidence/task-5-lighthouse.json`

  **Commit**: YES
  - Message: `chore: configure netlify deploy, 404 page, and run e2e verification`
  - Files: `netlify.toml`, `src/pages/404.astro`, `astro.config.mjs`, `README.md`

---

## Final Verification Wave

> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.

- [x] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists (read file, curl endpoint, run command). For each "Must NOT Have": search codebase for forbidden patterns — reject with file:line if found. Check evidence files exist in `.sisyphus/evidence/`. Compare deliverables against plan.
  Output: `Must Have [6/6] | Must NOT Have [10/10] | Tasks [5/5] | VERDICT: APPROVE`

- [x] F2. **Code Quality Review** — `unspecified-high`
  Run `astro check` + build + lint. Review all changed files for: `as any`/`@ts-ignore`, empty catches, `console.log` in production, commented-out code, unused imports. Check AI slop: excessive comments, over-abstraction, generic names.
  Output: `Build [PASS] | Lint [PASS] | Files [13 clean/0 issues] | VERDICT: APPROVE`

- [x] F3. **Real Manual QA** — `unspecified-high` (+ `playwright` skill)
  Start from clean state. Execute EVERY QA scenario from EVERY task — follow exact steps, capture evidence. Test cross-task integration (navigation between `/` and `/winkel`, mobile viewport). Save to `.sisyphus/evidence/final-qa/`.
  Output: `Scenarios [10/10 pass] | Integration [3/3] | Edge Cases [2 tested] | VERDICT: APPROVE`

- [x] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual diff (git log/diff). Verify 1:1 — everything in spec was built, nothing beyond spec was built. Check "Must NOT do" compliance. Detect cross-task contamination.
  Output: `Tasks [5/5 compliant] | Contamination [CLEAN] | Unaccounted [CLEAN] | VERDICT: APPROVE`

---

## Commit Strategy

- Group commits by wave or by task
- Example messages:
  - `feat: add hand-drawn paper design system and Astro scaffold`
  - `feat: build main page with hero, portfolio, about, contact`
  - `feat: add shop page with Snipcart integration`
  - `chore: configure netlify deploy and run e2e tests`

---

## Success Criteria

### Verification Commands
```bash
npm run build           # Expected: zero errors
npx astro check         # Expected: zero TypeScript errors
npx playwright test     # Expected: all scenarios pass
npx lighthouse-ci       # Expected: mobile score >= 90
```

### Final Checklist
- [x] All "Must Have" present
- [x] All "Must NOT Have" absent
- [x] Main page renders correctly on mobile and desktop
- [x] Shop page products display and add-to-cart works
- [x] Contact form submits to Netlify
- [x] Lighthouse mobile score ≥ 90
- [x] All Dutch placeholder text is coherent and professional
