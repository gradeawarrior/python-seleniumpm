from selenium.webdriver.support.select import Select
from seleniumpm.webelements.clickable import Clickable

from seleniumpm.webelements.element import Element


class Dropdown(Clickable):
    def __init__(self, driver, locator):
        super(Dropdown, self).__init__(driver, locator)
        self.select = None

    def instantiateSelect(self):
        if self.select == None:
            self.select = Select(self.get_webelement())

    def count_options(self):
        # TODO - Need to implement a way to get and modify the original locator to append '/option' (Assuming xpath)
        raise NotImplementedError

    def select_by_visible_text(self, txt):
        self.instantiateSelect()
        self.select.select_by_visible_text(txt)
        return self

    def select_by_index(self, index):
        self.instantiateSelect()
        self.select.select_by_index(index)
        return self
