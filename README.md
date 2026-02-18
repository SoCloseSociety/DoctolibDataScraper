# DoctolibDataScraper

**Automated web scraper for extracting doctor profile data from [Doctolib.fr](https://www.doctolib.fr)**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-WebDriver-green.svg)](https://www.selenium.dev/)
[![Made by SoClose Society](https://img.shields.io/badge/Made%20by-SoClose%20Society-purple.svg)](https://soclose.co)

> An open-source project by **[SoClose Society](https://soclose.co)** — Building and sharing developer tools for the community.

---

## Overview

DoctolibDataScraper automates the collection of healthcare provider data from Doctolib search results. It navigates through paginated search results, collects profile links, then visits each profile to extract structured information.

### What it extracts

| Field | Description |
|-------|-------------|
| **Name** | Doctor's full name |
| **Addresses** | Practice locations with full addresses |
| **Skills** | Listed medical specializations and competencies |
| **Degrees** | Educational background, diplomas, and certifications |
| **Contacts** | Phone numbers and other contact details |

### How it works

```
Search URL → [Phase 1] Collect Links → [Phase 2] Scrape Profiles → CSV Output
```

1. **Phase 1** — Iterates through all search result pages and collects unique profile links → `doctolib_profile_link.csv`
2. **Phase 2** — Visits each profile (including alternate practice locations) and extracts structured data → `doctolib_profile_details.csv`

---

## Features

- **Pagination handling** — Automatically navigates through all search result pages
- **Multi-location support** — Scrapes data from all practice locations per doctor
- **VPN integration** — Built-in NordVPN CLI support for IP rotation (optional)
- **Progressive saving** — Saves data every 5 profiles to prevent data loss
- **Auto-recovery** — Handles connection failures with automatic retry logic
- **Cross-platform** — Works on Windows, macOS, and Linux
- **Clean output** — Structured CSV files ready for analysis

---

## Quick Start

### Prerequisites

- **Python 3.9+** — [Download](https://www.python.org/downloads/)
- **Google Chrome** — [Download](https://www.google.com/chrome/)
- **NordVPN CLI** *(optional)* — For VPN-based IP rotation

### Installation

```bash
# Clone the repository
git clone https://github.com/SoCloseSociety/DoctolibDataScraper.git
cd DoctolibDataScraper

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
python main.py
```

When prompted, enter a Doctolib search URL:

```
Enter Doctolib search URL: https://www.doctolib.fr/medecin-generaliste/paris
```

The scraper will:
1. Collect all profile links from search results
2. Visit each profile and extract data
3. Save results to CSV files in the project directory

### Output Files

| File | Content |
|------|---------|
| `doctolib_profile_link.csv` | All unique profile links found |
| `doctolib_profile_details.csv` | Full extracted profile data |
| `scraper.log` | Execution log with timestamps |

---

## NordVPN Setup (Optional)

VPN support helps avoid rate limiting during large scraping sessions.

<details>
<summary><strong>Windows</strong></summary>

1. Install [NordVPN](https://nordvpn.com/)
2. Add NordVPN to your PATH: `C:\Program Files\NordVPN\`
3. Verify: `nordvpn -c` in Command Prompt

</details>

<details>
<summary><strong>macOS</strong></summary>

1. Install NordVPN via [official site](https://nordvpn.com/) or `brew install nordvpn`
2. Verify: `nordvpn connect` in Terminal

</details>

<details>
<summary><strong>Linux</strong></summary>

1. Install: `sh <(curl -sSf https://downloads.nordcdn.com/apps/linux/install.sh)`
2. Login: `nordvpn login`
3. Verify: `nordvpn connect`

</details>

---

## Project Structure

```
DoctolibDataScraper/
├── main.py              # Main scraper application
├── requirements.txt     # Python dependencies
├── .gitignore           # Git ignore rules
├── LICENSE              # MIT License
├── README.md            # This file
└── CONTRIBUTING.md      # Contribution guidelines
```

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| [Selenium](https://www.selenium.dev/) | Browser automation and page interaction |
| [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) | HTML parsing and data extraction |
| [Pandas](https://pandas.pydata.org/) | Data structuring and CSV export |
| [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) | Automatic ChromeDriver management |

---

## Disclaimer

This tool is intended for **educational and research purposes only**. Please respect Doctolib's [Terms of Service](https://www.doctolib.fr/terms) and applicable data protection laws (GDPR). Use responsibly and ethically. The authors are not responsible for any misuse of this software.

---

## Contributing

We welcome contributions from the community! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## About SoClose Society

**[SoClose Society](https://soclose.co)** is a developer collective dedicated to building and sharing open-source tools with the community. We believe in collaborative development and making useful software accessible to everyone.

- **Website:** [soclose.co](https://soclose.co)
- **GitHub:** [github.com/SoCloseSociety](https://github.com/SoCloseSociety)

### Other Projects

Explore our other open-source projects on our [GitHub organization](https://github.com/SoCloseSociety).

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

Copyright (c) 2022-2026 [SoClose Society](https://soclose.co)

---

<p align="center">
  <strong>Built with purpose by <a href="https://soclose.co">SoClose Society</a></strong><br>
  <em>Open source. Community driven. Always free.</em>
</p>
