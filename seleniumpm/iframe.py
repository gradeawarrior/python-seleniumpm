from seleniumpm.locator import Locator
from seleniumpm.webelements.element import Element
from seleniumpm.webelements.panel import Panel
from seleniumpm.webelements.element import take_screenshot_on_element_error


class IFrame(Panel):
    def __init__(self, driver, locator=None):
        super(IFrame, self).__init__(driver=driver, locator=locator)
        self.iframe_load_duration_time = 0

    def get_html(self, switch_in=True):
        """
        Retrieves the html of the entire page

        :param switch_in: (Default: True) This is used for automatically switching into and out of an iFrame context
        :return: a str of the entire page html
        """
        try:
            if switch_in:
                self.switch_in()
            return Element(self.driver, Locator.by_xpath("//html")).get_html()
        finally:
            if switch_in:
                self.switch_out()

    def wait_for_iframe_load(self, timeout=None, force_check_visibility=True, check_myself=True):
        """
        An IFrame wait_for_iframe_load() takes into account that you have to switch_in() to an iFrame to actually
        validate the inner-page.

        :param timeout: (Default: 30s) The number of seconds to poll waiting for an element
        :param force_check_visibility: (Default: False) Some elements can mark itself as invisible (but present) on
                                       load. The default is to respect this setting and only check for presence. Setting
                                       this to 'True' means you want to check for both present and visible.
        :param check_myself: (Default: True) Since a Widget/Panel/IFrame is a type of Element, it also has a locator.
                             This is used for enabling/disabling adding a validation against itself. The scenario
                             where this could be used is in a situation where you want to validate the elements of this
                             container, but not the Locator of the container itself.
        :raises TimeoutException: if an element doesn't appear within timeout
        :return: self
        """
        timeout = timeout if timeout is not None else self.page_timeout
        return self.validate(timeout=timeout, force_check_visibility=force_check_visibility, check_myself=check_myself)

    def validate(self, timeout=None, force_check_visibility=False, check_myself=True):
        """
        An IFrame validate takes into account that you have to switch_in() to an iFrame to actually validate the
        inner-page.

        :param timeout: (Default: 10s) The number of seconds to poll waiting for an element
        :param force_check_visibility: (Default: False) Some elements can mark itself as invisible (but present) on
                                       load. The default is to respect this setting and only check for presence. Setting
                                       this to 'True' means you want to check for both present and visible.
        :param check_myself: (Default: True) Since a Widget/Panel/IFrame is a type of Element, it also has a locator.
                             This is used for enabling/disabling adding a validation against itself. The scenario
                             where this could be used is in a situation where you want to validate the elements of this
                             container, but not the Locator of the container itself.
        :raises TimeoutException: if an element doesn't appear within timeout
        :return: self
        """
        timeout = timeout if timeout is not None else self.element_timeout
        try:
            self.start_timer(type="iframe_load")
            self.switch_in() if check_myself else None
            return super(IFrame, self).validate(timeout=timeout,
                                                force_check_visibility=force_check_visibility,
                                                check_myself=check_myself)
        finally:
            self.switch_out() if check_myself else None
            self.stop_timer(type="iframe_load")

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

    @property
    def iframe_load_duration(self):
        driver_iframe_load_duration_time = self.get_duration(type="iframe_load")
        if driver_iframe_load_duration_time > self.iframe_load_duration_time:
            self.iframe_load_duration_time = driver_iframe_load_duration_time
        return self.iframe_load_duration_time
