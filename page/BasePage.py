import logging
from pathlib import Path
from datetime import datetime
from typing import Union,TypeVar
from playwright.sync_api import Page,Locator,expect

LocatorLike = Union[str,Locator]
P = TypeVar("P",bound="BasePage")

class BasePage:

    def __init__(self,page:Page):
        self.page = page
        self.logger = logging.getLogger(self.__class__.__name__)

    def _loc(self,selector:LocatorLike)->Locator:
        return selector if isinstance(selector,Locator) else self.page.locator(selector)

    def _go(self,page_cls:type[P])->P:
        return page_cls(self.page)

    def reload(self):
        self.logger.info(f"页面刷新")
        self.page.reload()

    def click(self,selector:LocatorLike,**kwargs)->None:
        """
        点击行为
        GIVE:CSS选择器或者Locator对象
        WHEN:元素存在时
        THEN:触发点击事件
        :param selector: CSS选择器或者Locator对象
        :param kwargs: Locator.click()的额外关键字参数
        :return: None
        """
        self.logger.info(f"click: {selector}")
        self._loc(selector).click(**kwargs)

    def fill(self,selector:LocatorLike,text:str,sensitive:bool = False,**kwargs)->None:
        """
        输入框填充行为
        GIVE:CSS选择器或者Locator对象,text
        WHEN:元素存在时
        THEN:填写text相应文本
        :param selector: CSS选择器或者Locator对象
        :param text: 输入框填充的文本
        :param sensitive: 信息是否敏感
        :param kwargs: Locator.fill()的额外关键字参数
        :return: None
        """
        self.logger.info(f"fill:{selector} -> {'***' if sensitive else text}")
        self._loc(selector).fill(text,**kwargs)

    def goto(self,url:str,**kwargs)->None:
        """
        跳转行为
        GIVE:目标url字符串
        WHEN:None
        THEN:跳转到相应的页面
        :param url: 目标url
        :param kwargs: Locator.goto()的额外关键字参数
        :return: None
        """
        self.logger.info(f"goto: {url}")
        self.page.goto(url,**kwargs)

    def screenshot(self,name:str = "screenshot",full_page:bool=True)-> Path:
        """
        截图行为
        GIVE:截图文件名字，是否截图全屏
        WHEN:None
        THEN:截图并且保存到相应的路径
        :param name: 截图文件名字
        :param full_page: 是否截全图
        :return: 返回图片保存的路径
        """
        d = Path(".reports/screenshots")
        d.mkdir(parents=True,exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        path = d / f"{name}_{ts}.png"
        self.page.screenshot(path=path, full_page=full_page)
        return path

    def get_text(self,selector:LocatorLike,**kwargs)->str:
        """
        获取元素文本
        GIVE:CSS选择器或者Locator对象
        WHEN:元素存在时
        THEN:返回元素相应的文本
        :param selector: CSS选择器或者Locator对象
        :param kwargs: Locator.inner_text()的其他参数
        :return: 返回元素相应的文本
        """
        text = self._loc(selector).inner_text(**kwargs)
        self.logger.info(f"从元素{selector}中获取文本{text}")
        return text

    def assert_visible(self,selector:LocatorLike,**kwargs)->bool:
        """
        断言元素是否可见
        GIVE:CSS选择器或者Locator对象
        WHEN:元素存在时
        THEN:断言元素是否可见
        :param selector: CSS选择器或者Locator对象
        :param kwargs: expect().to_be_visible()的其他参数
        :return: None
        """
        self.logger.info(f"断言元素{selector}可见")
        try:
            expect(self._loc(selector)).to_be_visible(**kwargs)
            return True
        except AssertionError:
            return False


    def assert_hidden(self,selector:LocatorLike,**kwargs)->bool:
        """
        断言元素是否隐藏
        GIVE:CSS选择器或者Locator对象
        WHEN:元素存在时
        THEN:断言元素是否可见
        :param selector: CSS选择器或者Locator对象
        :param kwargs: expect().to_be_hidden()的其他参数
        :return: None
        """
        self.logger.info(f"断言元素{selector}被隐藏")
        try:
            expect(self._loc(selector)).to_be_hidden(**kwargs)
            return True
        except AssertionError:
            return False

    def assert_contains_text(self,selector:LocatorLike,text:str,**kwargs)->bool:
        """
        断言元素中拥有的文本
        GIVE:CSS选择器或者Locator对象，text:预期文本
        WHEN:元素存在时
        THEN:断言元素是否有用这段文本
        :param selector: CSS选择器或者Locator对象
        :param text: 预期文本
        :param kwargs: expect().to_contain_text()的其他参数
        :return: None
        """
        self.logger.info(f"断言元素{selector}的文本为{text}")
        try:
            expect(self._loc(selector)).to_contain_text(text, **kwargs)
            return True
        except AssertionError:
            return False

    def assert_url(self,url:str,**kwargs)->bool:
        """
        断言页面当前url
        GIVE:预期url
        WHEN:点击相应的跳转按钮后
        THEN:断言页面现在的url
        :param url:预期url
        :param kwargs: to_have_url的其他参数
        :return: None
        """
        self.logger.info(f"断言当前页面的url为{url}")
        try:
            expect(self.page).to_have_url(self._URL, **kwargs)
            return True
        except AssertionError:
            return False

    def get_all_texts(self,selector:LocatorLike):
        """
        返回页面列表中相同元素的所有文本列表
        GIVE:selector 列表中所有元素的相同标签
        WHEN:当匹配到多个html行的时候
        THEN:返回包含所有文本的列表
        :param selector: 列表中子组件的相同标签
        :return:
        """
        self.logger.info(f"获取多个元素{selector}中的本文")
        return self._loc(selector).all_inner_texts()

    def assert_count(self,selector:LocatorLike,num:int,**kwargs)->bool:
        """
        返回元素列表中所有相同元素的个数
        GIVE:selector 列表中所有元素的相同标签;num：预期数量
        WHEN:当匹配到多个html行的时候
        THEN:断言这些相同元素有num个
        :param selector:列表中子组件的相同标签
        :param num:预期个数
        :param kwargs: to_have_url的其他参数
        :return:子组件总个数
        """
        self.logger.info(f"断言元素{selector}一共有")
        try:
            expect(self._loc(selector)).to_have_count(num, **kwargs)
            return True
        except AssertionError:
            return False
