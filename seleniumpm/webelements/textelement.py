from seleniumpm.webelements.element import Element


class TextElement(Element):
    def __init__(self, driver, locator):
        super(TextElement, self).__init__(driver, locator)
