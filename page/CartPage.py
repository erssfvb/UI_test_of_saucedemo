from playwright.sync_api import Page, expect
from utils.Loader.DataLoader import DataLoader
from utils.paths import PRODUCTS_FILE
from page.BasePage import BasePage
from page.components.Header import Header
from page.components.Footer import Footer
from page.components.CartItem import CartItemInCart


class CartPage(BasePage):
    _PRODUCTS_DATA = DataLoader(PRODUCTS_FILE)
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = Header(page)
        self.footer = Footer(page)
        self.items = page.locator('.cart_list')
        self.item = page.locator('.cart_item')
        self.back_button = page.locator('#continue-shopping')
        self.checkout_button = page.locator('#checkout')

    #------页面信息操作--------
    def get_all_names(self)->list[str]:
        self.assert_visible(self.items)
        return self.items.locator('.inventory_item_name').all_inner_texts()

    def get_item_count(self)->int:
        """
        获取页面中所有子组件的数量
        :return:
        """
        return len(self.get_all_names())

    def get_product_info_by_ids(self,ids:list[int])->list[list[str]]:
        items = self.get_cartItem_by_ids(ids)
        product_info = list()
        for item in items:
            product_info.append(item.get_product_info())
        return product_info

    #------获取子组件对象操作------
    def get_cartItem_by_id(self,id:int):
        return CartItemInCart(self.page,self._PRODUCTS_DATA.get_value(f'Products.{id}.title'))

    def get_cartItem_by_ids(self,ids:list[int])->list[CartItemInCart]:
        items = list()
        for id in ids:
            items.append(self.get_cartItem_by_id(id))
        return items

    def get_CartItem(self,item_name:str)->CartItemInCart:
        """
        获取单个子组件对象
        :param item_name:
        :return:
        """
        return CartItemInCart(self.page,item_name)

    def get_cartItems(self)->list[CartItemInCart]:
        """
        获取页面中所有子组件的对象
        :return:
        """
        item_list = []
        for name in self.get_all_names():
            item_list.append(self.get_CartItem(name))
        return item_list

    #-------跳转操作----------
    def back_shopping(self):
        """
        返回商品主页面
        :return:
        """
        from page.InventoryPage import InventoryPage
        self.click(self.back_button)
        return self._go(InventoryPage)

    def continue_checkInfo(self):
        """
        跳转到结账信息填写页面
        :return:
        """
        from page.CheckInfoPage import CheckInfoPage
        self.click(self.checkout_button)
        return self._go(CheckInfoPage)

    #------购物车操作-----------
    def add_cart_by_ids(self,ids:list[int]):
        items = self.get_cartItem_by_ids(ids)
        for item in items:
            item.add_cart()

    def remove_by_ids(self,ids:list[int]):
        items = self.get_cartItem_by_ids(ids)
        for item in items:
            item.remove()

    #---------断言操作----------
    def expect_empty(self):
        """
        断言购物车子组件数量为0
        :return:
        """
        if not self.assert_count(self.item,0):
            self.logger.info(f"断言购物车为空失败")

