"""
Flipkart Review Scraper — Infinite Scroll Edition
==================================================
Scrapes ALL reviews from any Flipkart product review page.

Flipkart uses React Native Web (inline styles, no semantic CSS).
Reviews load via IntersectionObserver on scroll — this script handles that.

Usage:
    uv run python scraper.py "https://www.flipkart.com/.../product-reviews/..."
    uv run python scraper.py  # uses default URL

Output:
    flipkart_reviews.csv
"""

import csv
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# ─── Config ───────────────────────────────────────────────────
DEFAULT_URL = "https://www.flipkart.com/apple-iphone-17-pro-silver-256-gb/product-reviews/itm106f475c264c7?pid=MOBHFN6YPFSDYRTY&lid&marketplace=FLIPKART"
OUTPUT_CSV = "flipkart_reviews.csv"
SCROLL_PAUSE = 3          # seconds to wait after each scroll
MAX_NO_NEW_SCROLLS = 7    # stop after this many scrolls with no new reviews
MAX_SCROLLS = 500         # safety limit
# ──────────────────────────────────────────────────────────────


def setup_driver():
    """Launch Chrome with anti-detection settings."""
    opts = Options()
    # Runs headed (visible browser) — headless gets CAPTCHAd by Flipkart
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    )
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)

    # Remove webdriver flag to avoid detection
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    return driver


def extract_reviews_via_js(driver):
    """
    Extract reviews using JavaScript executed in the browser.
    
    Flipkart renders reviews in div.fWi7J_ containers using React Native Web.
    All styling is inline — we match by inline style patterns, not class names.
    """
    js_code = """
    const cards = document.querySelectorAll('div.fWi7J_');
    const reviews = [];
    
    for (const card of cards) {
        try {
            const review = {};
            const allText = card.querySelectorAll('div[dir="auto"]');
            
            // Rating: green text (rgb(14,119,45)) for high ratings
            const ratingEl = card.querySelector('div[style*="color: rgb(14, 119, 45)"]');
            if (!ratingEl) {
                // Orange/red for lower ratings
                const altRating = card.querySelector('div[style*="color: rgb(255,"]') ||
                                  card.querySelector('div[style*="color: rgb(230,"]');
                review.rating = altRating ? altRating.textContent.trim() : '';
            } else {
                review.rating = ratingEl.textContent.trim();
            }
            
            // Title: after the bullet, with flex: 1 1 0% and margin-left: 8px
            const titleEl = card.querySelector(
                'div[style*="margin-left: 8px"][style*="flex: 1 1 0%"]'
            );
            review.title = titleEl ? titleEl.textContent.trim() : '';
            
            // Review variant: "Review for: Color X • Storage Y"
            let reviewFor = '';
            for (const el of allText) {
                if (el.textContent.includes('Review for:')) {
                    reviewFor = el.textContent.trim();
                    break;
                }
            }
            review.review_for = reviewFor;
            
            // Body: inside span.css-1jxf684
            const bodySpan = card.querySelector('span.css-1jxf684');
            review.body = bodySpan ? bodySpan.textContent.trim() : '';
            
            // Fallback: div with padding-bottom: 16px, padding-top: 8px
            if (!review.body) {
                const bodyDiv = card.querySelector(
                    'div[style*="padding-bottom: 16px"][style*="padding-top: 8px"]'
                );
                if (bodyDiv) review.body = bodyDiv.textContent.trim();
            }
            
            // Author: gray text with flex-shrink: 1
            const authorEl = card.querySelector(
                'div[style*="flex-shrink: 1"][style*="color: rgb(133, 137, 143)"]'
            );
            review.author = authorEl ? authorEl.textContent.trim() : '';
            
            // Location: sibling of author, starts with comma
            let location = '';
            if (authorEl && authorEl.nextElementSibling) {
                const locText = authorEl.nextElementSibling.textContent.trim();
                if (locText.startsWith(',')) {
                    location = locText.substring(1).trim();
                }
            }
            review.location = location;
            
            // Reviewer badge: "Gold Reviewer", "Silver Reviewer"
            let badge = '';
            for (const el of allText) {
                const t = el.textContent.trim();
                if (t.includes('Reviewer') && !t.includes('Verified')) {
                    badge = t;
                    break;
                }
            }
            review.badge = badge;
            
            // Helpful count: "Helpful for XXX"
            let helpful = '';
            for (const el of allText) {
                const t = el.textContent.trim();
                if (t.startsWith('Helpful for')) {
                    helpful = t.replace('Helpful for ', '');
                    break;
                }
            }
            review.helpful_count = helpful;
            
            // Unhelpful count: second semi-bold number in the actions area
            const helpfulDivs = [];
            for (const el of allText) {
                const t = el.textContent.trim();
                const style = el.getAttribute('style') || '';
                if (style.includes('inter_semi_bold') && 
                    style.includes('margin-left: 4px') && 
                    style.includes('rgb(113, 116, 120)')) {
                    helpfulDivs.push(t);
                }
            }
            review.unhelpful_count = helpfulDivs.length >= 2 ? helpfulDivs[1] : '';
            
            // Verified Purchase
            let verified = false;
            for (const el of allText) {
                if (el.textContent.includes('Verified Purchase')) {
                    verified = true;
                    break;
                }
            }
            review.verified_purchase = verified;
            
            // Time ago: "· 5 months ago"
            let timeAgo = '';
            for (const el of allText) {
                const t = el.textContent.trim();
                if (t.includes('ago') && t.includes('·')) {
                    timeAgo = t.replace('·', '').trim();
                    break;
                }
            }
            review.time_ago = timeAgo;
            
            // Image count
            const reviewImages = card.querySelectorAll('img[src*="blobio"]');
            review.image_count = reviewImages.length;
            
            // Only real reviews (not header/filter cards)
            if (review.body && review.title && review.rating && 
                (review.rating.match(/^[1-5]\\.0$/) || review.rating.match(/^[1-5]$/))) {
                reviews.push(review);
            }
        } catch(e) {
            console.error('Error parsing card:', e);
        }
    }
    return reviews;
    """
    return driver.execute_script(js_code)


