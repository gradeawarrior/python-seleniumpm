import copy
from selenium.webdriver.common.by import By

class Locator(object):

    def __init__(self, by, value):
        self.by = by
        self.value = value

    def append(self, relative_path):
        self.value += relative_path

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def get_tuple(self):
        """
        Returns a Locator as a tuple of (by, path)
        """
        return (self.by, self.value)

    def copy(self):
        return copy.deepcopy(self)

    @staticmethod
    def by_xpath(value):
        return Locator(by=By.XPATH, value=value)

    @staticmethod
    def by_css_selector(value):
        return Locator(by=By.CSS_SELECTOR, value=value)

    @staticmethod
    def by_name(value):
        return Locator(by=By.NAME, value=value)

    @staticmethod
    def by_class_name(value):
        return Locator(by=By.CLASS_NAME, value=value)

    @staticmethod
    def by_id(value):
        return Locator(by=By.ID, value=value)

    @staticmethod
    def by_link_text(value):
        return Locator(by=By.LINK_TEXT, value=value)

    @staticmethod
    def by_partial_link_text(value):
        return Locator(by=By.PARTIAL_LINK_TEXT, value=value)

    @staticmethod
    def by_tag_name(value):
        return Locator(by=By.TAG_NAME, value=value)
