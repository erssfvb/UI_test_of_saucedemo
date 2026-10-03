from dataclasses import dataclass
from playwright.sync_api import Page
from page.BasePage import BasePage
from page.registry import registry


@dataclass(frozen=True)
class LoginPageElement:
    Username:str
    Password:str
    error_message:str
    error_button:str
    Login_submit:str

@registry('login')
class LoginPage(BasePage):
    _URL = 'https://www.saucedemo.com/'
    _NEXT_URL = 'https://www.saucedemo.com/inventory.html'
    def __init__(self,page:Page):
        super().__init__(page)
        self.el = LoginPageElement(
            Username='#user-name',
            Password='#password',
            error_message='[data-test="error"]',
            error_button='.error-button',
            Login_submit='#login-button'
        )
    #-----------用户起点----------
    def open(self):
        self.goto(self._URL)

    #-----------登录模块操作--------

    def clear_input(self):
        self.fill(self.el.Username,'')
        self.fill(self.el.Password, '')

    def login(self,username:str,password:str):
        """
        用户登录行为，包含填写，提交，但不涉及其他的操作
        :param username:
        :param password:
        :return:
        """
        self.open()
        self.fill(self.el.Username,username)
        self.fill(self.el.Password,password)
        self.click(self.el.Login_submit)

    def login_successfully(self):
        """
        直接登录，返回一个商品主页面对象
        :return:
        """
        from page.InventoryPage import InventoryPage
        self.login('standard_user','secret_sauce')
        return self._go(InventoryPage)


    def expect_success_login(self,username:str,password:str):
        """
        正常用户登录操作
        :param username:用户名
        :param password: 密码
        :return: None
        """
        from page.InventoryPage import InventoryPage
        self.login(username,password)
        self.assert_url(self._NEXT_URL)
        return self._go(InventoryPage)

    def login_expected_text(self, username: str, password: str, expected_text: str = None)->None:
        """
        异常登录操作
        :param username:用户名
        :param password:密码
        :param expected_text:预期失败提示文本
        :return:None
        """
        self.open()
        self.fill(self.el.Username,username,sensitive=False)
        self.fill(self.el.Password,password)
        self.click(self.el.Login_submit)
        self.assert_visible(self.el.error_message)
        self.assert_contains_text(self.el.error_message,expected_text)



    #--------错误提示框操作----------
    def close_error_message(self):
        """
        关闭提示框
        :return:
        """
        self.click(self.el.error_button)
        if not self.assert_hidden(self.el.error_message):
            self.logger.info(f"断言错误提示框隐藏失败")


