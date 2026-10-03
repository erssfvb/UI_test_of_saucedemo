from playwright.sync_api import Page, expect
from page.BasePage import BasePage,LocatorLike


class Footer(BasePage):
    _COPYRIGHT_TEXT = "© 2026 Sauce Labs. All Rights Reserved. Terms of Service | Privacy Policy"
    _TEXT = {
        "copyright":"© 2026 Sauce Labs. All Rights Reserved. Terms of Service | Privacy Policy",
        "X":"https://x.com/saucelabs",
        "facebook":"https://www.facebook.com/saucelabs",
        "linkedin":"https://www.linkedin.com/company/sauce-labs/"
    }
    def __init__(self,page:Page):
        super().__init__(page)
        self.X = page.locator('[data-test="social-x"]')
        self.facebook = page.locator('[data-test="social-facebook"]')
        self.linkedin = page.locator('[data-test="social-linkedin"]')
        self.copyright = page.locator('.footer_copy')

    def check_copyright(self):
        self.assert_contains_text(self.copyright,self._COPYRIGHT_TEXT)

    def get_social_href(self,option:str)->str:
        """
        返回社交链接的href
        :param option:['x','facebook','linkedin']
        :return:
        """
        if option == 'x':
            return self.X.get_attribute('href')
        elif option == 'facebook':
            return self.facebook.get_attribute('href')
        elif option == 'linkedin':
            return self.facebook.get_attribute('href')
        return ''

    def assert_href(self,selector:LocatorLike,href):
        self.logger.info(f"断言元素{selector}的href属性为{href}")
        expect(selector).to_have_attribute('href',href)