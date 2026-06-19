from playwright.async_api import async_playwright


class BrowserManager:

    def __init__(self):
        self.playwright = None
        self.browser = None

    async def start(self):

        self.playwright = (
            await async_playwright().start()
        )

        self.browser = (
            await self.playwright.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                ]
            )
        )

        return self.browser

    async def stop(self):

        if self.browser:
            await self.browser.close()

        if self.playwright:
            await self.playwright.stop()