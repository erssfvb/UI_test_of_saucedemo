from playwright.sync_api import Page, expect
from page.BasePage import BasePage
from utils.Loader.DataLoader import DataLoader
from utils.paths import DATA_FILE
from page.registry import registry


def hex_to_rgb(hex_str:str):
    """
    hex转换成rgb(a,a,a)
    :param hex_str:
    :return:
    """
    hex_color = hex_str.lstrip('#')
    r,g,b = tuple(int(hex_color[i:i+2],16) for i in (0,2,4))
    return f"rgb({r},{g},{b})"

@registry('Slider')
class DynamicCatalogSliderPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.data = DataLoader(DATA_FILE)
        self.card = page.locator('.dynamic_catalog_card')
        self.img = self.card.locator('.class="dynamic_catalog_card_img"')
        self.title = self.card.locator('.dynamic_catalog_card_name')
        self.price = self.card.locator('.dynamic_catalog_card_price')
        self.slider_dots = page.locator('.dynamic_catalog_slider_dot')

    #--------页面文本操作---------
    def click_dot(self,num:int):
        """
        点击相应dot之后断言卡片中的所有内容
        :param num: 第几个
        :return:
        """
        self.click(self.slider_dots.nth(num-1))
        self.assert_contains_text(self.title,self.data.get_value(f"Products.{num}.title"))
        expect(self.img).to_have_attribute('src',self.data.get_value(f"Products.{num}.img"))
        self.assert_contains_text(self.price,self.data.get_value(f"Products.{num}.price"))

    #-----------断言初始状态---------
    def expect_default(self,default:int=1):
        self.assert_contains_text(self.title,self.data.get_value(f"Products.{default}.title"))
        for i in range(6):
            if i == default:
                expect(self.slider_dots.nth(i)).to_have_css('background', f"{hex_to_rgb('#3ddc91')}")
            else:
                expect(self.slider_dots.nth(i)).to_have_css('background', f"{hex_to_rgb('#ffffff')}")

