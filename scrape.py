from playwright.sync_api import sync_playwright

def fetch_chapter(url="https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        print(f"Opening URL: {url}")
        page.goto(url)
        
        # Take a full-page screenshot
        page.screenshot(path="chapter1_screenshot.png", full_page=True)
        print("✅ Screenshot saved as 'chapter1_screenshot.png'")

        # Extract main content text
        text = page.inner_text("body")
        print("✅ Chapter text extracted.")
        
        browser.close()
        return text
