from dataclasses import dataclass
from playwright.sync_api import Page, Locator, expect
from page.registry import registry
from page.BasePage import BasePage
from utils.paths import PRODUCTS_FILE
from utils.Loader.DataLoader import DataLoader


@dataclass(frozen=True)
class InventoryItemElement:
    item_img:Locator
    item_title:Locator
    item_desc:Locator
    item_price:Locator
    item_button:Locator

class InventoryItem(BasePage):
    _TEXT = {
        'add':'Add to cart',
        'remove':'Remove'
    }
    _PRODUCTS_DATA = DataLoader(PRODUCTS_FILE)
    def __init__(self, page: Page, item_name):
        super().__init__(page)
        self.root = page.locator('.inventory_item').filter(
            has=page.get_by_text(item_name,exact=True)
        )
        self.el = InventoryItemElement(
            item_img=self.root.locator('img.inventory_item_img'),
            item_title=self.root.locator('.inventory_item_name '),
            item_desc=self.root.locator('.inventory_item_desc'),
            item_price=self.root.locator('.inventory_item_price'),
            item_button=self.root.locator('.btn_inventory')
        )
    #-------------购物车模块--------------
    def add_cart(self):
        """
        如果当前商品不在购物车，按钮会是Add to cart文本，这时候可以将商品添加到购物车，否则断言失败
        :return:
        """
        expect(self.el.item_button).to_have_text(self._TEXT['add'])
        self.click(self.el.item_button)


    def remove_from_cart(self):
        """
        如果当前商品在购物车，按钮会是Remove文本，这时候可以将商品从购物车中移除，否则断言失败
        :return:
        """
        expect(self.el.item_button).to_have_text(self._TEXT['remove'])
        self.click(self.el.item_button)

    #------------获取页面信息-------------

    def get_all_info(self)->list[str]:
        """
        按页面返回一个包含所有子组件文本的列表[title,desc,price,button_test]
        :return:
        """
        page_info = self.root.all_inner_texts()
        return page_info[0].split('\n')

    def get_product_info(self)->list[str]:
        return self.get_all_info()[0:3]

    def get_price(self)->float:
        """
        获取item的价格
        :return:
        """
        return float(self.get_text(self.el.item_price).lstrip('$'))

    def get_title(self)->str:
        """
        获取item的标题
        :return:
        """
        return self.get_text(self.el.item_title)

    def get_desc(self)->str:
        """
        获取item的秒速
        :return:
        """
        return self.get_text(self.el.item_desc)

    def get_button_text(self)->str:
        """
        获取item的按钮文本
        :return:
        """
        return self.get_text(self.el.item_button)



    #--------------跳转操作--------------
    def enter_detail(self,option:str='title'):
        """
        跳转到商品的详细页，option分别对应从图片跳转还是标题跳转
        :param option: ['img','title']
        :return:
        """
        from page.InventoryDetailPage import InventoryDetailPage
        if option == 'img':
            self.click(self.el.item_img)
        elif option == 'title':
            self.click(self.el.item_title)
        self.page.locator('.inventory_item_container').wait_for(state='visible')
        return self._go(InventoryDetailPage)

    #-------------断言功能------------
    def expect_button_text(self,text:str):
        """
        断言按钮文本
        :param text:
        :return:
        """
        if not self.assert_contains_text(self.el.item_button,text):
            self.logger.info(f"断言商品页面子组件按钮文本失败")
