from seleniumpm.webelements.clickable import Clickable


class Widget(Clickable):
    def __init__(self, driver, locator):
        super(Clickable, self).__init__(driver, locator)

    def validate(self):
        raise NotImplementedError
