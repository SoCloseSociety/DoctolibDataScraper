"""
DoctolibDataScraper - Automated Doctolib.fr profile data extraction tool.

Scrapes doctor profiles from Doctolib search results, extracting names,
addresses, skills, degrees, and contact information into structured CSV files.

Author: SoClose Society (https://soclose.co)
License: MIT
Repository: https://github.com/SoCloseSociety/DoctolibDataScraper
"""

import logging
import platform
import socket
import subprocess
import sys
import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_URL = "https://www.doctolib.fr"
OUTPUT_LINKS_CSV = "doctolib_profile_link.csv"
OUTPUT_DETAILS_CSV = "doctolib_profile_details.csv"
VPN_RECONNECT_DELAY = 10  # seconds
PAGE_LOAD_WAIT = 8  # seconds (WebDriverWait timeout)
SCROLL_PAUSE = 2  # seconds after scroll

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("scraper.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Network utilities
# ---------------------------------------------------------------------------


def is_connected(host: str = "one.one.one.one", port: int = 80, timeout: int = 3) -> bool:
    """Check internet connectivity by resolving and connecting to a known host."""
    try:
        addr = socket.gethostbyname(host)
        with socket.create_connection((addr, port), timeout):
            return True
    except OSError:
        return False


def vpn_connect() -> None:
    """Attempt to connect via NordVPN CLI (cross-platform)."""
    cmd = ["nordvpn", "-c"] if platform.system() == "Windows" else ["nordvpn", "connect"]
    try:
        subprocess.run(cmd, check=False, timeout=30)
        logger.info("VPN connection initiated.")
    except FileNotFoundError:
        logger.warning("NordVPN CLI not found. Continuing without VPN.")
    except subprocess.TimeoutExpired:
        logger.warning("VPN connection timed out.")


def ensure_connectivity() -> None:
    """Wait until internet connectivity is restored, reconnecting VPN if needed."""
    retries = 0
    max_retries = 5
    while not is_connected() and retries < max_retries:
        logger.info("No connectivity. Attempting VPN reconnect (%d/%d)...", retries + 1, max_retries)
        vpn_connect()
        time.sleep(VPN_RECONNECT_DELAY)
        retries += 1
    if not is_connected():
        logger.error("Failed to establish connectivity after %d attempts.", max_retries)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Browser utilities
# ---------------------------------------------------------------------------


def create_driver() -> webdriver.Chrome:
    """Create and return a configured Chrome WebDriver instance."""
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    return driver


def safe_get(driver: webdriver.Chrome, url: str, wait_class: str) -> webdriver.Chrome:
    """
    Navigate to *url* and wait for an element with *wait_class* to appear.
    If the page is blocked (e.g. by Doctolib), reconnect VPN and retry.
    Returns the (possibly new) driver instance.
    """
    max_retries = 3
    for attempt in range(max_retries):
        try:
            driver.get(url)
            WebDriverWait(driver, PAGE_LOAD_WAIT).until(
                EC.presence_of_element_located((By.CLASS_NAME, wait_class))
            )
            return driver
        except Exception:
            logger.warning("Page load failed for %s (attempt %d/%d).", url, attempt + 1, max_retries)
            try:
                driver.quit()
            except Exception:
                pass
            ensure_connectivity()
            driver = create_driver()

    logger.error("Could not load %s after %d attempts.", url, max_retries)
    return driver


def scroll_page(driver: webdriver.Chrome) -> None:
    """Scroll to the bottom of the page to trigger lazy-loaded content."""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE)


# ---------------------------------------------------------------------------
# Scraping: search results (Phase 1)
# ---------------------------------------------------------------------------


def scrape_search_page(soup: BeautifulSoup) -> list[str]:
    """Extract doctor profile links from a single search results page."""
    links = []
    for tag in soup.find_all("a", class_="dl-search-result-name js-search-result-path", href=True):
        links.append(tag["href"])
    return links


