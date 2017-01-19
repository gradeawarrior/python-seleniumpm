from seleniumpm.webelements.textelement import TextElement


class TextField(TextElement):

    def __init__(self, driver, locator):
        super(TextField, self).__init__(driver, locator)

    def send_keys(self, txt):
        self.driver.find_element(self.locator.by, self.locator.value).send_keys(txt)

    def type(self, txt):
        self.send_keys(txt)

    def clear(self):
        self.driver.find_element(self.locator.by, self.locator.value).clear()
        return self

    def submit(self):
        self.driver.find_element(self.locator.by, self.locator.value).submit()
