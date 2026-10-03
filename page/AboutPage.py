from playwright.sync_api import Page

from page.BasePage import BasePage
from page.registry import registry

@registry("About")
class AboutPage(BasePage):
    _URL = 'https://saucelabs.com/'
    def __init__(self, page: Page):
        super().__init__(page)