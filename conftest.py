import pytest
from playwright.sync_api import sync_playwright, Browser,Page
from page.LoginPage import LoginPage

@pytest.fixture(scope='function')
def browser():
    """
    返回一个Browser对象
    :return:
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture(scope='function')
def page(browser:Browser):
    """
    返回一个Page对象
    :param browser:
    :return:
    """
    content = browser.new_context()
    page = content.new_page()
    yield page
    content.close()

@pytest.fixture
def login_page(page:Page):
    """
    返回一个LoginPage对象
    :param page:
    :return:
    """
    return LoginPage(page)

@pytest.fixture
def inventory_page(login_page):
    return login_page.login_successfully()

@pytest.fixture
def checkout_info_page(inventory_page):
    inventory_page.add_cart_by_ids([1,2,3,4,5,6])
    cart_page = inventory_page.header.enter_cart()
    return cart_page.continue_checkInfo()



