import re

from conftest import inventory_page
from utils.Loader.DataLoader import DataLoader
import pytest
from utils.paths import DATA_FILE,PRODUCTS_FILE
import random

class TestInventory:
    test_data = DataLoader(DATA_FILE)
    product_data = DataLoader(PRODUCTS_FILE)

    #商品主页面排序根据id=[5,1,2,6,3,4]排序
    @pytest.mark.parametrize('default_ids',test_data.get_value('test_inventory.test_check_inventory_items'))
    def test_check_inventory_items(self,inventory_page,default_ids:list,default_option:str='az'):
        inventory_page.select_to_sort_and_assert_names(default_option,default_ids)

    #断言sort按钮的默认值
    @pytest.mark.parametrize('expected_value',test_data.get_value('test_inventory.test_default_sort_value'))
    def test_default_sort_value(self,inventory_page,expected_value):
        actual_value = inventory_page.get_sort_value()
        assert actual_value == expected_value

    #验证所有排序结果(相同价格下按照标题A-Z再排序)
    @pytest.mark.parametrize('option,expected_ids',test_data.get_value('test_inventory.test_sort_assert_names'))
    def test_sort_assert_names(self,inventory_page,option,expected_ids):
        inventory_page.select_to_sort_and_assert_names(option,expected_ids)

    #验证排序切换后再切换回来的结果
    @pytest.mark.parametrize('option,expected_ids',test_data.get_value('test_inventory.test_sort_twice_names'))
    def test_sort_twice_names(self,inventory_page,option,expected_ids):
        default_option = 'az'
        inventory_page.select_to_sort_and_assert_names(option,expected_ids)
        inventory_page.select_to_sort(default_option)
        inventory_page.select_to_sort_and_assert_names(option,expected_ids)

    #验证排序不影响购物车
    @pytest.mark.parametrize('option',test_data.get_value('test_inventory.test_sort_not_to_indicate_cart'))
    def test_sort_not_to_indicate_cart(self,inventory_page,option):
        for inventoryItem in inventory_page.get_inventoryItems():
            inventoryItem.add_cart()
        cartPage = inventory_page.header.enter_cart()
        cart_names_before_sort = cartPage.get_all_names()
        sidebar = cartPage.header.open_sidebar()
        inventory_page = sidebar.chain_click('All Items',cartPage.page)
        inventory_page.select_to_sort(option)
        cartPage = inventory_page.header.enter_cart()
        cart_names_after_sort = cartPage.get_all_names()
        assert cart_names_before_sort == cart_names_after_sort

    #测试加购后按钮的文本改变
    @pytest.mark.parametrize('test_id',test_data.get_value('test_inventory.test_add_to_cart'))
    def test_add_to_cart(self,inventory_page,test_id):
        test_item = inventory_page.get_inventoryItemByItemName(self.product_data.get_value(f"Products.{test_id}.title"))
        test_item.add_cart()
        test_item.assert_contains_text(test_item.el.item_button,'Remove')


    #测试加购全部商品后徽标的数字改变
    @pytest.mark.parametrize('test_ids',test_data.get_value('test_inventory.test_shopping_cart_badge'))
    def test_shopping_cart_badge(self,inventory_page,test_ids):
        for i,item in enumerate(inventory_page.get_inventoryItemByIds(test_ids)):
            item.add_cart()
            inventory_page.assert_contains_text(inventory_page.header.shopping_cart_badge,str(i+1))

    #测试加购三个商品后移除一个商品，该商品的按钮文本改变
    @pytest.mark.parametrize('test_ids',test_data.get_value('test_inventory.test_remove'))
    def test_remove(self,inventory_page,test_ids):
        add_names = []
        items = inventory_page.get_inventoryItemByIds(test_ids)
        for item in items:
            item.add_cart()
            add_names.append(item.get_title())
        remove_name = random.choice(add_names)
        remove_item = inventory_page.get_inventoryItemByItemName(remove_name)
        remove_item.remove_from_cart()
        remove_item.assert_contains_text(remove_item.el.item_button,'Add to cart')
        inventory_page.assert_contains_text(inventory_page.header.shopping_cart_badge,str(len(add_names)-1))

    #全部商品移出购物车后徽标消失
    @pytest.mark.parametrize('test_ids', test_data.get_value('test_inventory.test_remove'))
    def test_remove_all_badge_disappear(self,inventory_page,test_ids):
        inventory_page.add_cart_by_ids(test_ids)
        inventory_page.assert_contains_text(inventory_page.header.shopping_cart_badge,str(len(test_ids)))
        inventory_page.remove_from_cart_by_ids(test_ids)
        inventory_page.assert_hidden(inventory_page.header.shopping_cart_badge)

    #商品价格格式校验
    @pytest.mark.parametrize('test_ids', test_data.get_value('test_inventory.test_item_price_format'))
    def test_item_price_format(self,inventory_page,test_ids):
        items = inventory_page.get_inventoryItemByIds(test_ids)
        for item in items:
            item.assert_contains_text(item.el.item_price,re.compile(r'^\$\d+\.\d{2}$'))

    #点击商品图片或者标题进入详情页
    @pytest.mark.parametrize('test_id,option', test_data.get_value('test_inventory.test_click_title_to_detail'))
    def test_click_title_to_detail(self,inventory_page,test_id,option:str):
        item = inventory_page.get_inventoryItemById(test_id)
        detail_page = item.enter_detail(option)
        detail_page.assert_url(detail_page._URL+str(test_id - 1))

    #详情页信息与列表页一致,并且url中的id与商品id一致
    @pytest.mark.parametrize('test_id', test_data.get_value('test_inventory.test_check_text_in_inventory_and_detail'))
    def test_check_text_in_inventory_and_detail(self,inventory_page,test_id):
        item = inventory_page.get_inventoryItemById(test_id)
        info_in_invent = item.get_all_info()
        item_detail_page = item.enter_detail()
        info_in_detail = item_detail_page.get_all_info()
        assert info_in_detail == info_in_invent
        item_detail_page.assert_url(item_detail_page._URL+str(test_id-1))

    #详情页 URL 带正确的商品 id
    @pytest.mark.parametrize('test_id', test_data.get_value('test_inventory.test_detail_has_id_in_url'))
    def test_detail_has_id_in_url(self,inventory_page,test_id):
        item = inventory_page.get_inventoryItemById(test_id)
        detail_page = item.enter_detail()
        detail_page.assert_url(detail_page._URL+str(test_id-1))

    #详情页加入购物车
    @pytest.mark.parametrize('test_id', test_data.get_value('test_inventory.test_add_to_cart_in_detail'))
    def test_add_to_cart_in_detail(self,inventory_page,test_id):
        item = inventory_page.get_inventoryItemById(test_id)
        detail_page = item.enter_detail()
        detail_page.assert_url(detail_page._URL+str(test_id-1))
        detail_page.add_cart()
        detail_page.assert_contains_text(detail_page.add_or_remove_button,detail_page._TEXT['remove'])
        detail_page.header.assert_cartBadge(1)

    #详情页移出购物车
    @pytest.mark.parametrize('test_id', test_data.get_value('test_inventory.test_remove_from_cart_in_detail'))
    def test_remove_from_cart_in_detail(self,inventory_page,test_id):
        item = inventory_page.get_inventoryItemById(test_id)
        item.add_cart()
        detail_page = item.enter_detail()
        detail_page.assert_url(detail_page._URL+str(test_id-1))
        detail_page.remove()
        detail_page.assert_contains_text(detail_page.add_or_remove_button,detail_page._TEXT['add'])
        detail_page.header.assert_hidden(detail_page.header.shopping_cart_badge)

    #从排为lohi的商品主页面进入商品详细页返回查看排序状态
    @pytest.mark.parametrize('test_id', test_data.get_value('test_inventory.test_sortState_from_detail_to_invent'))
    def test_sortState_from_detail_to_invent(self, inventory_page, test_id):
        inventory_page.select_to_sort('lohi')
        item = inventory_page.get_inventoryItemById(test_id)
        detail_page = item.enter_detail()
        inventory_page = detail_page.back_InventoryPage()
        assert inventory_page.get_sort_value() == 'lohi'

    #详情页加购后进入购物车核对商品信息(商品名，描述，价格)
    @pytest.mark.parametrize('test_id', test_data.get_value('test_inventory.test_info_in_detail_and_cart'))
    def test_info_in_detail_and_cart(self,inventory_page,test_id):
        item = inventory_page.get_inventoryItemById(test_id)
        info_in_invent = item.get_product_info()
        item.add_cart()
        cart_page = inventory_page.header.enter_cart()
        cart_item = cart_page.get_cartItem_by_id(test_id)
        info_in_cart = cart_item.get_product_info()
        assert info_in_invent == info_in_cart

    #详情页商品图片正常渲染
    @pytest.mark.parametrize('test_id', test_data.get_value('test_inventory.test_info_in_detail_and_cart'))
    def test_img_in_detail_show_normally(self,inventory_page,test_id):
        item = inventory_page.get_inventoryItemById(test_id)
        detail_page = item.enter_detail()
        detail_page.expect_img_loaded()