def scrape_all_search_results(search_url: str) -> list[str]:
    """Iterate through all paginated search results and collect profile links."""
    logger.info("Phase 1: Collecting profile links from search results...")
    driver = create_driver()

    # --- first page ---
    driver = safe_get(driver, search_url, "results")
    scroll_page(driver)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    all_links = scrape_search_page(soup)
    logger.info("Page 1: found %d links.", len(all_links))

    # --- subsequent pages ---
    page = 2
    while True:
        page_url = f"{search_url}/?page={page}"
        try:
            driver.get(page_url)
            WebDriverWait(driver, PAGE_LOAD_WAIT).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="doctor_search_bar"]'))
            )
        except Exception:
            logger.warning("Search bar not found on page %d. Reconnecting...", page)
            try:
                driver.quit()
            except Exception:
                pass
            ensure_connectivity()
            driver = create_driver()
            try:
                driver = safe_get(driver, page_url, "results")
            except Exception:
                logger.info("End of search results at page %d.", page)
                break

        # Check if results exist on this page
        try:
            driver.find_element(By.CLASS_NAME, "results")
        except Exception:
            logger.info("No more results at page %d. Stopping.", page)
            break

        scroll_page(driver)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        page_links = scrape_search_page(soup)

        if not page_links:
            logger.info("No links found on page %d. Stopping.", page)
            break

        all_links.extend(page_links)
        logger.info("Page %d: found %d links (total: %d).", page, len(page_links), len(all_links))
        page += 1

    try:
        driver.quit()
    except Exception:
        pass

    # Deduplicate while preserving order
    seen = set()
    unique_links = []
    for link in all_links:
        if link not in seen:
            seen.add(link)
            unique_links.append(link)

    logger.info("Phase 1 complete: %d unique profile links collected.", len(unique_links))
    return unique_links


def save_links_csv(links: list[str], filepath: str) -> None:
    """Save profile links to a CSV file."""
    df = pd.DataFrame({"profile_link": links})
    df.to_csv(filepath, index=False)
    logger.info("Links saved to %s.", filepath)


# ---------------------------------------------------------------------------
# Scraping: individual profiles (Phase 2)
# ---------------------------------------------------------------------------


def extract_address(soup: BeautifulSoup) -> str:
    """Extract practice name and address from a profile page."""
    try:
        section = soup.find("div", class_="dl-profile-address-picker-address-text")
        if not section:
            return ""
        divs = section.find_all("div")
        practice_name = divs[1].text.strip() if len(divs) > 1 else ""
        full_address = divs[0].text.strip() if divs else ""
        address = full_address.replace(practice_name, "").strip()
        return f"{practice_name} -> {address}" if practice_name else address
    except (IndexError, AttributeError) as exc:
        logger.debug("Address extraction issue: %s", exc)
        return ""


def extract_skills(soup: BeautifulSoup) -> list[str]:
    """Extract skills list from a profile page."""
    skills = []
    try:
        skills_section = soup.find("div", id="skills")
        if skills_section:
            for chip in skills_section.find_all("div", class_="dl-profile-skill-chip"):
                skills.append(chip.text.strip())
    except AttributeError as exc:
        logger.debug("Skills extraction issue: %s", exc)
    return skills


def extract_degrees(soup: BeautifulSoup) -> list[str]:
    """Extract degrees and achievements from a profile page."""
    degrees = []
    try:
        sections = soup.find_all("div", class_="dl-profile-card-section dl-profile-history")
        for section in sections:
            header = section.find("h4", class_="dl-profile-card-title")
            if header:
                degrees.append(header.text.strip())
                degrees.append("---")

            entries = section.find_all("div", class_="dl-profile-text dl-profile-entry")
            for entry in entries:
                year_el = entry.find("div", class_="dl-profile-entry-time")
                label_el = entry.find("div", class_="dl-profile-entry-label")
                year = year_el.text.strip() if year_el else ""
                label = label_el.text.strip() if label_el else ""
                if year or label:
                    degrees.append(f"{year} - {label}" if year else label)
    except AttributeError as exc:
        logger.debug("Degrees extraction issue: %s", exc)
    return degrees


def extract_contact(soup: BeautifulSoup) -> list[str]:
    """Extract contact info (excluding opening hours) from a profile page."""
    contacts = []
    try:
        contact_section = soup.find("div", id="openings_and_contact")
        if not contact_section:
            return contacts
        for box in contact_section.find_all("div", class_="dl-profile-box"):
            subtitle = box.find("h4", class_="dl-profile-card-subtitle")
            if not subtitle:
                continue
            header_text = subtitle.text.strip()
            if "Horaires d'ouverture" in header_text:
                continue
            content_div = box.find("div")
            content = content_div.text.strip() if content_div else ""
            contacts.append(f"{header_text}: {content}")
    except AttributeError as exc:
        logger.debug("Contact extraction issue: %s", exc)
    return contacts


