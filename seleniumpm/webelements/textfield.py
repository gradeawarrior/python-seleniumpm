from seleniumpm.webelements.textelement import TextElement


class TextField(TextElement):
    def __init__(self, driver, locator):
        super(TextField, self).__init__(driver, locator)

    def send_keys(self, txt):
        self.get_webelement().send_keys(txt)

    def type(self, txt):
        self.send_keys(txt)

    def clear(self):
        self.get_webelement().clear()
        return self

    def submit(self):
        self.get_webelement().submit()
