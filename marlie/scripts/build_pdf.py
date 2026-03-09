"""
Convert MARLIE-I-Investor-Deck-SHARE.html to PDF using Playwright/Chromium.
"""
import sys, asyncio
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HTML = Path(r"c:\Users\adhsc\OneDrive\Documents\GitHub\gpu-learning-lab\marlie\MARLIE-I-Investor-Deck-SHARE.html")
PDF  = Path(r"c:\Users\adhsc\OneDrive\Documents\GitHub\gpu-learning-lab\marlie\MARLIE-I-Investor-Deck.pdf")

async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(HTML.as_uri(), wait_until="networkidle")
        # Give JS (SVG rack render, calc) time to finish
        await page.wait_for_timeout(2000)
        await page.pdf(
            path=str(PDF),
            format="A4",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
        )
        await browser.close()
    size_mb = PDF.stat().st_size / 1_048_576
    print(f"Done: {PDF}")
    print(f"Size: {size_mb:.1f} MB")

asyncio.run(main())
