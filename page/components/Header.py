from playwright.sync_api import Page, Locator, expect
from page.registry import get
from page.BasePage import BasePage




class SideBar:
    #缩进代表层级
    _DIRECT = {
        'All Items':'All Items',
            'Lazy Load':'Lazy Load',
            'Spinner':'Spinner',
            'Slider':'Slider',
        'Logout':'login',
        "About":'About'
    }
    _TEXT = ["All Items","Dynamic Catalog","About","Logout","Reset App State"]
    def __init__(self, locator: Locator):
        self.root = locator
        self.button = self.root.locator('.menu-item')
        self.sub_button = self.root.locator('.submenu-item')

    #-------------页面信息操作----------
    def get_menu_item(self,option:str)->list[str]:
        """
        返回统一层级的按钮文本
        :param option: ['menu','submenu']
        :return: list[str]
        """
        if option == 'menu':
            return self.button.all_inner_texts()
        elif option == 'submenu':
            return self.sub_button.all_inner_texts()
        return []

    def chain_click(self,chain:str,page:Page):
        """
        用路径来替代定位每个按钮元素，减少代码量
        在测试层中控制返回对象
        :param chain: a.b.c
        :return: None
        """
        scope = self.root
        for _ in chain.split('.'):
            scope = scope.locator('.bm-item').filter(has_text=_)
            scope.click()
            if _ in self._DIRECT:
                return get(self._DIRECT[_])(page)
        return None


class Header(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.sidebar = SideBar(page.locator('.bm-menu'))
        self.open_menu = page.locator('#react-burger-menu-btn')
        self.cart_icon = page.locator('.shopping_cart_link')
        self.shopping_cart_badge = page.locator('.shopping_cart_badge')

    #---------页面信息------------
    def get_cart_badge(self)->int:
        return int(self.get_text(self.shopping_cart_badge))

    #----------跳转操作-----------
    def enter_cart(self):
        from page.CartPage import CartPage
        self.click(self.cart_icon)
        self.page.locator('.cart_list').wait_for(state='visible')
        return self._go(CartPage)

    #----------导航操作-----------
    def open_sidebar(self)->SideBar:
        self.click(self.open_menu)
        return self.sidebar


    #------断言操作---------
    def assert_cartBadge_hidden(self):
        if not self.assert_hidden(self.shopping_cart_badge):
            self.logger.info(f"断言购物车徽标隐藏失败")

    def assert_cartBadge(self,num:int):
        if not expect(self.shopping_cart_badge).to_have_text(str(num)):
            self.logger.info(f"断言购物车徽标数量失败")
