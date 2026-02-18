<p align="center">
  <h1 align="center">DoctolibDataScraper</h1>
  <p align="center">
    <strong>Free open-source Doctolib.fr web scraper</strong><br>
    Extract doctor profiles, addresses, skills &amp; degrees automatically with Python.
  </p>
  <p align="center">
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9%2B-3776AB.svg?logo=python&logoColor=white" alt="Python 3.9+"></a>
    <a href="https://www.selenium.dev/"><img src="https://img.shields.io/badge/Selenium-WebDriver-43B02A.svg?logo=selenium&logoColor=white" alt="Selenium"></a>
    <a href="https://soclose.co"><img src="https://img.shields.io/badge/by-SoClose-575ECF.svg" alt="Made by SoClose"></a>
    <a href="https://github.com/SoCloseSociety/DoctolibDataScraper/stargazers"><img src="https://img.shields.io/github/stars/SoCloseSociety/DoctolibDataScraper?style=social" alt="GitHub Stars"></a>
  </p>
</p>

---

> Built by **[SoClose](https://soclose.co)** — Digital solutions & software development studio specializing in automation and AI integration.

---

## Why DoctolibDataScraper?

Manually collecting doctor information from [Doctolib.fr](https://www.doctolib.fr) is time-consuming. This Python web scraper automates the entire process: give it a Doctolib search URL, and it extracts every doctor profile into clean, analysis-ready CSV files.

### What it extracts

| Data Field | Example |
|------------|---------|
| **Name** | Dr. Marie Dupont |
| **Addresses** | All practice locations with full addresses |
| **Skills** | Medical specializations, competencies |
| **Degrees** | Diplomas, certifications, education history |
| **Contacts** | Phone numbers, additional contact details |

### How it works

```
Doctolib Search URL
        │
        ▼
┌─────────────────────┐
│  Phase 1: Crawl     │──→ doctolib_profile_link.csv
│  Paginated results   │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Phase 2: Scrape    │──→ doctolib_profile_details.csv
│  Each doctor profile │
└─────────────────────┘
```

---

## Key Features

- **Full pagination** — Automatically crawls all search result pages
- **Multi-location** — Scrapes every practice location per doctor
- **VPN rotation** — Built-in NordVPN CLI support to avoid rate limiting *(optional)*
- **Progressive saving** — Data saved every 5 profiles, no loss on crash
- **Auto-recovery** — Handles connection drops with smart retry logic
- **Cross-platform** — Windows, macOS, and Linux
- **Clean CSV output** — Ready to import in Excel, Google Sheets, or any data tool

---

## Quick Start

### Prerequisites

| Requirement | Link |
|-------------|------|
| Python 3.9+ | [python.org/downloads](https://www.python.org/downloads/) |
| Google Chrome | [google.com/chrome](https://www.google.com/chrome/) |
| NordVPN CLI *(optional)* | For IP rotation during large scrapes |

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

### Run

```bash
python main.py
```

Enter a Doctolib search URL when prompted:

```
============================================================
  DoctolibDataScraper
  by SoClose Society - https://soclose.co
============================================================

Enter Doctolib search URL: https://www.doctolib.fr/medecin-generaliste/paris
```

### Output

| File | Content |
|------|---------|
| `doctolib_profile_link.csv` | All unique doctor profile links |
| `doctolib_profile_details.csv` | Full structured profile data |
| `scraper.log` | Timestamped execution log |

---

## NordVPN Setup *(Optional)*

VPN support helps avoid rate limiting during large scraping sessions.

<details>
<summary><strong>Windows</strong></summary>

1. Install [NordVPN](https://nordvpn.com/)
2. Add NordVPN to your PATH: `C:\Program Files\NordVPN\`
3. Verify in Command Prompt: `nordvpn -c`

</details>

<details>
<summary><strong>macOS</strong></summary>

1. Install NordVPN via [nordvpn.com](https://nordvpn.com/) or `brew install nordvpn`
2. Verify in Terminal: `nordvpn connect`

</details>

<details>
<summary><strong>Linux</strong></summary>

1. Install: `sh <(curl -sSf https://downloads.nordcdn.com/apps/linux/install.sh)`
2. Login: `nordvpn login`
3. Verify: `nordvpn connect`

</details>

---

## Tech Stack

| Technology | Role |
|------------|------|
| [Python](https://www.python.org/) | Core language |
| [Selenium](https://www.selenium.dev/) | Browser automation & page interaction |
| [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) | HTML parsing & data extraction |
| [Pandas](https://pandas.pydata.org/) | Data structuring & CSV export |
| [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) | Automatic ChromeDriver management |

---

## Project Structure

```
DoctolibDataScraper/
├── main.py              # Main scraper application
├── requirements.txt     # Python dependencies
├── .gitignore           # Git ignore rules
├── LICENSE              # MIT License
├── README.md            # Documentation
└── CONTRIBUTING.md      # Contribution guidelines
```

---

## Other Open-Source Tools by SoClose

| Project | Description | Stars |
|---------|-------------|-------|
| [PinterestBulkPostBot](https://github.com/SoCloseSociety/PinterestBulkPostBot) | Free Pinterest bulk upload bot — automate posting hundreds of pins | ![Stars](https://img.shields.io/github/stars/SoCloseSociety/PinterestBulkPostBot?style=flat-square) |
| [LinkedinDataScraper](https://github.com/SoCloseSociety/LinkedinDataScraper) | Scrape contact info from LinkedIn profiles | ![Stars](https://img.shields.io/github/stars/SoCloseSociety/LinkedinDataScraper?style=flat-square) |
| [InstagramDataScraper](https://github.com/SoCloseSociety/InstagramDataScraper) | Scrape Instagram profile data | ![Stars](https://img.shields.io/github/stars/SoCloseSociety/InstagramDataScraper?style=flat-square) |
| [BOT_GoogleMap_Scrapping](https://github.com/SoCloseSociety/BOT_GoogleMap_Scrapping) | Scrape data from Google Maps | ![Stars](https://img.shields.io/github/stars/SoCloseSociety/BOT_GoogleMap_Scrapping?style=flat-square) |
| [FreeWorkDataScraper](https://github.com/SoCloseSociety/FreeWorkDataScraper) | Scrape job postings from FreeWork | ![Stars](https://img.shields.io/github/stars/SoCloseSociety/FreeWorkDataScraper?style=flat-square) |

**[See all repositories →](https://github.com/SoCloseSociety?tab=repositories)**

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Quick start:** Fork → Branch → Code → PR against `main`

---

## Disclaimer

This tool is for **educational and research purposes only**. Respect Doctolib's [Terms of Service](https://www.doctolib.fr/terms) and applicable data protection laws (GDPR). The authors are not responsible for any misuse.

---

## License

[MIT License](LICENSE) — Copyright (c) 2022-2026 [SoClose](https://soclose.co)

---

<p align="center">
  <a href="https://soclose.co"><strong>SoClose</strong></a> · Digital solutions & software development studio<br>
  <a href="https://soclose.co">Website</a> · <a href="https://github.com/SoCloseSociety">GitHub</a> · <a href="mailto:contact@soclose.co">contact@soclose.co</a><br><br>
  <em>If this tool helped you, give it a</em> <a href="https://github.com/SoCloseSociety/DoctolibDataScraper/stargazers">star</a> ⭐
</p>
