from playwright.sync_api import Page
from page.BasePage import BasePage
from page.registry import registry

@registry('Lazy Load')
class DynamicCatalogLazyLoadPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.cards = page.locator('.dynamic_catalog_card')

