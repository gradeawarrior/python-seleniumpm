from seleniumpm.webelements.clickable import Clickable


class Button(Clickable):
    def __init__(self, driver, locator):
        super(Button, self).__init__(driver, locator)
