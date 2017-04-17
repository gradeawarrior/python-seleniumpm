from seleniumpm.webelements.panel import Panel
from seleniumpm.webelements.element import take_screenshot_on_element_error


class IFrame(Panel):
    def __init__(self, driver, locator=None):
        super(IFrame, self).__init__(driver=driver, locator=locator)

    def validate(self, timeout=None, force_check_visibility=False):
        """
        An IFrame validate takes into account that you have to switch_in() to an iFrame to actually validate the
        inner-page.

        :param timeout: (Default: 10s) The number of seconds to poll waiting for an element
        :param force_check_visibility: (Default: False) Some elements can mark itself as invisible (but present) on
                                       load. The default is to respect this setting and only check for presence. Setting
                                       this to 'True' means you want to check for both present and visible.
        :raises TimeoutException: if an element doesn't appear within timeout
        :return: self
        """
        timeout = timeout if timeout is not None else self.page_timeout
        try:
            self.switch_in()
            return super(IFrame, self).validate(timeout=timeout, force_check_visibility=force_check_visibility)
        finally:
            self.switch_out()

    @take_screenshot_on_element_error
    def switch_in(self):
        """
        This is to support switching to an iFrame for smart validations of all Element's on a page

        TODO - This implementation lacks support of multiple embedded iFrame's (e.g. an iFrame within another iFrame)

        :return: self
        """
        if self.locator:
            self.driver.switch_to.frame(self.driver.find_element(by=self.locator.by, value=self.locator.value))
        return self

    @take_screenshot_on_element_error
    def switch_out(self):
        """
        This is to support switching out of an iFrame for smart validations of all Element's on a page

        TODO - This implementation lacks support of multiple embedded iFrame's (e.g. an iFrame within another iFrame)

        :return: self
        """
        self.driver.switch_to.default_content()
        return self
