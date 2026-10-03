from enum import Enum

from playwright.sync_api import Page, expect
from typing_extensions import Literal
from utils.Loader.DataLoader import DataLoader
from utils.paths import PRODUCTS_FILE
from page.BasePage import BasePage
from page.components.Header import Header
from page.components.Footer import Footer
from page.components.InventoryItem import InventoryItem
from page.registry import registry

@registry('All Items')
class InventoryPage(BasePage):
    _URL = 'https://www.saucedemo.com/inventory.html'
    OPTION = Literal["az","za","lohi","hilo"]
    product_data = DataLoader(PRODUCTS_FILE)
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = Header(page)
        self.footer = Footer(page)
        self.title = page.locator('.title')
        self.items = page.locator('.inventory_item')
        self.sort = page.locator('.product_sort_container')

    #-------------获取子组件对象--------

    def get_inventoryItemById(self,id)->InventoryItem:
        return InventoryItem(self.page,self.product_data.get_value(f"Products.{id}.title"))

    def get_inventoryItemByIds(self,ids:list[int])->list[InventoryItem]:
        items = list()
        for id in ids:
            items.append(self.get_inventoryItemById(id))
        return items

    def get_inventoryItemByItemName(self, item_name):
        return InventoryItem(self.page,item_name)

    def get_inventoryItemByItemNames(self,names:list[str]):
        items = list()
        for name in names:
            items.append(self.get_inventoryItemByItemName(name))
        return items

    def get_inventoryItems(self)->list[InventoryItem]:
        items = list()
        for _ in self.get_all_names():
            items.append(self.get_inventoryItemByItemName(_))
        return items

    #---------获取页面信息---------
    def get_all_names(self)->list[str]:
        return self.items.locator('.inventory_item_name ').all_inner_texts()

    def get_all_prices(self)->list[str]:
        result = []
        for item in self.get_inventoryItems():
            result.append(item.get_price())
        return result

    def get_product_info_by_ids(self,ids:list[int])->list[list[str]]:
        items = self.get_inventoryItemByIds(ids)
        product_info = list()
        for item in items:
            product_info.append(item.get_product_info())
        return product_info

    #--------排序功能----------

    def select_to_sort(self,option:OPTION):
        """
        切换排序的规则
        :param option: ['az','za','lohi','hilo']分别对应按名字，价格
        :return:
        """
        self.sort.select_option(option)

    def select_to_sort_and_assert_names(self,option:OPTION,expect_ids:list[int]):
        """
        主界面排序,并且断言结果，断言用的是assert关键字，所以错误会抛出AssertionError异常
        :param option:['az','za','lohi','hilo']分别对应按名字，价格
        :param expect_ids 商品的id列表
        :return:
        """
        self.sort.select_option(option)
        actual_names = self.get_all_names()
        expect_names = []
        for id in expect_ids:
            expect_names.append(self.product_data.get_value(f"Products.{id}.title"))
        assert actual_names == expect_names

    def get_sort_value(self):
        """
        返回当前排序按钮的选项值,['az','za','lohi','hilo']其中的一个
        :return:
        """
        return self.sort.input_value()
    #----------购物车---------
    def add_cart_by_ids(self,ids:list[int]):
        """
        通过一个id列表将商品加入购物车
        :param ids:
        :return:
        """
        items = self.get_inventoryItemByIds(ids)
        for item in items:
            item.add_cart()

    def remove_from_cart_by_ids(self,ids:list[int]):
        """
        通过一个id列表将商品从购物车中移除
        :param ids:
        :return:
        """
        items = self.get_inventoryItemByIds(ids)
        for item in items:
            item.remove_from_cart()
    #-------断言功能---------
    def expect_item_count(self,num:int):
        """
        断言当前商品有多少个
        :param num:
        :return:
        """
        if not self.assert_count(self.items,num):
            self.logger.info(f"断言商品主页面的所有商品数量失败")

    def expect_title(self,text:str):
        """
        断言当前页面标题
        :param text:
        :return:
        """
        if not self.assert_contains_text(self.title,text):
            self.logger.info(f"断言主页面标题失败")










