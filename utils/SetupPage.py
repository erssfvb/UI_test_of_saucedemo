from contextlib import contextmanager
from playwright.sync_api import sync_playwright


@contextmanager
def Page():
    with sync_playwright() as p:
         browser = p.chromium.launch(headless=True)
         content = browser.new_context()
         page = content.new_page()
         yield page
         browser.close()

@contextmanager
def Inventory():
     from page.LoginPage import LoginPage
     with Page() as p:
          l =  LoginPage(p)
          yield l.login_successfully()
          p.close()