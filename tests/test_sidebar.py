from playwright.sync_api import expect

from conftest import inventory_page
from utils.Loader.DataLoader import DataLoader
import pytest,random
from utils.paths import DATA_FILE,PRODUCTS_FILE



class TestSidebar:
    test_data = DataLoader(DATA_FILE)
    # ----------Sidebar----------
    # 打开侧边栏展示全部菜单项
    def test_Sidebar_text(self, inventory_page):
        sidebar = inventory_page.header.open_sidebar()
        for text in sidebar._TEXT:
            inventory_page.assert_contains_text(sidebar.root, text)

    # All Items 返回商品列表
    def test_AllItems_url(self,inventory_page):
        cart_page = inventory_page.header.enter_cart()
        sidebar = cart_page.header.open_sidebar()
        inventory_page = sidebar.chain_click("All Items",cart_page.page)
        inventory_page.assert_url(inventory_page._URL)

    #About 跳转 Sauce Labs 官网
    def test_About_url(self,inventory_page):
        sidebar = inventory_page.header.open_sidebar()
        about_page = sidebar.chain_click('About',inventory_page.page)
        about_page.assert_url(about_page._URL)

    #Logout 退出登录
    def test_Logout_url(self,inventory_page):
        sidebar = inventory_page.header.open_sidebar()
        login_page = sidebar.chain_click('Logout',inventory_page.page)
        login_page.assert_url(login_page._URL)

    #登出后无法再访问商品列表
    def test_cannot_access_inventory_without_login(self,login_page):
        login_page.goto(login_page._NEXT_URL)
        error_message = "Epic sadface: You can only access '/inventory.html' when you are logged in."
        login_page.assert_contains_text(login_page.el.error_message,error_message)

    #Reset App State 清空购物车
    def test_Reset_App_State(self,inventory_page):
        items = inventory_page.get_inventoryItems()
        for item in items:
            item.add_cart()
        sidebar = inventory_page.header.open_sidebar()
        sidebar.chain_click("Reset App State",inventory_page.page)
        cart_page = inventory_page.header.enter_cart()
        assert cart_page.get_item_count() == 0

    #---------Footer----------
    #页脚版权文案正确
    def test_text_in_footer(self,inventory_page):
        inventory_page.footer.assert_contains_text(inventory_page.footer.copyright,
                                                   inventory_page.footer._TEXT['copyright'])

    #三个社交链接地址正确
    def test_href_in_social_link(self,inventory_page):
        footer = inventory_page.footer
        footer.assert_href(footer.X,footer._TEXT['X'])
        footer.assert_href(footer.facebook,footer._TEXT['facebook'])
        footer.assert_href(footer.linkedin, footer._TEXT['linkedin'])

    #

