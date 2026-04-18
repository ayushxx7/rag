import asyncio
from playwright.async_api import async_playwright
import os
import time

async def capture_showcase():
    async with async_playwright() as p:
        # Launch browser (headless for speed)
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        
        # Ensure directory exists
        os.makedirs("showcase", exist_ok=True)
        
        print("🎬 Starting Master UI Capture...")
        
        try:
            # 1. Capture Bot Main
            print("📸 Capturing Genius Bot...")
            await page.goto("http://localhost:8501")
            time.sleep(6) # Wait for rebuild/init
            await page.screenshot(path="showcase/01_chatbot_main.png", full_page=False)
            
            # 2. Capture Bot Interaction
            await page.fill("input[placeholder*='Ask about a']", "Who are the top 2026 artists?")
            await page.keyboard.press("Enter")
            time.sleep(10) # Wait for LLM
            await page.screenshot(path="showcase/02_chatbot_answer.png")
            
            # 3. Capture Analytics Dashboard
            print("📸 Capturing Magic Analytics...")
            # Click the second tab (Analytics)
            await page.click("text=Magic Analytics")
            time.sleep(3)
            await page.screenshot(path="showcase/03_analytics_view.png")
            
            # 4. Capture Jukebox
            print("📸 Capturing Magic Jukebox...")
            await page.click("text=Genius Bot") # Switch back
            await page.click("text=Magic Jukebox")
            await page.click("text=Shuffle & Pick!")
            time.sleep(2)
            await page.screenshot(path="showcase/04_jukebox.png")

            # 5. Capture Scraper
            print("📸 Capturing Infinite Scraper Dashboard...")
            await page.goto("http://localhost:8502")
            time.sleep(4)
            await page.screenshot(path="showcase/05_scraper_ui.png")
            
            print("\n✅ All assets captured in 'showcase/' directory!")
            print("👉 You can now commit these to GitHub to see them in your README.")
            
        except Exception as e:
            print(f"\n❌ Error during capture: {e}")
            print("💡 TIP: Ensure your apps are running on ports 8501 and 8502.")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_showcase())