def scroll_and_collect(driver):
    """
    Scroll to load all reviews via infinite scroll.
    
    Flipkart uses IntersectionObserver on a div.CogBpN sentinel element.
    Scrolling it into view triggers the next batch of reviews.
    """
    prev_count = 0
    no_new_count = 0
    scroll_num = 0

    while scroll_num < MAX_SCROLLS:
        scroll_num += 1

        # Scroll sentinel into view (triggers IntersectionObserver)
        driver.execute_script("""
            const sentinel = document.querySelector('div.CogBpN');
            if (sentinel) {
                sentinel.scrollIntoView({behavior: 'smooth'});
            } else {
                window.scrollTo(0, document.body.scrollHeight);
            }
        """)
        time.sleep(SCROLL_PAUSE)

        # Count loaded review cards
        curr_count = driver.execute_script(
            "return document.querySelectorAll('div.fWi7J_').length"
        )

        if curr_count == prev_count:
            no_new_count += 1
            print(
                f"  Scroll {scroll_num}: {curr_count} cards "
                f"(no new — {no_new_count}/{MAX_NO_NEW_SCROLLS})"
            )
            if no_new_count >= MAX_NO_NEW_SCROLLS:
                print(f"\n✅ No new reviews after {MAX_NO_NEW_SCROLLS} scrolls. Done.")
                break
        else:
            new = curr_count - prev_count
            no_new_count = 0
            print(f"  Scroll {scroll_num}: {curr_count} cards (+{new} new)")
            prev_count = curr_count

    return scroll_num


def save_to_csv(reviews, filename):
    """Save reviews to CSV file."""
    if not reviews:
        print("❌ No reviews to save!")
        return

    fieldnames = [
        "index", "rating", "title", "body", "review_for", "author",
        "location", "badge", "helpful_count", "unhelpful_count",
        "verified_purchase", "time_ago", "image_count",
    ]

    for i, r in enumerate(reviews):
        r["index"] = i + 1

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(reviews)

    print(f"\n✅ Saved {len(reviews)} reviews → {filename}")


def print_stats(reviews):
    """Print summary stats."""
    print(f"\n{'─' * 50}")
    print(f"📊 Summary")
    print(f"{'─' * 50}")
    print(f"   Total reviews:      {len(reviews)}")
    print(f"   Verified purchases: {sum(1 for r in reviews if r.get('verified_purchase'))}")
    print(f"   With images:        {sum(1 for r in reviews if r.get('image_count', 0) > 0)}")

    print(f"\n   ⭐ Rating distribution:")
    for star in ["5", "4", "3", "2", "1"]:
        count = sum(1 for r in reviews if str(r.get("rating", "")).startswith(star))
        if count:
            bar = "█" * min(count, 50)
            print(f"      {star}★: {count:>4}  {bar}")
    print(f"{'─' * 50}")


def main():
    # Accept URL as CLI argument or use default
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL

    print("🚀 Flipkart Review Scraper")
    print(f"   URL:    {url}")
    print(f"   Output: {OUTPUT_CSV}")
    print()

    driver = setup_driver()

    try:
        # Load page
        print("📄 Loading page...")
        driver.get(url)
        time.sleep(5)

        # Handle CAPTCHA
        page_src = driver.page_source.lower()
        if "recaptcha" in page_src or "captcha" in page_src:
            print("\n⚠️  CAPTCHA detected!")
            print("   → Solve it in the Chrome window.")
            print("   → Waiting 30s for you to solve it...")
            time.sleep(30)

        # Close login popup
        try:
            close_btn = driver.find_element(
                By.CSS_SELECTOR, "button._2KpZ6l._2doB4z"
            )
            close_btn.click()
            time.sleep(1)
            print("   ✅ Closed login popup")
        except Exception:
            pass

        # Check initial load
        initial = driver.execute_script(
            "return document.querySelectorAll('div.fWi7J_').length"
        )
        print(f"📊 Initial cards loaded: {initial}")

        if initial == 0:
            print("\n❌ No review cards found (div.fWi7J_).")
            print("   Flipkart may have changed their DOM structure.")
            print("   Saving page source to flipkart_debug.html for inspection.")
            with open("flipkart_debug.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            driver.quit()
            return

        # Scroll to load all reviews
        print("\n📜 Scrolling to load all reviews...")
        total_scrolls = scroll_and_collect(driver)

        # Extract
        final_count = driver.execute_script(
            "return document.querySelectorAll('div.fWi7J_').length"
        )
        print(f"\n📦 Extracting data from {final_count} cards...")

        reviews = extract_reviews_via_js(driver)
        print(f"   Got {len(reviews)} valid reviews")

        # Save & stats
        save_to_csv(reviews, OUTPUT_CSV)
        if reviews:
            print_stats(reviews)

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted! Saving what we have...")
        reviews = extract_reviews_via_js(driver)
        if reviews:
            save_to_csv(reviews, OUTPUT_CSV)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        print("\n🔒 Closing browser...")
        driver.quit()
        print("Done! ✅")


if __name__ == "__main__":
    main()
