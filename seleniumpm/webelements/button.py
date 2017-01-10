from seleniumpm.webelements.element import Element

class Button(Element):

    def __init__(self, driver, locator):
        super(Button, self).__init__(driver, locator)

    def click(self):
        self.driver.find_element(self.locator.by, self.locator.value).click()
        return self
