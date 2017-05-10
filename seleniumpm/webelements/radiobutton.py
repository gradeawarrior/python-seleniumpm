from seleniumpm.webelements.clickable import Clickable


class RadioButton(Clickable):
    def __init__(self, driver, locator):
        super(RadioButton, self).__init__(driver, locator)

    def select(self):
        if not self.is_selected():
            self.get_webelement().click()