def scrape_profile(driver: webdriver.Chrome, profile_path: str) -> dict:
    """
    Scrape a single doctor profile page and return extracted data.
    Also visits alternate practice location tabs if available.
    """
    url = f"{BASE_URL}{profile_path}"
    driver = safe_get(driver, url, "dl-profile-header-name")
    scroll_page(driver)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Name
    name_el = soup.find("h1", class_="dl-profile-header-name")
    name = name_el.text.strip() if name_el else "Unknown"

    # Primary location data
    addresses = [extract_address(soup)]
    all_skills = extract_skills(soup)
    all_degrees = extract_degrees(soup)
    contacts = extract_contact(soup)

    # Check for additional practice locations (tabs)
    base_path = profile_path.split("?")[0]
    alt_links = []
    for tag in soup.find_all("a", class_="dl-text", href=True):
        href = tag["href"]
        if base_path in href and href != profile_path:
            alt_links.append(href)

    for alt_link in alt_links:
        alt_url = f"{BASE_URL}{alt_link}"
        driver = safe_get(driver, alt_url, "dl-profile-header-name")
        scroll_page(driver)
        alt_soup = BeautifulSoup(driver.page_source, "html.parser")

        addr = extract_address(alt_soup)
        if addr:
            addresses.append(addr)

        alt_skills = extract_skills(alt_soup)
        all_skills.extend(s for s in alt_skills if s not in all_skills)

        alt_degrees = extract_degrees(alt_soup)
        all_degrees.extend(d for d in alt_degrees if d not in all_degrees)

        alt_contacts = extract_contact(alt_soup)
        contacts.extend(c for c in alt_contacts if c not in contacts)

    return {
        "name": name,
        "addresses": "\n".join(addresses),
        "skills": ", ".join(all_skills),
        "degrees": "\n".join(all_degrees),
        "contacts": "\n".join(contacts),
    }


def scrape_all_profiles(links: list[str]) -> None:
    """Scrape all profiles and progressively save to CSV."""
    logger.info("Phase 2: Scraping %d profiles...", len(links))

    results = []
    driver = create_driver()

    for idx, link in enumerate(links, start=1):
        logger.info("[%d/%d] Scraping: %s", idx, len(links), link)
        try:
            data = scrape_profile(driver, link)
            results.append(data)
            logger.info("  -> %s", data["name"])
        except Exception as exc:
            logger.error("  -> Failed to scrape %s: %s", link, exc)
            results.append({
                "name": "ERROR",
                "addresses": link,
                "skills": "",
                "degrees": "",
                "contacts": str(exc),
            })
            # Recreate driver on failure
            try:
                driver.quit()
            except Exception:
                pass
            ensure_connectivity()
            driver = create_driver()

        # Progressive save every 5 profiles
        if idx % 5 == 0 or idx == len(links):
            df = pd.DataFrame(results)
            df.to_csv(OUTPUT_DETAILS_CSV, index=False)
            logger.info("  -> Progress saved (%d/%d).", idx, len(links))

    try:
        driver.quit()
    except Exception:
        pass

    logger.info("Phase 2 complete: %d profiles scraped.", len(results))


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Main execution flow."""
    print()
    print("=" * 60)
    print("  DoctolibDataScraper")
    print("  by SoClose Society - https://soclose.co")
    print("=" * 60)
    print()

    search_url = input("Enter Doctolib search URL: ").strip()
    if not search_url:
        logger.error("No URL provided. Exiting.")
        sys.exit(1)

    if not search_url.startswith("http"):
        search_url = f"{BASE_URL}{search_url}"

    # Phase 1 - Collect links
    links = scrape_all_search_results(search_url)
    save_links_csv(links, OUTPUT_LINKS_CSV)

    if not links:
        logger.warning("No profile links found. Exiting.")
        sys.exit(0)

    # Phase 2 - Scrape profiles
    scrape_all_profiles(links)

    print()
    print("=" * 60)
    print(f"  Done! {len(links)} profiles scraped.")
    print(f"  Links:   {OUTPUT_LINKS_CSV}")
    print(f"  Details: {OUTPUT_DETAILS_CSV}")
    print("=" * 60)


if __name__ == "__main__":
    main()
