from seleniumpm.webelements.panel import Panel
from seleniumpm.webelements.element import take_screenshot_on_element_error


class IFrame(Panel):
    def __init__(self, driver, locator=None):
        super(IFrame, self).__init__(driver=driver, locator=locator)

    def validate(self, timeout=None, force_check_visibility=False):
        timeout = timeout if timeout is not None else self.element_timeout
        try:
            self.switch_in()
            super(IFrame, self).validate(timeout=timeout, force_check_visibility=force_check_visibility)
        finally:
            self.switch_out()

    @take_screenshot_on_element_error
    def switch_in(self):
        """
        This is to support switching to an iframe for smart validations of all Element's on a page

        TODO - This implementation lacks support of multiple embedded iframe's (e.g. an iframe within another iframe)

        :return: self
        """
        if self.locator:
            self.driver.switch_to.frame(self.driver.find_element(by=self.locator.by, value=self.locator.value))
        return self

    @take_screenshot_on_element_error
    def switch_out(self):
        """
        This is to support switching out of an iframe for smart validations of all Element's on a page

        TODO - This implementation lacks support of multiple embedded iframe's (e.g. an iframe within another iframe)

        :return: self
        """
        self.driver.switch_to.default_content()
        return self
