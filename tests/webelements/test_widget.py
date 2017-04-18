from tests.uitestwrapper import UiTestWrapper
import tests.pages.testingwebpages as testingwebpages
from seleniumpm.locator import Locator
from seleniumpm.webelements.element import Element
from seleniumpm.webelements.widget import Widget
from seleniumpm.webelements.panel import Panel
from seleniumpm.iframe import IFrame


class TestWidget(UiTestWrapper):
    """
    Tests to make sure that the widget type is working correctly.
    """
    @staticmethod
    def calculate_meta(elements):
        initial = {'total': 0,
                   'visible': 0,
                   'invisible': 0,
                   'do-not-check': 0,
                   'types': {'iframe': 0,
                             'panel': 0,
                             'widget': 0,
                             'element': 0}}
        for element in elements:
            initial['total'] += 1
            if element.do_not_check:
                initial['do-not-check'] += 1
            elif element.check_visible:
                initial['visible'] += 1
            else:
                initial['invisible'] += 1
            if isinstance(element, IFrame):
                initial['types']['iframe'] += 1
            elif isinstance(element, Panel):
                initial['types']['panel'] += 1
            elif isinstance(element, Widget):
                initial['types']['widget'] += 1
            elif isinstance(element, Element):
                initial['types']['element'] += 1
        return initial

    def test_complex_widget(self):
        widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        elements = widget.get_element_attr()
        meta_data = self.calculate_meta(elements)
        assert len(elements) == 4, "Expecting there to be 4 elements in this test complex widget"
        assert meta_data['types']['element'] == 3, "Expecting there to be 3 Element types"
        assert meta_data['visible'] == 2, "Expecting there to be 2 visible"
        assert meta_data['invisible'] == 1, "Expecting there to be 1 invisible"
        assert meta_data['do-not-check'] == 1, "Expecting there to be 1 do-not-check"

    def test_complex_widget_without_locator(self):
        widget = testingwebpages.MyComplexWidget(self.driver)
        elements = widget.get_element_attr()
        meta_data = self.calculate_meta(elements)
        assert len(elements) == 4, "Expecting there to be 4 elements in this test complex widget"
        assert meta_data['types']['element'] == 3, "Expecting there to be 3 Element types"
        assert meta_data['visible'] == 2, "Expecting there to be 2 visible"
        assert meta_data['invisible'] == 1, "Expecting there to be 1 invisible"
        assert meta_data['do-not-check'] == 1, "Expecting there to be 1 do-not-check"

    def test_complex_widget_without_locator_get_webelement(self):
        widget = testingwebpages.MyComplexWidget(self.driver)
        try:
            widget.get_webelement()
            assert False, "Expecting an AttributeError to be thrown for a Widget with no locator"
        except AttributeError:
            pass

    def test_complex_widget_with_widget(self):
        widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        widget.visible_widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        elements = widget.get_element_attr()
        meta_data = self.calculate_meta(elements)
        assert len(elements) == 8, "Expecting there to be 8 elements in this test complex widget"
        assert meta_data['types']['element'] == 6, "Expecting there to be 6 Element types"
        assert meta_data['types']['widget'] == 2, "Expecting there to be 2 Widget types"
        assert meta_data['visible'] == 4, "Expecting there to be 4 visible"
        assert meta_data['invisible'] == 2, "Expecting there to be 2 invisible"
        assert meta_data['do-not-check'] == 2, "Expecting there to be 2 do-not-check"

    def test_complex_widget_with_invisible_widget(self):
        widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        widget.visible_widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget")).mark_invisible()
        elements = widget.get_element_attr()
        meta_data = self.calculate_meta(elements)
        assert len(elements) == 5, "Expecting there to be 5 elements in this test complex widget"
        assert meta_data['types']['element'] == 3, "Expecting there to be 3 Element types"
        assert meta_data['types']['widget'] == 2, "Expecting there to be 2 Widget types"
        assert meta_data['visible'] == 2, "Expecting there to be 2 visible"
        assert meta_data['invisible'] == 2, "Expecting there to be 2 invisible"
        assert meta_data['do-not-check'] == 1, "Expecting there to be 1 do-not-check"

    def test_complex_widget_with_do_not_check_widget(self):
        widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        widget.visible_widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget")).mark_do_not_check()
        elements = widget.get_element_attr()
        meta_data = self.calculate_meta(elements)
        assert len(elements) == 5, "Expecting there to be 5 elements in this test complex widget"
        assert meta_data['types']['element'] == 3, "Expecting there to be 3 Element types"
        assert meta_data['types']['widget'] == 2, "Expecting there to be 2 Widget types"
        assert meta_data['visible'] == 2, "Expecting there to be 2 visible"
        assert meta_data['invisible'] == 1, "Expecting there to be 1 invisible"
        assert meta_data['do-not-check'] == 2, "Expecting there to be 2 do-not-check"

    def test_complex_widget_with_widget_panel(self):
        widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        visible_widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        visible_widget.visible_panel = testingwebpages.MyComplexPanel(self.driver, Locator.by_xpath("//panel"))
        widget.visible_widget = visible_widget
        elements = widget.get_element_attr()
        meta_data = self.calculate_meta(elements)
        assert len(elements) == 12, "Expecting there to be 12 elements in this test complex widget"
        assert meta_data['types']['element'] == 9, "Expecting there to be 9 Element types"
        assert meta_data['types']['widget'] == 2, "Expecting there to be 2 Widget types"
        assert meta_data['types']['panel'] == 1, "Expecting there to be 1 Panel types"
        assert meta_data['visible'] == 6, "Expecting there to be 6 visible"
        assert meta_data['invisible'] == 3, "Expecting there to be 3 invisible"
        assert meta_data['do-not-check'] == 3, "Expecting there to be 3 do-not-check"

    def test_complex_widget_with_widget_hidden_panel(self):
        widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        visible_widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        visible_widget.invisible_panel = testingwebpages.MyComplexPanel(self.driver, Locator.by_xpath("//panel")).mark_invisible()
        widget.visible_widget = visible_widget
        elements = widget.get_element_attr()
        meta_data = self.calculate_meta(elements)
        assert len(elements) == 9, "Expecting there to be 9 elements in this test complex widget"
        assert meta_data['types']['element'] == 6, "Expecting there to be 6 Element types"
        assert meta_data['types']['widget'] == 2, "Expecting there to be 2 Widget types"
        assert meta_data['types']['panel'] == 1, "Expecting there to be 1 Panel types"
        assert meta_data['visible'] == 4, "Expecting there to be 4 visible"
        assert meta_data['invisible'] == 3, "Expecting there to be 3 invisible"
        assert meta_data['do-not-check'] == 2, "Expecting there to be 2 do-not-check"

    def test_complex_widget_with_widget_do_not_check_panel(self):
        widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//xpath"))
        visible_widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        visible_widget.do_not_check_panel = testingwebpages.MyComplexPanel(self.driver, Locator.by_xpath("//panel")).mark_do_not_check()
        widget.visible_widget = visible_widget
        elements = widget.get_element_attr()
        meta_data = self.calculate_meta(elements)
        assert len(elements) == 9, "Expecting there to be 9 elements in this test complex widget"
        assert meta_data['types']['element'] == 6, "Expecting there to be 6 Element types"
        assert meta_data['types']['widget'] == 2, "Expecting there to be 2 Widget types"
        assert meta_data['types']['panel'] == 1, "Expecting there to be 1 Panel types"
        assert meta_data['visible'] == 4, "Expecting there to be 4 visible"
        assert meta_data['invisible'] == 2, "Expecting there to be 2 invisible"
        assert meta_data['do-not-check'] == 3, "Expecting there to be 3 do-not-check"

    def test_complex_widget_with_iframe(self):
        widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        widget.visible_iframe = testingwebpages.MyComplexIframe(self.driver, Locator.by_xpath("//iframe"))
        elements = widget.get_element_attr()
        meta_data = self.calculate_meta(elements)
        assert len(elements) == 5, "Expecting there to be 5 elements in this test complex widget"
        assert meta_data['types']['element'] == 3, "Expecting there to be 3 Element types"
        assert meta_data['types']['widget'] == 1, "Expecting there to be 1 Widget types"
        assert meta_data['types']['iframe'] == 1, "Expecting there to be 1 IFrame types"
        assert meta_data['visible'] == 3, "Expecting there to be 3 visible"
        assert meta_data['invisible'] == 1, "Expecting there to be 1 invisible"
        assert meta_data['do-not-check'] == 1, "Expecting there to be 1 do-not-check"

    def test_complex_widget_with_widget_iframe(self):
        widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        visible_widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        visible_widget.visible_iframe = testingwebpages.MyComplexIframe(self.driver, Locator.by_xpath("//iframe"))
        widget.visible_widget = visible_widget
        elements = widget.get_element_attr()
        meta_data = self.calculate_meta(elements)
        assert len(elements) == 9, "Expecting there to be 9 elements in this test complex widget"
        assert meta_data['types']['element'] == 6, "Expecting there to be 6 Element types"
        assert meta_data['types']['widget'] == 2, "Expecting there to be 2 Widget types"
        assert meta_data['types']['iframe'] == 1, "Expecting there to be 1 IFrame types"
        assert meta_data['visible'] == 5, "Expecting there to be 5 visible"
        assert meta_data['invisible'] == 2, "Expecting there to be 2 invisible"
        assert meta_data['do-not-check'] == 2, "Expecting there to be 2 do-not-check"

    def test_complex_widget_with_multiple_iframes(self):
        widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        visible_widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        visible_widget.visible_iframe = testingwebpages.MyComplexIframe(self.driver, Locator.by_xpath("//iframe1"))
        widget.visible_widget = visible_widget
        widget.visible_iframe = testingwebpages.MyComplexIframe(self.driver, Locator.by_xpath("//iframe2"))

        # Widgets currently do not have a check if there are multiple iframes defined
        widget.get_element_attr()

    def test_access_element_defined_directly_on_webpage(self):
        widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))

        # None of these should throw an AttributeError
        widget.regular_element_on_widget
        widget.invisible_element_on_widget
        widget.not_checked_element_on_widget

    def test_get_element_attr_dict(self):
        widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        elements = widget.get_element_attr(result_type=dict)
        assert len(elements) == 4, 'Expecting 4 elements'
        assert 'widget' in elements
        assert 'regular_element_on_widget' in elements
        assert 'invisible_element_on_widget' in elements
        assert 'not_checked_element_on_widget' in elements

    def test_get_element_attr_dict_with_iframe(self):
        widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        visible_iframe = testingwebpages.MyComplexIframe(self.driver, Locator.by_xpath("//iframe"))
        widget.visible_iframe = visible_iframe
        elements = widget.get_element_attr(result_type=dict)
        assert len(elements) == 5, 'Expecting 5 elements'
        assert 'widget' in elements
        assert 'regular_element_on_widget' in elements
        assert 'invisible_element_on_widget' in elements
        assert 'not_checked_element_on_widget' in elements
        assert 'visible_iframe' in elements

    def test_get_element_attr_dict_with_expanded_widget(self):
        widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        visible_widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        widget.visible_widget = visible_widget
        elements = widget.get_element_attr(result_type=dict)
        assert len(elements) == 8, 'Expecting 8 elements'
        assert 'widget' in elements
        assert 'regular_element_on_widget' in elements
        assert 'invisible_element_on_widget' in elements
        assert 'not_checked_element_on_widget' in elements
        assert 'visible_widget' in elements
        assert 'visible_widget_regular_element_on_widget' in elements
        assert 'visible_widget_invisible_element_on_widget' in elements
        assert 'visible_widget_not_checked_element_on_widget' in elements

    def test_get_element_attr_dict_with_expanded_iframe(self):
        widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        visible_iframe = testingwebpages.MyComplexIframe(self.driver, Locator.by_xpath("//iframe"))
        widget.visible_iframe = visible_iframe
        elements = widget.get_element_attr(result_type=dict, expand_iframe_elements=True)
        assert len(elements) == 8, 'Expecting 8 elements'
        assert 'widget' in elements
        assert 'regular_element_on_widget' in elements
        assert 'invisible_element_on_widget' in elements
        assert 'not_checked_element_on_widget' in elements
        assert 'visible_iframe' in elements
        assert 'regular_element' in elements
        assert 'invisible_element' in elements
        assert 'not_checked_element' in elements
        assert 'visible_iframe' in elements

    def test_access_element_defined_indirectly_on_webpage(self):
        widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))

        # None of these should throw an AttributeError
        widget.regular_element_on_widget
        widget.invisible_element_on_widget
        widget.not_checked_element_on_widget

    def test_access_element_not_defined_directly_on_webpage(self):
        widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        visible_widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        widget.visible_widget = visible_widget

        # None of these should throw an AttributeError
        widget.regular_element_on_widget
        widget.invisible_element_on_widget
        widget.not_checked_element_on_widget
        widget.visible_widget
        widget.visible_widget_regular_element_on_widget
        widget.visible_widget_invisible_element_on_widget
        widget.visible_widget_not_checked_element_on_widget

    def test_access_element_not_defined_directly_on_webpage_with_duplicates(self):
        widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        visible_iframe = testingwebpages.MyComplexIframe(self.driver, Locator.by_xpath("//iframe"))
        visible_widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        widget.visible_iframe = visible_iframe
        widget.visible_widget = visible_widget

        # None of these should throw an AttributeError
        widget.regular_element_on_widget
        widget.invisible_element_on_widget
        widget.not_checked_element_on_widget
        widget.visible_widget
        widget.visible_widget_regular_element_on_widget
        widget.visible_widget_invisible_element_on_widget
        widget.visible_widget_not_checked_element_on_widget
        widget.visible_iframe
        widget.regular_element
        widget.invisible_element
        widget.not_checked_element

    def test_access_element_not_definedy_on_webpage(self):
        widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        visible_iframe = testingwebpages.MyComplexIframe(self.driver, Locator.by_xpath("//iframe"))
        visible_widget = testingwebpages.MyComplexWidget(self.driver, Locator.by_xpath("//widget"))
        widget.visible_iframe = visible_iframe
        widget.visible_widget = visible_widget

        try:
            widget.foobar
            assert False, "Expecting widget.foobar to throw an AttributeError!"
        except AttributeError:
            pass
