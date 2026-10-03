from playwright.sync_api import expect

from conftest import inventory_page
from utils.Loader.DataLoader import DataLoader
import pytest,random
from utils.paths import DATA_FILE,PRODUCTS_FILE

class TestCheckout:
    product_data = DataLoader(PRODUCTS_FILE)
    test_data = DataLoader(DATA_FILE)

    #填写完整收货信息进入第二步
    @pytest.mark.parametrize('firstname,lastname,postal_code',test_data.get_value('test_checkout.test_continue_to_checkoutOverView'))
    def test_continue_to_checkoutOverView(self,checkout_info_page,firstname,lastname,postal_code):
        checkout_info_page.fill_info(firstname,lastname,postal_code)
        checkout_overviewPage = checkout_info_page.submit()
        checkout_overviewPage.assert_url(checkout_overviewPage._URL)

    #异常提交文本显示是否正确
    @pytest.mark.parametrize('firstname,lastname,postal_code,expected_text',test_data.get_value('test_checkout.test_fail_fillInfo'))
    def test_fail_fillInfo(self,checkout_info_page,firstname,lastname,postal_code,expected_text):
        checkout_info_page.fill_info(firstname,lastname,postal_code)
        checkout_info_page.submit()
        if expected_text == '':
            checkout_info_page.assert_hidden(checkout_info_page.error_message)
        else:
            checkout_info_page.assert_error_text(expected_text)

    #Cancel 返回购物车且数据不丢
    @pytest.mark.parametrize("test_ids",test_data.get_value('test_checkout.test_add_num_products_from_cancel'))
    def test_add_num_products_from_cancel(self,inventory_page,test_ids):
        inventory_page.add_cart_by_ids(test_ids)
        cart_page = inventory_page.header.enter_cart()
        before_info = cart_page.get_product_info_by_ids(test_ids)
        check_info_page = cart_page.continue_checkInfo()
        cart_page = check_info_page.cancel()
        after_info = cart_page.get_product_info_by_ids(test_ids)
        assert after_info == before_info

    #报错后修正信息可成功提交
    @pytest.mark.parametrize("firstFill_fail,revisionFill",
                             test_data.get_value('test_checkout.test_error_message_and_continue_submit_after_revision'))
    def test_error_message_and_continue_submit_after_revision(
            self,checkout_info_page,firstFill_fail:list[str],revisionFill:list[str]
    ):
        f,l,p,e = firstFill_fail
        checkout_info_page.fill_info(f,l,p)
        checkout_info_page.submit()
        checkout_info_page.assert_error_text(e)
        checkout_info_page.clear()
        f,l,p = revisionFill
        checkout_info_page.fill_info(f,l,p)
        checkout_info_page.submit()
        checkout_info_page.assert_error_text(e)
        checkout_info_page.assert_url(checkout_info_page._NEXT_URL)

    #第一步页面标题与 URL
    def test_title_and_url(self,checkout_info_page):
        checkout_info_page.assert_contains_text(checkout_info_page.continue_button,checkout_info_page._TEXT['continue_button'])
        checkout_info_page.assert_url(checkout_info_page._URL)

    #---------CheckoutOverview-----------
    #订单摘要商品与购物车一致
    @pytest.mark.parametrize("test_ids,userinfo",test_data.get_value('test_checkout.test_add_num_same_as_overview'))
    def test_add_num_same_as_overview(self,inventory_page,test_ids,userinfo):
        inventory_page.add_cart_by_ids(test_ids)
        cart_page = inventory_page.header.enter_cart()
        cart_info = cart_page.get_product_info_by_ids(test_ids)
        checkInfo_page = cart_page.continue_checkInfo()
        checkInfo_page.fill_info(*userinfo)
        checkout_overview_page = checkInfo_page.submit()
        overview_info = [item.get_product_info() for item in checkout_overview_page.get_all_items()]
        assert overview_info == cart_info

    #支付方式与配送方式文案
    @pytest.mark.parametrize('userinfo',test_data.get_value('test_checkout.test_text_in_paymentInfo_and_shippingInfo'))
    def test_text_in_paymentInfo_and_shippingInfo(self,inventory_page,userinfo):
        cart_page = inventory_page.header.enter_cart()
        checkInfo_page = cart_page.continue_checkInfo()
        checkInfo_page.fill_info(*userinfo)
        checkOverview_page = checkInfo_page.submit()
        checkOverview_page.assert_paymentInfo()
        checkOverview_page.assert_shipping_info()

    #商品小计等于各商品单价之和
    @pytest.mark.parametrize("test_ids,userinfo",test_data.get_value("test_checkout.test_prices_total_equal_itemTotal"))
    def test_prices_total_equal_itemTotal(self,inventory_page,test_ids,userinfo):
        inventory_page.add_cart_by_ids(test_ids)
        cart_page = inventory_page.header.enter_cart()
        checkInfo_page = cart_page.continue_checkInfo()
        checkInfo_page.fill_info(*userinfo)
        checkOverview_page = checkInfo_page.submit()
        checkOverview_page.assert_item_total()

    #税额按小计的 8% 计算
    @pytest.mark.parametrize("test_ids,userinfo",test_data.get_value("test_checkout.test_prices_total_multiply_tax_percent_equal_tax"))
    def test_prices_total_multiply_tax_percent_equal_tax(self,inventory_page,test_ids,userinfo):
        inventory_page.add_cart_by_ids(test_ids)
        cart_page = inventory_page.header.enter_cart()
        checkInfo_page = cart_page.continue_checkInfo()
        checkInfo_page.fill_info(*userinfo)
        checkOverview_page = checkInfo_page.submit()
        checkOverview_page.assert_tax()

    #仅 1 件最低价商品结算金额
    @pytest.mark.parametrize('test_id,userinfo',test_data.get_value('test_checkout.test_one_product_price_calculate_total_and_tax'))
    def test_one_product_price_calculate_total_and_tax(self,inventory_page,test_id,userinfo):
        inventory_page.add_cart_by_ids(test_id)
        cart_page = inventory_page.header.enter_cart()
        checkInfo_page = cart_page.continue_checkInfo()
        checkInfo_page.fill_info(*userinfo)
        checkOverview_page = checkInfo_page.submit()
        checkOverview_page.assert_item_total()
        checkOverview_page.assert_tax()
        checkOverview_page.assert_total()


    #全部 6 件商品结算金额
    @pytest.mark.parametrize("test_ids,userinfo",test_data.get_value('test_checkout.test_all_add_calculate_total_and_tax'))
    def test_all_add_calculate_total_and_tax(self,inventory_page,test_ids,userinfo):
        inventory_page.add_cart_by_ids(test_ids)
        cart_page = inventory_page.header.enter_cart()
        checkInfo_page = cart_page.continue_checkInfo()
        checkInfo_page.fill_info(*userinfo)
        checkOverview_page = checkInfo_page.submit()
        checkOverview_page.assert_item_total()
        checkOverview_page.assert_tax()
        checkOverview_page.assert_total()

    #Cancel 返回商品列表
    @pytest.mark.parametrize('userinfo',test_data.get_value('test_checkout.test_from_checkoutOverview_to_inventory_page'))
    def test_from_checkoutOverview_to_inventory_page(self,inventory_page,userinfo):
        cart_page = inventory_page.header.enter_cart()
        checkInfo_page = cart_page.continue_checkInfo()
        checkInfo_page.fill_info(*userinfo)
        checkOverview_page = checkInfo_page.submit()
        inventory_page = checkOverview_page.back_shopping()
        inventory_page.assert_url(inventory_page._URL)

    #Finish 提交订单进入完成页
    @pytest.mark.parametrize("userinfo",test_data.get_value('test_checkout.test_checkoutOverview_finish'))
    def test_checkoutOverview_finish(self,inventory_page,userinfo):
        items = inventory_page.get_inventoryItems()
        for item in items:
            item.add_cart()
        cart_page = inventory_page.header.enter_cart()
        checkInfo_page = cart_page.continue_checkInfo()
        checkInfo_page.fill_info(*userinfo)
        checkOverview_page = checkInfo_page.submit()
        checkoutComplete_page = checkOverview_page.continue_to()
        checkoutComplete_page.assert_url(checkoutComplete_page._URL)

    #-----------checkoutCompletePage----------
    #完成页展示下单成功信息
    @pytest.mark.parametrize("userinfo", test_data.get_value('test_checkout.test_checkoutComplete_title'))
    def test_checkoutComplete_title(self,inventory_page,userinfo):
        cart_page = inventory_page.header.enter_cart()
        checkInfo_page = cart_page.continue_checkInfo()
        checkInfo_page.fill_info(*userinfo)
        checkOverview_page = checkInfo_page.submit()
        checkoutComplete_page = checkOverview_page.continue_to()
        checkoutComplete_page.expect_complete_header()

    #下单后购物车被清空
    @pytest.mark.parametrize("userinfo",
                             test_data.get_value('test_checkout.test_shopping_cart_badge_be_zero_after_checkoutComplete'
                                                 ))
    def test_shopping_cart_badge_be_zero_after_checkoutComplete(self,inventory_page,userinfo):
        items = inventory_page.get_inventoryItems()
        for item in items:
            item.add_cart()
        cart_page = inventory_page.header.enter_cart()
        checkInfo_page = cart_page.continue_checkInfo()
        checkInfo_page.fill_info(*userinfo)
        checkOverview_page = checkInfo_page.submit()
        checkoutComplete_page = checkOverview_page.continue_to()
        checkoutComplete_page.assert_hidden(checkoutComplete_page.header.shopping_cart_badge)

    #Back Home 返回商品列表
    @pytest.mark.parametrize("userinfo",
                             test_data.get_value('test_checkout.test_checkoutComplete_backHome_to_inventoryPage'
                                                 ))
    def test_checkoutComplete_backHome_to_inventoryPage(self,inventory_page,userinfo):
        cart_page = inventory_page.header.enter_cart()
        checkInfo_page = cart_page.continue_checkInfo()
        checkInfo_page.fill_info(*userinfo)
        checkOverview_page = checkInfo_page.submit()
        checkoutComplete_page = checkOverview_page.continue_to()
        inventory_page = checkoutComplete_page.back_home_click()
        inventory_page.assert_url(inventory_page._URL)

    #下单后再进入购物车为空
    @pytest.mark.parametrize("userinfo",
                             test_data.get_value('test_checkout.test_checkoutComplete_enter_cart_has_on_item'
                                                 ))
    def test_checkoutComplete_enter_cart_has_on_item(self,inventory_page,userinfo):
        items = inventory_page.get_inventoryItems()
        for item in items:
            item.add_cart()
        cart_page = inventory_page.header.enter_cart()
        checkInfo_page = cart_page.continue_checkInfo()
        checkInfo_page.fill_info(*userinfo)
        checkOverview_page = checkInfo_page.submit()
        checkoutComplete_page = checkOverview_page.continue_to()
        cart_page = checkoutComplete_page.header.enter_cart()
        assert cart_page.get_item_count() == 0


