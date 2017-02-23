from seleniumpm.webelements.element import Element


class Image(Element):
    def __init__(self, driver, locator):
        super(Element, self).__init__(driver, locator)
