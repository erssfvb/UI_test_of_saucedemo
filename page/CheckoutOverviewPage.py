from playwright.sync_api import Page, Locator
from dataclasses import dataclass
from page.BasePage import BasePage
from page.components.CartItem import CartItemInCheckoutOverview
from utils.Loader.DataLoader import DataLoader
from utils.paths import PRODUCTS_FILE

@dataclass(frozen=True)
class CheckoutOverviewElement:
    cart_items:Locator
    payment_info:Locator
    shipping_info: Locator
    item_total:Locator
    tax: Locator
    total: Locator
    cancel_button: Locator
    finish_button: Locator


class CheckoutOverviewPage(BasePage):
    _URL = 'https://www.saucedemo.com/checkout-step-two.html'
    _PRODUCTS_DATA = DataLoader(PRODUCTS_FILE)
    _TEXT = {
        "payment_info":"SauceCard #31337",
        "shipping_info":"Free Pony Express Delivery!"
    }
    def __init__(self, page: Page):
        super().__init__(page)
        self.el = CheckoutOverviewElement(
            cart_items = page.locator('.cart_item'),
            payment_info = page.locator('[data-test="payment-info-value"]'),
            shipping_info = page.locator('[data-test="shipping-info-value"]'),
            item_total = page.locator('.summary_subtotal_label'),
            tax = page.locator('.summary_tax_label'),
            total = page.locator('.summary_total_label'),
            cancel_button = page.locator('#cancel'),
            finish_button = page.locator('#finish')
        )

    def _calculate_item_total(self)->float:
        items = self.get_all_items()
        total = float()
        for item in items:
            total += item.get_price()
        return total

    #---------页面信息操作----------
    def get_all_names(self)->list[str]:
        item_name_locator = self.el.cart_items.locator('.inventory_item_name')
        self.assert_visible(item_name_locator.first)
        return item_name_locator.all_inner_texts()

    def get_item_total(self)->float:
        return float(self.get_text(self.el.item_total).strip('Item total: $'))

    def get_tax(self)->float:
        return round(self.get_item_total(),0) * 0.08

    def get_total(self)->float:
        return round(self.get_item_total() + self.get_tax(),2)

    #---------获取子组件操作------
    def get_item_by_name(self,item_name)->CartItemInCheckoutOverview:
        return CartItemInCheckoutOverview(self.page,item_name)

    def get_all_items(self)->list[CartItemInCheckoutOverview]:
        self.assert_visible(self.el.cart_items.first)
        items = list()
        for _ in self.get_all_names():
            items.append(self.get_item_by_name(_))
        return items

    def get_item_by_id(self,id:int)->CartItemInCheckoutOverview:
        return CartItemInCheckoutOverview(self.page,self._PRODUCTS_DATA.get_value(f'Products.{id}.title'))

    #--------跳转操作-----------
    def back_shopping(self):
        from page.InventoryPage import InventoryPage
        self.click(self.el.cancel_button)
        return self._go(InventoryPage)

    def continue_to(self):
        from page.CheckoutCompletePage import CheckoutCompletePage
        self.click(self.el.finish_button)
        return self._go(CheckoutCompletePage)

    #---------断言操作--------
    def assert_item_total(self):
        total = self._calculate_item_total()
        total_text = f"Item total: ${total}"
        self.logger.info(
            f"断言overview页面item total的文本失败,断言值为{total_text},实际的文本为{self.get_text(self.el.item_total)}")
        if not self.assert_contains_text(self.el.item_total,total_text):
            raise ValueError

    def assert_tax(self):
        tax = round(self._calculate_item_total() * 0.08,2)
        tax_text = f"Tax: ${tax}"
        self.logger.info(f"断言overview页面tax的文本失败,断言值为{tax_text},实际的文本为{self.get_text(self.el.tax)}")
        if not self.assert_contains_text(self.el.tax,tax_text):
            raise ValueError

    def assert_total(self):
        total = round(self._calculate_item_total() + round(self._calculate_item_total() * 0.08,2),2)
        total_text = f"Total: ${total}"
        self.logger.info(
            f"断言overview页面total的文本失败,断言值为{total_text},实际的文本为{self.get_text(self.el.total)}")
        if not self.assert_contains_text(self.el.total,total_text):
            raise ValueError

    def assert_paymentInfo(self):
        self.logger.info(f"断言payment_info的文本，预期值为{self._TEXT['payment_info']}")
        if not self.assert_contains_text(self.el.payment_info,self._TEXT['payment_info']):
            raise ValueError

    def assert_shipping_info(self):
        self.logger.info(f"断崖shipping_info的文本。预期值为{self._TEXT['shipping_info']}")
        if not self.assert_contains_text(self.el.shipping_info,self._TEXT['shipping_info']):
            raise ValueError







