from seleniumpm.webelements.clickable import Clickable
from seleniumpm.webelements.element import take_screenshot_on_element_error


class Checkbox(Clickable):
    def __init__(self, driver, locator):
        super(Checkbox, self).__init__(driver, locator)

    @take_screenshot_on_element_error
    def select(self):
        if not self.is_selected():
            self.get_webelement().click()

    @take_screenshot_on_element_error
    def unselect(self):
        if self.is_selected():
            self.get_webelement().click()
