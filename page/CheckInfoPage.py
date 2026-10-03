from playwright.sync_api import Page, expect

from page.BasePage import BasePage
from page.components.Footer import Footer
from page.components.Header import Header

class CheckInfoPage(BasePage):
    _TEXT = {
        "cancel_button":"Cancel",
        "continue_button":"Continue"
    }
    _URL = 'https://www.saucedemo.com/checkout-step-one.html'
    _NEXT_URL = 'https://www.saucedemo.com/checkout-step-two.html'
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = Header(page)
        self.footer = Footer(page)
        self.firstname = page.locator('#first-name')
        self.lastname = page.locator('#last-name')
        self.postal_code = page.locator('#postal-code')
        self.cancel_button = page.locator('#cancel')
        self.continue_button = page.locator('#continue')
        self.error_message = page.locator('[data-test="error"]')

    #----------结账信息填写操作----------

    def fill_info(self,firstname:str,lastname:str,postal_code:str):
        self.fill(self.firstname, firstname)
        self.fill(self.lastname, lastname)
        self.fill(self.postal_code, postal_code)

    def submit(self):
        from page.CheckoutOverviewPage import CheckoutOverviewPage
        self.click(self.continue_button)
        return self._go(CheckoutOverviewPage)

    def assert_error_text(self,text):
        if not self.assert_contains_text(self.error_message,text):
            self.logger(f"断言结账信息错误提示失败")

    def clear(self):
        self.fill_info('','','')

    #----------跳转页面操作----------
    def cancel(self):
        from page.CartPage import CartPage
        self.click(self.cancel_button)
        return self._go(CartPage)