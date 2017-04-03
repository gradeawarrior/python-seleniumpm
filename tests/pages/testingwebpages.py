from seleniumpm.locator import Locator
from seleniumpm.webpage import Webpage
from seleniumpm.iframe import IFrame
from seleniumpm.webelements.panel import Panel
from seleniumpm.webelements.widget import Widget
from seleniumpm.webelements.element import Element


class ZeroValidatedElementsPage(Webpage):
    def __init__(self, driver, url=None):
        super(ZeroValidatedElementsPage, self).__init__(driver=driver, url=url)
        self.element1 = Element(driver, Locator.by_xpath("//a")).mark_do_not_check()
        self.element2 = Element(driver, Locator.by_xpath("//b")).mark_do_not_check()
        self.element3 = Element(driver, Locator.by_xpath("//c")).mark_do_not_check()

class HiddenElementsPage(Webpage):
    def __init__(self, driver, url=None):
        super(HiddenElementsPage, self).__init__(driver=driver, url=url)
        self.element1 = Element(driver, Locator.by_xpath("//a")).mark_invisible()
        self.element2 = Element(driver, Locator.by_xpath("//b")).mark_invisible()
        self.element3 = Element(driver, Locator.by_xpath("//c")).mark_invisible()

class MyComplexPage(Webpage):
    def __init__(self, driver, url=None):
        super(MyComplexPage, self).__init__(driver=driver, url=url)
        self.regular_element = Element(driver, Locator.by_xpath("//a"))
        self.invisible_element = Element(driver, Locator.by_xpath("//b")).mark_invisible()
        self.not_checked_element = Element(driver, Locator.by_xpath("//c")).mark_do_not_check()

class MyComplexWidget(Widget):
    def __init__(self, driver, locator):
        super(MyComplexWidget, self).__init__(driver=driver, locator=locator)
        self.regular_element_on_widget = Element(driver, Locator.by_xpath("//d"))
        self.invisible_element_on_widget = Element(driver, Locator.by_xpath("//e")).mark_invisible()
        self.not_checked_element_on_widget = Element(driver, Locator.by_xpath("//f")).mark_do_not_check()

class MyComplexPanel(Panel):
    def __init__(self, driver, locator):
        super(MyComplexPanel, self).__init__(driver=driver, locator=locator)
        self.regular_element = Element(driver, Locator.by_xpath("//g"))
        self.invisible_element = Element(driver, Locator.by_xpath("//h")).mark_invisible()
        self.not_checked_element = Element(driver, Locator.by_xpath("//i")).mark_do_not_check()

class MyComplexIframe(IFrame):
    def __init__(self, driver, locator):
        super(MyComplexIframe, self).__init__(driver=driver, locator=locator)
        self.regular_element = Element(driver, Locator.by_xpath("//j"))
        self.invisible_element = Element(driver, Locator.by_xpath("//k")).mark_invisible()
        self.not_checked_element = Element(driver, Locator.by_xpath("//l")).mark_do_not_check()
