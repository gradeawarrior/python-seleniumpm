from seleniumpm.webelements.textelement import TextElement
import time


class TextField(TextElement):
    def __init__(self, driver, locator):
        super(TextField, self).__init__(driver, locator)

    def send_keys(self, txt):
        self.get_webelement().send_keys(txt)
        return self

    def type(self, txt):
        return self.send_keys(txt)

    def send_keys_delayed(self, txt, delay=0.2):
        element = self.get_webelement()
        for i in txt:
            time.sleep(delay)
            element.send_keys(i)
        return self

    def type_delayed(self, txt, delay=0.2):
        return self.send_keys_delayed(txt=txt, delay=delay)

    def clear(self):
        self.get_webelement().clear()
        return self

    def submit(self):
        self.get_webelement().submit()
