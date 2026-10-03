from playwright.sync_api import Page, expect

from page.BasePage import BasePage
from page.components.Header import Header
from page.components.Footer import Footer

class InventoryDetailPage(BasePage):
    _URL = 'https://www.saucedemo.com/inventory-item.html?id='
    _TEXT = {
        'add':'Add to cart',
        'remove':'Remove'
    }
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = Header(page)
        self.footer = Footer(page)
        self.root = page.locator('.inventory_details_container')
        self.back_button = page.locator('#back-to-products')
        self.img = page.locator('.inventory_details_img')
        self.title = page.locator('.inventory_details_name')
        self.desc = page.locator('.inventory_details_desc')
        self.price = page.locator('.inventory_details_price')
        self.add_or_remove_button = page.locator('.btn_inventory')

    #------页面信息操作--------
    def get_name(self)->str:
        """
        返回当前页面标题文本
        :return:
        """
        return self.get_text(self.title)

    def get_desc(self)->str:
        """
        返回当前页面的描述文本
        :return:
        """
        return self.get_text(self.desc)

    def get_price(self)->float:
        """
        返回当前页面商品的价格
        :return:
        """
        return float(self.get_text(self.price))

    def get_all_info(self)->list[str]:
        """
        按页面返回一个包含所有文本的列表[title,desc,price,button_test]
        :return:
        """
        page_info = self.root.all_inner_texts()
        return page_info[0].split('\n')

    #----------购物车--------------
    def add_cart(self):
        self.assert_contains_text(self.add_or_remove_button,self._TEXT['add'])
        self.click(self.add_or_remove_button)

    def remove(self):
        self.assert_contains_text(self.add_or_remove_button,self._TEXT['remove'])
        self.click(self.add_or_remove_button)


    #---------跳转操作-----------
    def back_InventoryPage(self):
        from page.InventoryPage import InventoryPage
        self.click(self.back_button)
        return self._go(InventoryPage)


    #----------断言操作-------
    def expect_img_loaded(self)->bool:
        """
        等待图片加载完成并且naturalWidth大于0，断言图片的natural_width大于0，这段代码是assert断言，抛出AssertionError
        :return:
        """
        try:
            self.assert_visible(self.img)
            handle = self.img.element_handle()
            self.page.wait_for_function(
                "el => el.complete && el.naturalWidth > 0",
                arg=handle,
            )
            natural_width = self.img.evaluate("el => el.naturalWidth")
            print(natural_width)
            assert natural_width > 0
            return True
        except AssertionError:
            self.logger.info(f"断言图片加载成功失败")
            return False
