from playwright.sync_api import Page, expect

from page.BasePage import BasePage

class CartItemInCheckoutOverview(BasePage):
    _TEXT = {
        'add':'Add to cart',
        'remove':'Remove'
    }
    def __init__(self,page:Page,item_name):
        super().__init__(page)
        self.root = page.locator('.cart_item').filter(has=page.get_by_text(item_name,exact=True))
        self.title = self.root.locator('.inventory_item_name')
        self.quantity = self.root.locator('.cart_quantity')
        self.price = self.root.locator('.inventory_item_price')

    def get_price(self)->float:
        return float(self.get_text(self.price).lstrip('$'))

    def get_all_info(self)->list[str]:
        page_info = self.root.all_inner_texts()
        return page_info[0].split('\n')

    def get_product_info(self)->list[str]:
        """
        商品的信息包括标题，描述和价格
        :return:
        """
        return self.get_all_info()[1:4]

    def get_qty(self)->int:
        return int(self.get_text(self.quantity))



class CartItemInCart(CartItemInCheckoutOverview):
    def __init__(self,page:Page,item_name):
        super().__init__(page,item_name)
        self.button = self.root.locator('.cart_button')

    #---------页面信息操作------------
    def get_name(self)->str:
        return self.get_text(self.title)

    def get_quantity(self)->int:
        return int(self.get_text(self.quantity))

    #----------购物车操作-------------
    def remove(self):
        self.assert_contains_text(self.button,self._TEXT['remove'])
        self.click(self.button)

    def add_cart(self):
        self.assert_contains_text(self.button,self._TEXT['add'])
        self.click(self.button)
