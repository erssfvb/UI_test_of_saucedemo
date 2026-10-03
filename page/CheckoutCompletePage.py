from page.BasePage import BasePage
from playwright.sync_api import Locator,Page
from page.components.Header import Header
from page.components.Footer import Footer

class CheckoutCompletePage(BasePage):
    _URL = 'https://www.saucedemo.com/checkout-complete.html'
    _TEXT = {
        "complete_header":"Thank you for your order!",
        "back_home":"Back Home",
        "generate_pdf_order":"Generate PDF order"
    }
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = Header(page)
        self.footer = Footer(page)
        self.complete_header = page.locator('.complete-header')
        self.back_home = page.locator('#back-to-products')
        self.generate_pdf_order = page.locator('#generate-pdf-order')

    def back_home_click(self):
        from page.InventoryPage import InventoryPage
        self.click(self.back_home)
        return self._go(InventoryPage)

    def expect_complete_header(self):
        self.assert_contains_text(self.complete_header,self._TEXT['complete_header'])