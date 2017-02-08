from seleniumpm.webelements.clickable import Clickable


class Link(Clickable):
    def __init__(self, driver, locator):
        super(Link, self).__init__(driver, locator)
