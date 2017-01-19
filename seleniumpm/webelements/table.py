from selenium.webdriver.common.by import By

from seleniumpm.webelements.element import Element


class Table(Element):
    def __init__(self, driver, locator):
        super(Table, self).__init__(driver, locator)

    def get_rows(self):
        return self.driver.find_elements(By.XPATH, "//tbody/tr")

    def count_rows(self):
        return len(self.get_rows())
