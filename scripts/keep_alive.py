import os
import time
from playwright.sync_api import sync_playwright

def wake_up():
    url = os.environ.get("STREAMLIT_APP_URL")
    if not url:
        print("Error: STREAMLIT_APP_URL environment variable not set.")
        return

    print(f"Checking Streamlit app at: {url}")
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            # Visit the app
            page.goto(url, wait_until="networkidle", timeout=60000)
            
            # Check for the "Wake up this app" button
            # Streamlit Cloud's "Your app is sleeping" page typically has this button.
            wake_up_button = page.get_by_text("Wake up this app", exact=False)
            
            if wake_up_button.is_visible():
                print("App is sleeping. Clicking 'Wake up' button...")
                wake_up_button.click()
                # Wait for the app to load
                page.wait_for_selector('div[data-testid="stAppViewContainer"]', timeout=90000)
                print("App woke up successfully!")
            else:
                # Check if it's already awake by looking for a common streamlit element
                if page.locator('div[data-testid="stAppViewContainer"]').is_visible():
                    print("App is already awake and running.")
                else:
                    print("App is not sleeping, but I couldn't find the main app container. It might still be loading.")
                    # Take a screenshot for debugging (optional in GitHub Actions if we upload it)
                    page.screenshot(path="app_status.png")
                    print("Screenshot saved as app_status.png")
                    
        except Exception as e:
            print(f"An error occurred: {e}")
            page.screenshot(path="error_screenshot.png")
            print("Error screenshot saved.")
        finally:
            browser.close()

if __name__ == "__main__":
    wake_up()
