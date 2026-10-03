from conftest import inventory_page
from utils.Loader.DataLoader import DataLoader
import pytest,random
from utils.paths import DATA_FILE,PRODUCTS_FILE

class TestCart:
    test_data = DataLoader(DATA_FILE)
    product_data = DataLoader(PRODUCTS_FILE)

    #购物车为空时的展示
    def test_no_item_in_cart(self,inventory_page):
        cart_page = inventory_page.header.enter_cart()
        assert cart_page.get_item_count() == 0

    #加购 3 件后购物车内容正确
    @pytest.mark.parametrize('test_ids',test_data.get_value('test_cart.test_add_num_item'))
    def test_add_num_item(self,inventory_page,test_ids):
        inventory_page.add_cart_by_ids(test_ids)
        info_in_invent_list = inventory_page.get_product_info_by_ids(test_ids)
        cart_page = inventory_page.header.enter_cart()
        assert cart_page.get_item_count() == len(test_ids)
        info_in_cart_list = cart_page.get_product_info_by_ids(test_ids)
        assert info_in_invent_list == info_in_cart_list

    #购物车条目数量字段正确
    @pytest.mark.parametrize('test_ids',test_data.get_value('test_cart.test_add_to_quantity'))
    def test_add_to_quantity(self,inventory_page,test_ids):
        inventory_page.add_cart_by_ids(test_ids)
        cart_page = inventory_page.header.enter_cart()
        assert cart_page.get_item_count() == len(test_ids)
        cart_items = cart_page.get_cartItem_by_ids(test_ids)
        info_in_cart_list = [item.get_quantity() for item in cart_items]
        assert info_in_cart_list == [1] * len(test_ids)

    #购物车内移除单个商品
    @pytest.mark.parametrize('test_ids', test_data.get_value('test_cart.test_add_to_cart_and_remove_one'))
    def test_add_to_cart_and_remove_one(self, inventory_page, test_ids):
        inventory_page.add_cart_by_ids(test_ids)
        cart_page = inventory_page.header.enter_cart()
        assert cart_page.get_item_count() == len(test_ids)
        remove_id = random.sample(test_ids,1)
        cart_page.remove_by_ids(remove_id)
        assert cart_page.get_item_count() == len(test_ids) - 1

    #购物车内移除全部商品
    @pytest.mark.parametrize('test_ids', test_data.get_value('test_cart.test_add_to_cart_and_remove_all'))
    def test_add_to_cart_and_remove_all(self, inventory_page, test_ids):
        inventory_page.add_cart_by_ids(test_ids)
        cart_page = inventory_page.header.enter_cart()
        assert cart_page.get_item_count() == len(test_ids)
        cart_page.remove_by_ids(test_ids)
        assert cart_page.get_item_count() == 0

    #Continue Shopping 返回商品列表
    def test_back_to_product(self,inventory_page):
        cart_page = inventory_page.header.enter_cart()
        inventory_page = cart_page.back_shopping()
        inventory_page.assert_url(inventory_page._URL)

    #加购商品后Checkout
    @pytest.mark.parametrize('test_ids',test_data.get_value('test_cart.test_checkout_with_add_to_step_one'))
    def test_checkout_with_add_to_step_one(self,inventory_page,test_ids):
        inventory_page.add_cart_by_ids(test_ids)
        cart_page = inventory_page.header.enter_cart()
        Check_page = cart_page.continue_checkInfo()
        Check_page.assert_url(Check_page._URL)

    #空购物车Checkout进入结算第一步
    def test_checkout_without_add_to_step_one(self,inventory_page):
        cart_page = inventory_page.header.enter_cart()
        Check_page = cart_page.continue_checkInfo()
        Check_page.assert_url(Check_page._URL)


