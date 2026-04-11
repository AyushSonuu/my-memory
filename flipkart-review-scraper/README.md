# Flipkart Review Scraper

Scrape **all** reviews from any Flipkart product page. Handles infinite scroll, CAPTCHA detection, and Flipkart's React Native Web DOM.

## Output

`flipkart_reviews.csv` with columns:

| Column | Example |
|--------|---------|
| rating | 5.0 |
| title | Classy product |
| body | Battery is long lasting and... |
| review_for | Color Deep Blue • Storage 256 GB |
| author | Akash Lahariya |
| location | Jabalpur |
| badge | Gold Reviewer |
| helpful_count | 73 |
| unhelpful_count | 25 |
| verified_purchase | True |
| time_ago | 1 month ago |
| image_count | 4 |

---

## Prerequisites

- **Python 3.9+**
- **Google Chrome** installed on your machine
- **uv** (fast Python package manager) — [install guide](https://docs.astral.sh/uv/getting-started/installation/)

### Install uv (if you don't have it)

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## Quick Start (3 commands)

```bash
# 1. Clone / download this folder
cd flipkart-review-scraper

# 2. Install dependencies (uv creates a virtual env automatically)
uv sync

# 3. Run the scraper
uv run python scraper.py
```

That's it. Chrome will open, scroll through all reviews, and save `flipkart_reviews.csv`.

---

## Usage

### Default URL (iPhone 17 Pro reviews)

```bash
uv run python scraper.py
```

### Custom URL (any Flipkart product)

```bash
uv run python scraper.py "https://www.flipkart.com/your-product/product-reviews/xxx?pid=YYY"
```

> **Tip:** Go to any Flipkart product → click "All Reviews" → copy that URL.

---

## How It Works

```
1. Opens Chrome (visible — headless gets CAPTCHAd)
2. Loads the review page
3. If CAPTCHA appears → waits 30s for you to solve it manually
4. Scrolls the IntersectionObserver sentinel (div.CogBpN) into view
5. Each scroll loads ~10 more reviews
6. Stops when no new reviews load after 7 consecutive scrolls
7. Extracts all data via JavaScript (runs inside the browser)
8. Saves to CSV
```

---

## Configuration

Edit these constants at the top of `scraper.py`:

| Variable | Default | What it does |
|----------|---------|-------------|
| `SCROLL_PAUSE` | 3 | Seconds to wait between scrolls |
| `MAX_NO_NEW_SCROLLS` | 7 | Stop after N scrolls with no new reviews |
| `MAX_SCROLLS` | 500 | Safety limit (won't scroll forever) |

**Slow internet?** Increase `SCROLL_PAUSE` to 5.

---

## CAPTCHA

Flipkart sometimes shows a CAPTCHA on first load. If that happens:

1. The script will detect it and print a warning
2. **Solve the CAPTCHA manually** in the Chrome window that opened
3. The script waits 30 seconds, then continues automatically

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `chromedriver` version mismatch | `webdriver-manager` auto-downloads the right version |
| No reviews found | Flipkart may have changed their DOM — open an issue |
| CAPTCHA keeps appearing | Try again after a few minutes, or use a different network |
| Reviews stop loading early | Increase `SCROLL_PAUSE` to 5 or `MAX_NO_NEW_SCROLLS` to 10 |
| `Chrome not found` | Install Google Chrome from https://www.google.com/chrome/ |

---

## Project Structure

```
flipkart-review-scraper/
├── pyproject.toml     # Dependencies + metadata
├── scraper.py         # The scraper script
├── README.md          # This file
└── .python-version    # Python version pin
```

---

## License

MIT — do whatever you want with it.
