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
            # 1. Capture AI Assistant Interaction (This will be our primary showcase)
            print("📸 Capturing AI Assistant Interaction...")
            await page.goto("http://localhost:8501")
            time.sleep(10) # Wait for initial load and index check
            
            await page.fill("input[placeholder*='Ask about a']", "Who are the top 2026 artists and why?")
            await page.keyboard.press("Enter")
            print("⏳ Waiting for AI response...")
            time.sleep(15) # Wait for LLM to finish streaming
            await page.screenshot(path="showcase/02_chatbot_answer.png")
            
            # 2. Capture Analytics Dashboard
            print("📸 Capturing Analytics Dashboard...")
            # Using a more robust selector for Streamlit tabs
            await page.click("button:has-text('Analytics')")
            time.sleep(8) # Wait for Plotly charts to render
            await page.screenshot(path="showcase/03_analytics_view.png")
            
            # 3. Capture Jukebox
            print("📸 Capturing Jukebox...")
            await page.click("button:has-text('AI Assistant')") # Switch back
            time.sleep(2)
            await page.click("text=Jukebox")
            await page.click("text=Shuffle & Pick!")
            time.sleep(5) # Wait for random selection and thumbnail
            await page.screenshot(path="showcase/04_jukebox.png")

            # 4. Capture Infinite Scraper
            print("📸 Capturing Infinite Scraper Dashboard...")
            await page.goto("http://localhost:8502")
            time.sleep(10) # Wait for scraper UI to load
            await page.screenshot(path="showcase/05_scraper_ui.png")
            
            # 5. Backup of main landing
            await page.goto("http://localhost:8501")
            time.sleep(5)
            await page.screenshot(path="showcase/01_chatbot_main.png")
            
            print("\n✅ All assets captured in 'showcase/' directory!")
            print("👉 You can now commit these to GitHub to see them in your README.")
            
        except Exception as e:
            print(f"\n❌ Error during capture: {e}")
            print("💡 TIP: Ensure your apps are running on ports 8501 and 8502.")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_showcase())
