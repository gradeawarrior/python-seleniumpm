from seleniumpm.webelements.element import Element

class TextField(Element):

    def __init__(self, driver, locator):
        super(TextField, self).__init__(driver, locator)

    def type(self, text):
        self.send_keys(text)
        return self

    def send_keys(self, text):
        self.driver.find_element(self.locator.by, self.locator.value).send_keys(text)
        return self

    def clear(self):
        self.driver.find_element(self.locator.by, self.locator.value).clear()
        return self

    def submit(self):
        self.driver.find_element(self.locator.by, self.locator.value).submit()
