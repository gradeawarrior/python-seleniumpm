from seleniumpm.webelements.element import Element


class Label(Element):
    def __init__(self, driver, locator):
        super(Label, self).__init__(driver=driver, locator=locator)
