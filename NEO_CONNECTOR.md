# NEO_CONNECTOR -- DoctolibDataScraper
- service: doctolibscraper
- base_url_prod: N/A (no HTTP service -- pure CLI tool)
- auth: none (no server; not network-callable)
- env_required: []
- generated_at:

## Summary

DoctolibDataScraper is a **pure command-line Selenium scraper**, not a web service.
It exposes **NO HTTP endpoints, webhooks, SSE/WebSocket streams, cron jobs, or queues**.
The entire program is a single interactive script (`main.py`, ~463 LOC) launched as
`python main.py`, which prompts on stdin for a Doctolib search URL and writes two local
CSV files. There is nothing for NeoBot to call over the network.

Proven from code (`main.py`):
- No web framework imported. `requirements.txt` = beautifulsoup4, pandas, selenium,
  webdriver-manager only. No flask/fastapi/aiohttp/express/uvicorn anywhere
  (grep confirmed: zero matches).
- Entry point is `if __name__ == "__main__": main()` (main.py:462-463).
- `main()` (main.py:426) reads the target via `input("Enter Doctolib search URL: ")`
  (main.py:435) -- interactive stdin, not an argument or request.
- Output is files on disk, not a response:
  - `OUTPUT_LINKS_CSV = "doctolib_profile_link.csv"` (main.py:35)
  - `OUTPUT_DETAILS_CSV = "doctolib_profile_details.csv"` (main.py:36)
  - also `scraper.log` (FileHandler, main.py:50).

## Endpoints

None. This project does not serve any HTTP/webhook/SSE/WS endpoint.

## Flows

Local two-phase batch run (no network API surface):
1. `python main.py` -> prompts on stdin for a Doctolib search URL (main.py:435).
2. **Phase 1** `scrape_all_search_results(search_url)` (main.py:161): paginated crawl
   of search results via Selenium Chrome -> `save_links_csv(...)` ->
   `doctolib_profile_link.csv` (main.py:233).
3. **Phase 2** `scrape_all_profiles(links)` (main.py:377): visits each profile + alt
   location tabs, extracts name/addresses/skills/degrees/contacts -> progressively
   writes `doctolib_profile_details.csv` every 5 profiles (main.py:408-411).

Optional, non-API runtime dependencies (NOT inputs Neo can pass):
- Headful Chrome via Selenium + webdriver-manager (`create_driver`, main.py:101).
- NordVPN CLI for IP rotation if installed (`vpn_connect`, main.py:70); skipped with a
  warning if the `nordvpn` binary is absent (main.py:76-77).

## Config (hardcoded constants, not env vars)

From code (main.py:34-39); none are environment-driven:
- `BASE_URL = "https://www.doctolib.fr"` (the scrape target, not a service base URL)
- `VPN_RECONNECT_DELAY = 10`, `PAGE_LOAD_WAIT = 8`, `SCROLL_PAUSE = 2`

## Gaps

None ambiguous. The project is unambiguously a standalone CLI scraper with no exposed
service. There are no UNKNOWN endpoints to verify.

## Neo wiring guidance

**Do NOT wire this as a Neo HTTP tool.** There is no callable service, auth, or base URL.
If Neo ever needs Doctolib data, the only integration path is to **execute the script as a
subprocess** (interactive stdin URL prompt) on a host that has Chrome + (optionally)
NordVPN, then read the produced CSV files -- this is a shell/process integration, not an
HTTP `integrations.py` tool. Note: scraping Doctolib.fr may violate its ToS; treat as a
manual/operator-gated action, not an autonomous Neo HTTP capability.

## Recap

- Endpoints found: 0 (HTTP/webhook/SSE/WS/cron/queue).
- Already covered vs new: N/A -- nothing to cover; not an HTTP integration target.
