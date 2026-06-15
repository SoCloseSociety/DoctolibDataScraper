# CLAUDE.md -- DoctolibDataScraper

## 1. Project Identity

**Name:** DoctolibDataScraper -- French Doctor Listings Scraper
**Role:** Scrape doctor profiles from Doctolib.fr including names, addresses, skills, degrees, and contacts. Supports VPN rotation via NordVPN CLI.
**Author:** SoClose Society (https://soclose.co)
**License:** MIT

### Stack

- **Language:** Python 3.9+
- **Browser:** Selenium 4.15+ with webdriver-manager
- **Parsing:** BeautifulSoup4
- **Data:** pandas
- **VPN:** NordVPN CLI (optional, for IP rotation)
- **Architecture:** Monolithic (single main.py, 463 LOC)

### Architecture

```
Phase 1: Crawl paginated search results -> doctolib_profile_link.csv
Phase 2: Scrape each doctor profile -> doctolib_profile_details.csv
```

### Critical Files

- `main.py` -- All logic (463 LOC)
- Output: doctolib_profile_link.csv, doctolib_profile_details.csv

## 2-5. Standard Workflow

- Enter plan mode for non-trivial tasks
- Test with a single search URL first
- Verify both CSV outputs have data
- Track tasks in `tasks/todo.md`, lessons in `tasks/lessons.md`

## 6. Project-Specific Rules

### Dev Commands
```bash
pip install -r requirements.txt
python main.py   # Interactive: enter Doctolib search URL
```

### Config (hardcoded in main.py)
- BASE_URL = "https://www.doctolib.fr"
- VPN_RECONNECT_DELAY=10, PAGE_LOAD_WAIT=8, SCROLL_PAUSE=2
- Progressive save every 5 profiles

### Known Fragile Areas
- Doctolib DOM changes -- French localized selectors
- VPN rotation -- NordVPN CLI must be installed separately
- Pagination detection -- relies on specific button selectors

## 7. Core Principles

- Simplicity First, No Laziness, Minimal Impact
- Never use em dashes (use -- instead)

## Neo Connector (auto)

Ce projet expose `NEO_CONNECTOR.md` : le manifeste machine-lisible de TOUS ses
endpoints/auth/env, consommé par NeoBot pour se câbler automatiquement.
- ÉTAT : ce projet est un scraper CLI pur (aucun endpoint HTTP/webhook/SSE/WS). Le
  manifeste le déclare explicitement -- il ne doit PAS être câblé comme outil HTTP Neo.
- RÈGLE : à chaque ajout/suppression/modif d'un endpoint, d'une auth ou d'une env var,
  régénère le manifeste via `/neo-connector` (ou le prompt dans .claude/skills/neo-connector).
- Ne jamais éditer NEO_CONNECTOR.md à la main : il est généré.
- Le hook pre-commit (.git/hooks/pre-commit) avertit si des routes ont changé sans MAJ du manifeste.
