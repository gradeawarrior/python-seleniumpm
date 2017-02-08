from seleniumpm.webelements.clickable import Clickable


class Checkbox(Clickable):
    def __init__(self, driver, locator):
        super(Checkbox, self).__init__(driver, locator)
