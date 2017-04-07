from seleniumpm.webelements.textelement import TextElement
from seleniumpm.webelements.element import take_screenshot_on_element_error
import time


class TextField(TextElement):
    def __init__(self, driver, locator):
        super(TextField, self).__init__(driver, locator)

    @take_screenshot_on_element_error
    def send_keys(self, txt):
        self.get_webelement().send_keys(txt)
        return self

    @take_screenshot_on_element_error
    def type(self, txt):
        return self.send_keys(txt)

    @take_screenshot_on_element_error
    def send_keys_delayed(self, txt, delay=0.2):
        element = self.get_webelement()
        for i in txt:
            time.sleep(delay)
            element.send_keys(i)
        return self

    @take_screenshot_on_element_error
    def type_delayed(self, txt, delay=0.2):
        return self.send_keys_delayed(txt=txt, delay=delay)

    @take_screenshot_on_element_error
    def clear(self):
        self.get_webelement().clear()
        return self

    @take_screenshot_on_element_error
    def submit(self):
        self.get_webelement().submit()
