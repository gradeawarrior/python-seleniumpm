import inspect
import sys
import types

from seleniumpm.webelements.clickable import Clickable
from seleniumpm.webelements.element import Element


class Widget(Clickable):
    def __init__(self, driver, locator=None):
        super(Clickable, self).__init__(driver, locator)

    def dict(self):
        """
        This returns a dictionary representation of a Widget

        :return: a dict representation of a Widget
        """
        dictionary = super(Widget, self).dict()
        elements = self.get_element_attr_local()
        dictionary['elements'] = {}
        for key, element in elements.iteritems():
            dictionary['elements'][key] = element.dict()
        dictionary['methods'] = self.get_methods_local()
        return dictionary

    def wait_for_widget_load(self, timeout=None, force_check_visibility=False, check_myself=True):
        """
        This implementation is the same as Webpage.wait_for_page_load(). This is to support iFrame situations that
        is a separate page load than the outer page.

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

    def validate(self, timeout=None, force_check_visibility=True, check_myself=False):
        """
        The intention of validate is to make sure that an already loaded widget contains these elements.

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
        from seleniumpm.iframe import IFrame
        for element in self.get_element_attr(expand_iframe_elements=False, check_myself=check_myself):
            # Continue if the element has marked itself do_not_check=True or a Locator is not defined
            if element.do_not_check or element.locator is None:
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

    def get_element_attr(self, type=Element, override_check_visible=False, override_do_not_check=False,
                         expand_iframe_elements=False, result_type=list, check_myself=True, attr_name='widget'):
        """
        Retrieves a list of WebElements on a Widget. Optionally, you can pass in a different type (e.g. Button,
        Link, TextElement) to return only those types associated with a Widget object.

        :param type: one of the seleniumpm.webelement types (Default: seleniumpm.webelements.Element)
        :param override_check_visible: (Default: False) This overrides check for visibility. By default, widgets that are
                                        invisible, means that we assume its elements are also invisible
        :param override_do_not_check: (Default: False) This overrides check for do_not_check. By default, widgets that are
                                        marked as do_not_check, means that we assume its elements are not accessible
        :param expand_iframe_elements: (Default: False) Elements within an iFrame must be kept together in order to execute validate()
        :param result_type: (Default: list) This value can either be (list|dict). By default, we simply want a list of
                            available elements on the page. However, the dictionary version is implemented for the ability
                            to retrieve every element and sub-element on a Webpage directly from the page level
        :param check_myself: (Default: True) Since a Widget/Panel/IFrame is a type of Element, it also has a locator.
                             This is used for enabling/disabling adding a validation against itself. The scenario
                             where this could be used is in a situation where you want to validate the elements of this
                             container, but not the Locator of the container itself.
        :param attr_name: (Default: 'widget') This is for passing the attribute name from its parent when recursively
                            iterating through all of its sub-elements.
        :return: This is a list or dict of attributes of base type seleniumpm.webelements.Element
        """
        from seleniumpm.iframe import IFrame
        from seleniumpm.webelements.panel import Panel
        if result_type != list and result_type != dict:
            raise AttributeError(
                "result_type can either be 'list' (default) or 'dict', but was '{}'".format(result_type))
        elements = [] if result_type == list else {}
        temp_widgets = {}
        # Add myself if I match the expected type
        if isinstance(self, type) and (not isinstance(self, IFrame) or expand_iframe_elements) and check_myself:
            if result_type == dict:
                elements[attr_name] = self
            else:
                elements.append(self)
        for attr in dir(self):
            # This is to catch potential exceptions thrown in situations where a developer
            # decorates a method with @property and the method raises an error
            try:
                element = getattr(self, attr, None)
            except:
                element = None
            # Ensure that it is of type Element
            if isinstance(element, Element):
                # Set some Widget meta-data in the element
                element.attr_name = attr
                element.attr_class_name = self.__class__.__name__
                # If it is a widget, then recursively drill down and get its Elements
                if isinstance(element, Widget):
                    # Check if widget is a type of iFrame and also check for visibility
                    if (element.check_visible or override_check_visible) and \
                            (not element.do_not_check or override_do_not_check) and \
                            not isinstance(element, IFrame) or \
                            ((isinstance(element, IFrame) and expand_iframe_elements)):
                        if result_type == dict:
                            temp_widgets[attr] = []
                            for key, value in element.get_element_attr(type=type,
                                                                       override_check_visible=override_check_visible,
                                                                       override_do_not_check=override_do_not_check,
                                                                       expand_iframe_elements=expand_iframe_elements,
                                                                       result_type=result_type,
                                                                       check_myself=True,
                                                                       attr_name=attr).items():
                                temp_widgets[attr].append({'key': key, 'value': value})
                        else:
                            for welement in element.get_element_attr(type=type):
                                elements.append(welement)
                    # Add the widget but not its sub-elements if invisible
                    else:
                        if result_type == dict:
                            elements[attr] = element
                        else:
                            elements.append(element)
                # Add the element if it matches the expected type (not a Widget)
                if type not in (Widget, Panel, IFrame) and isinstance(element, type) and not isinstance(element,
                                                                                                        Widget):
                    if result_type == dict:
                        elements[attr] = element
                    else:
                        elements.append(element)

        # Give non-widgets priority, hence why there is a separate loop for widgets and their elements
        for attr, values in temp_widgets.items():
            for element in values:
                if element['key'] not in elements:
                    elements[element['key']] = element['value']
                else:
                    elements["{}_{}".format(attr, element['key'])] = element['value']
        return elements

    def get_element_attr_local(self):
        """
        This is a much simpler implement of get_element_attr() in that it only returns back the locally defined
        Elements, and not any elements defined in sub-Widgets and sub-Panels.

        :return: A dict of Element types
        """
        elements = {}
        for attr in dir(self):
            element = getattr(self, attr)
            if isinstance(element, Element) and attr in self.__dict__.keys():
                elements[attr] = element
        return elements

    def get_methods_local(self):
        """
        Returns only the local methods defined for this class

        :return: a dict containing method names (keys) and a list of parameters for the method (values)
        """
        results = {}
        for attr in dir(self):
            method = getattr(self, attr)
            if type(method) == types.MethodType and \
                            method.__name__ not in ('__init__') and \
                            method.__func__ in method.im_class.__dict__.values():
                args = inspect.getargspec(method)[0][1:]
                results[method.__name__] = args
        return results

    def get_all_elements_on_widget(self):
        """
        Retrieves all the webelements that have been defined on the widget. This includes all sub-elements found on
        widgets, panels, and iframes.

        :return: A dict of all the elements
        """
        return self.get_element_attr(override_check_visible=True,
                                     override_do_not_check=True,
                                     expand_iframe_elements=True,
                                     result_type=dict)

    def __getattr__(self, name):
        """
        Overridden method so that we can also be able to directly access all webelements defined at lower level
        webelements (a.k.a. widgets, panels, and iframes)

        :param name: The name of the attribute or webelement that we expect to exist on the Webpage
        :return: The attribute value if found
        :raises AttributeError: If the attribute with given name doesn't exist
        """
        # Need to escape a potential infinite recursion for the following names
        if name in ('__members__', '__methods__'):
            return
        # Checking if the element is defined in the sub-widgets, panels, or iframes
        all_elements = self.get_all_elements_on_widget()
        if name in all_elements:
            return all_elements[name]
        else:
            raise AttributeError(
                "'{}' webpage and its widgets has no attribute '{}'. "
                "The following are valid webelements on the page:\n  - {}".format(
                    self.__class__.__name__, name, "\n  - ".join(all_elements.keys())))
