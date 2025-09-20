import undetected_chromedriver as uc
from selenium_stealth import stealth
import time

url = "https://macrotrends.net/stocks/charts/NVDA/nvidia/shares-outstanding"

options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")

driver = uc.Chrome(
    version_main=138,  # Match your Chrome version
    options=options,
    headless=False  # Start with visible browser for debugging
)

# Apply stealth settings
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

try:
    driver.get(url)
    
    # Handle potential Cloudflare challenge
    if "Just a moment" in driver.title:
        print("Cloudflare challenge detected. Waiting...")
        time.sleep(15)  # Increase wait time for challenge
    
    # Wait for page content to load
    time.sleep(8)
    
    # Check if we're still blocked
    if "Verifying" in driver.page_source:
        print("Still blocked by Cloudflare. Trying additional measures...")
        # Try refreshing with cookies
        driver.refresh()
        time.sleep(15)
    
    # Save final page source
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("Page source saved successfully!")

except Exception as e:
    print("Error:", e)
    # Save error page for debugging
    with open("error_page.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

finally:
    driver.quit()