import asyncio
import logging
import os
from typing import List

from playwright.async_api import async_playwright
from datetime import datetime

logger = logging.getLogger(__name__)

async def run_nfpa_with_handler(query: str | None = None) -> List[str]:
    headless_env = os.getenv("HEADLESS", "true").lower() not in ("0", "false", "no")
    search_term = query or os.getenv("NFPA_QUERY", "NFPA 70")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    trace_path = os.getenv("TRACE_PATH", f"./app/log/nfpa_handler_trace_{timestamp}.zip")
    trace_dir = os.path.dirname(trace_path)
    if trace_dir:
        os.makedirs(trace_dir, exist_ok=True)
    logger.info(
        "nfpa run start headless=%s query=%s trace=%s",
        headless_env,
        search_term,
        trace_path,
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless_env)
        context = await browser.new_context()
        await context.tracing.start(screenshots=True, snapshots=True)
        page = await context.new_page()

        cookie_selector = 'button:has-text("Accept"), button:has-text("OK"), .optanon-allow-all'

        await page.add_locator_handler(
            page.locator(cookie_selector).first,
            lambda: page.locator(cookie_selector).first.click()
        )

        try:
            logger.info("访问首页...")
            await page.goto("https://www.nfpa.org", wait_until="domcontentloaded")

            search_trigger = page.get_by_label("Search", exact=False).first
            await search_trigger.click()

            await page.locator('input[type="search"]').fill(search_term)
            await page.keyboard.press("Enter")

            products_btn = page.locator("button.listing_toolboxTabBtn__PgiHd").filter(has_text="Products")
            await products_btn.wait_for(state="visible", timeout=30000)
            await products_btn.click()

            logger.info("成功点击 Products 按钮，正在提取标题...")
            title_locators = page.locator("div.cardTitle")
            await title_locators.first.wait_for(state="attached")

            all_titles = await title_locators.all()
            results: List[str] = []
            for index, title in enumerate(all_titles):
                text = await title.inner_text()
                clean_text = text.strip()
                results.append(clean_text)
                logger.info("nfpa title index=%s title=%s", index + 1, clean_text)

            logger.info("nfpa run done count=%s", len(results))
            return results

        finally:
            await context.tracing.stop(path=trace_path)
            await browser.close()


if __name__ == "__main__":
    asyncio.run(run_nfpa_with_handler())
