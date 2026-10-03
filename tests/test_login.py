from utils.Loader.DataLoader import DataLoader
import pytest
from utils.paths import DATA_FILE

class TestLogin:
    test_data = DataLoader(DATA_FILE)

    #测试成功登录
    @pytest.mark.parametrize('username,password',test_data.get_value('test_login.test_success_login'))
    def test_success_login(self,login_page,username:str,password:str):
        login_page.expect_success_login(username,password)

    #测试失败登录文案
    @pytest.mark.parametrize('username,password,expected_text',test_data.get_value('test_login.test_fail_login'))
    def test_fail_login(self,login_page,username:str,password:str,expected_text:str):
        login_page.login_expected_text(username,password,expected_text)

    #测试提示框关闭之后是否会再次显示相同文本
    @pytest.mark.parametrize('username,password,expected_text',test_data.get_value('test_login.test_close_error_text'))
    def test_close_error_text(self,login_page,username,password,expected_text):
        login_page.login_expected_text(username,password,expected_text)
        login_page.close_error_message()
        login_page.clear_input()
        login_page.login_expected_text(username,password,expected_text)

    @pytest.mark.parametrize('expect_text',test_data.get_value('test_login.test_direct_next_without_login'))
    def test_direct_next_without_login(self,login_page,expect_text):
        login_page.goto(login_page._NEXT_URL)
        login_page.assert_contains_text(login_page.el.error_message,expect_text)


