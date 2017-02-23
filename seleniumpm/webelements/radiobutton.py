from seleniumpm.webelements.clickable import Clickable


class RadioButton(Clickable):
    def __init__(self, driver, locator):
        super(RadioButton, self).__init__(driver, locator)
