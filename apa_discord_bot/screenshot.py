import os
from urllib.parse import urljoin
import asyncio
from playwright.async_api import async_playwright


async def take_screenshot():
    async with async_playwright() as p:
        # Launch the browser
        browser = await p.chromium.launch(headless=True)  # Set headless=False if you want the browser UI
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        
        # Open a new page
        page = await context.new_page()

        # Navigate to the desired URL
        file_path = os.path.abspath('matchup.html')
        file_url = urljoin('file://', file_path)
        await page.goto(file_url)

        # Take screenshots of 8/9-ball matchup containers
        await page.get_by_text("8-Ball Matchup Player").screenshot(path='8ball_ss.png')
        await page.get_by_text("9-Ball Matchup Player").screenshot(path='9ball_ss.png')

        await browser.close()

# Run the script
def start_func():
    asyncio.run(take_screenshot())

if __name__ == "__main__":
    start_func()