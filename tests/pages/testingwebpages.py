from seleniumpm.locator import Locator
from seleniumpm.webpage import Webpage
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
