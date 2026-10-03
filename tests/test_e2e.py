from utils.Loader.DataLoader import DataLoader
import pytest
from utils.paths import DATA_FILE


class TestE2E:
    test_data = DataLoader(DATA_FILE)

    #标准下单主流程（3 件商品）
    @pytest.mark.smoke
    @pytest.mark.parametrize('test_ids,user_info',test_data.get_value('test_e2e.test_user_purchase_three_product'))
    def test_user_purchase_three_product(self,login_page,test_ids,user_info):
        inventory_page = login_page.login_successfully()
        inventory_page.add_cart_by_ids(test_ids)
        cart_page = inventory_page.header.enter_cart()
        checkInfo_page = cart_page.continue_checkInfo()
        checkInfo_page.fill_info(*user_info)
        checkOverview_page = checkInfo_page.submit()
        checkComplete_page = checkOverview_page.continue_to()
        checkComplete_page.expect_complete_header()

    #单件最低价商品最小下单流程
    @pytest.mark.smoke
    @pytest.mark.parametrize('lowest_product_title,user_info',test_data.get_value('test_e2e.test_add_one_lowest_price_product'))
    def test_add_one_lowest_price_product(self,login_page,lowest_product_title,user_info):
        inventory_page = login_page.login_successfully()
        item = inventory_page.get_inventoryItemByItemName(lowest_product_title)
        item.add_cart()
        cart_page = inventory_page.header.enter_cart()
        checkInfo_page = cart_page.continue_checkInfo()
        checkInfo_page.fill_info(*user_info)
        checkOverview_page = checkInfo_page.submit()
        checkComplete_page = checkOverview_page.continue_to()
        checkComplete_page.expect_complete_header()


    #全部 6 件商品下单流程
    @pytest.mark.smoke
    @pytest.mark.parametrize('user_info',test_data.get_value('test_e2e.test_user_purchase_all_product'))
    def test_user_purchase_all_product(self,login_page,user_info):
        inventory_page = login_page.login_successfully()
        items = inventory_page.get_inventoryItems()
        for item in items:
            item.add_cart()
        cart_page = inventory_page.header.enter_cart()
        checkInfo_page = cart_page.continue_checkInfo()
        checkInfo_page.fill_info(*user_info)
        checkOverview_page = checkInfo_page.submit()
        checkComplete_page = checkOverview_page.continue_to()
        checkComplete_page.expect_complete_header()

    #加购 - 移除 - 再加购后下单
    @pytest.mark.smoke
    @pytest.mark.parametrize('user_info',test_data.get_value('test_e2e.test_user_purchase_twice'))
    def test_user_purchase_twice(self,login_page,user_info):
        inventory_page = login_page.login_successfully()
        items = inventory_page.get_inventoryItems()
        for item in items:
            item.add_cart()
        cart_page = inventory_page.header.enter_cart()
        checkInfo_page = cart_page.continue_checkInfo()
        checkInfo_page.fill_info(*user_info)
        checkOverview_page = checkInfo_page.submit()
        checkComplete_page = checkOverview_page.continue_to()
        checkComplete_page.expect_complete_header()
        inventory_page = checkComplete_page.back_home_click()
        for item in items:
            item.add_cart()
        cart_page = inventory_page.header.enter_cart()
        checkInfo_page = cart_page.continue_checkInfo()
        checkInfo_page.fill_info(*user_info)
        checkOverview_page = checkInfo_page.submit()
        checkComplete_page = checkOverview_page.continue_to()
        checkComplete_page.expect_complete_header()

    #结算中途 Cancel 后再次下单成功(分两种，一种是在步骤一时取消，一种是在步骤二时取消)
    #步骤一
    @pytest.mark.smoke
    @pytest.mark.parametrize('user_info',test_data.get_value('test_e2e.test_checkout_cancel_checkout_in_step_one'))
    def test_checkout_cancel_checkout_in_step_one(self,login_page,user_info):
        inventory_page = login_page.login_successfully()
        items = inventory_page.get_inventoryItems()
        for item in items:
            item.add_cart()
        cart_page = inventory_page.header.enter_cart()
        checkInfo_page = cart_page.continue_checkInfo()
        inventory_page = checkInfo_page.cancel()
        cart_page = inventory_page.header.enter_cart()
        checkInfo_page = cart_page.continue_checkInfo()
        checkInfo_page.fill_info(*user_info)
        checkOverview_page = checkInfo_page.submit()
        checkComplete_page = checkOverview_page.continue_to()
        checkComplete_page.expect_complete_header()

    #步骤二
    @pytest.mark.smoke
    @pytest.mark.parametrize('user_info',test_data.get_value('test_e2e.test_checkout_cancel_checkout_in_step_two'))
    def test_checkout_cancel_checkout_in_step_two(self,login_page,user_info):
        inventory_page = login_page.login_successfully()
        items = inventory_page.get_inventoryItems()
        for item in items:
            item.add_cart()
        cart_page = inventory_page.header.enter_cart()
        checkInfo_page = cart_page.continue_checkInfo()
        checkInfo_page.fill_info(*user_info)
        checkOverview_page = checkInfo_page.submit()
        inventory_page = checkOverview_page.back_shopping()
        cart_page = inventory_page.header.enter_cart()
        checkInfo_page = cart_page.continue_checkInfo()
        checkInfo_page.fill_info(*user_info)
        checkOverview_page = checkInfo_page.submit()
        checkComplete_page = checkOverview_page.continue_to()
        checkComplete_page.expect_complete_header()