import sys

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
        from seleniumpm.iframe import IFrame
        for element in self.get_element_attr(expand_iframe_elements=False):
            # Continue if the element has marked itself do_not_check=True
            if element.do_not_check:
                continue
            # Check for presence and visibility
            if force_check_visibility or element.check_visible:
                # Print to stderr a WARNING message when force_check_visibility=True and element has been marked 'invisible'
                if force_check_visibility and not element.check_visible:
                    sys.stderr.write(
                        "[WARNING] element {}={} ({}) was marked as 'invisible' but force_check_visibility=True".format(
                            element.locator.by, element.locator.value, self.__class__))
                if isinstance(element, IFrame):
                    element.validate(timeout=timeout, force_check_visibility=force_check_visibility)
                else:
                    element.wait_for_present_and_visible(timeout)
            else:
                element.wait_for_present(timeout)
        return self

    def get_element_attr(self, type=Element, expand_iframe_elements=False):
        """
        Retrieves a list of WebElements on a Widget. Optionally, you can pass in a different type (e.g. Button,
        Link, TextElement) to return only those types associated with a Widget object.

        :param type: one of the seleniumpm.webelement types (Default: seleniumpm.webelements.Element)
        :param expand_iframe_elements: (Default: False) Elements within an iFrame must be kept together in order to execute validate()
        :return: This is a list of attributes of base type seleniumpm.webelements.Element
        """
        from seleniumpm.iframe import IFrame
        from seleniumpm.webelements.panel import Panel
        elements = []
        # Add myself if I match the expected type
        if isinstance(self, type) and not isinstance(self, IFrame):
            elements.append(self)
        for attr in dir(self):
            element = getattr(self, attr)
            # Ensure that it is of type Element
            if isinstance(element, Element):
                # If it is a widget, then recursively drill down and get its Elements
                if isinstance(element, Widget):
                    # Check if widget is a type of iFrame, then override expanding elements
                    if element.check_visible and not element.do_not_check and not isinstance(element, IFrame) or (isinstance(element, IFrame) and expand_iframe_elements):
                        for welement in element.get_element_attr(type=type):
                            elements.append(welement)
                    # Add the widget but not its sub-elements if invisible
                    else:
                        elements.append(element)
                # Add the element if it matches the expected type (not a Widget)
                if type not in (Widget, Panel, IFrame) and isinstance(element, type) and not isinstance(element, Widget):
                    elements.append(element)
        return elements
