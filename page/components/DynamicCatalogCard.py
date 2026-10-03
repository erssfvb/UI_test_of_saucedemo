from playwright.sync_api import Page
from page.BasePage import BasePage

class DynamicCatalogCard(BasePage):
    def __init__(self, page: Page,item_name:str):
        super().__init__(page)
        self.root = page.locator('.dynamic_catalog_card').filter(has=page.get_by_text(item_name,exact=True))
        self.img = self.root.locator('.dynamic_catalog_card_img')
        self.title = self.root.locator('.dynamic_catalog_card_name')
        self.price = self.root.locator('.dynamic_catalog_card_price')

    #---------页面信息操作---------
    def get_title(self)->str:
        return self.get_text(self.title)

    def get_price(self)->float:
        return float(self.get_text(self.price).lstrip('$'))

    #--------断言操作-----------
    def img_loaded(self):
        natural_width = self.img.evaluate('img => img.naturalWidth')
        assert natural_width > 0
