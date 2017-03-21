from seleniumpm.webelements.clickable import Clickable
from seleniumpm.webelements.element import Element


class Widget(Clickable):
    def __init__(self, driver, locator):
        super(Clickable, self).__init__(driver, locator)

    def validate(self, timeout=10, force_check_visibility=False):
        """
        The intention of validate is to make sure that an already loaded widget contains these elements.
        :param timeout: (Default: 10s) The number of seconds to poll waiting for an element
        :param force_check_visibility: (Default: False) Some elements can mark itself as invisible (but present) on
                                       load. The default is to respect this setting and only check for presence. Setting
                                       this to 'True' means you want to check for both present and visible.
        :raises TimeoutException: if an element doesn't appear within timeout
        """
        for element in self.get_element_attr():
            # Continue if the element has marked itself do_not_check=True
            if element.do_not_check:
                continue
            # Check for presence and visibility
            if force_check_visibility or element.check_visible:
                element.wait_for_present_and_visible(timeout)
            else:
                element.wait_for_present(timeout)
        return self

    def get_element_attr(self, type=Element):
        """
        Retrieves a list of WebElements on a Widget. Optionally, you can pass in a different type (e.g. Button,
        Link, TextElement) to return only those types associated with a Widget object.
        :param type: one of the seleniumpm.webelement types (Default: seleniumpm.webelements.Element)
        :return: This is a list of attributes of base type seleniumpm.webelements.Element
        """
        elements = []
        for attr in dir(self):
            element = getattr(self, attr)
            # Ensure that it is of type Element
            if isinstance(element, Element):
                # If it is a widget, then recursively drill down and get its Elements
                if isinstance(element, Widget):
                    for welement in element.get_element_attr(type=type):
                        elements.append(welement)
                # Add the element if it matches the expected type
                if isinstance(element, type):
                    elements.append(element)
        return elements
