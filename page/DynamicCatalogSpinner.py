from page.BasePage import BasePage
from playwright.sync_api import Page
from page.components.DynamicCatalogCard import DynamicCatalogCard
from page.registry import registry

@registry('Spinner')
class DynamicCatalogSpinnerPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.title = page.locator('.title')
        self.cards = page.locator('.dynamic_catalog_card')

    #--------页面信息显示--------
    def get_all_names(self)->list[str]:
        return self.get_all_texts(self.cards)


    #--------子组件对象获取
    def get_item(self,item_name:str)->DynamicCatalogCard:
        return DynamicCatalogCard(self.page,item_name)

    def get_items(self)->list[DynamicCatalogCard]:
        result = []
        for name in self.get_all_names():
            result.append(self.get_item(name))
        return result
