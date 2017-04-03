from selenium import webdriver
from selenium.webdriver.common.by import By
from seleniumpm.locator import Locator
from seleniumpm.webelements.element import Element
from seleniumpm.webelements.button import Button
from seleniumpm.webelements.checkbox import Checkbox
from seleniumpm.webelements.clickable import Clickable
from seleniumpm.webelements.dropdown import Dropdown
from seleniumpm.webelements.image import Image
from seleniumpm.webelements.link import Link
from seleniumpm.webelements.table import Table
from seleniumpm.webelements.textelement import TextElement
from seleniumpm.webelements.textfield import TextField
from seleniumpm.webelements.radiobutton import RadioButton
from seleniumpm.webelements.widget import Widget
from seleniumpm.webelements.panel import Panel
from seleniumpm.iframe import IFrame
from seleniumpm.webpage import Webpage

class TestClassTypes(object):
    """
    Tests to make sure that all classes are the appropriate type. This is at the core of Selenium PageModel library;
    that there is a relationship between the WebElements on a page to other WebElement types.
    """

    driver = None

    @classmethod
    def setup_class(self):
        server = 'http://localhost:4444/wd/hub'
        capabilities = webdriver.DesiredCapabilities.PHANTOMJS
        self.driver = webdriver.Remote(command_executor=server, desired_capabilities=capabilities)

    @classmethod
    def teardown_class(self):
        if self.driver:
            self.driver.quit()

    def test_element(self):
        """Element --> object"""
        element = Element(self.driver, Locator(By.XPATH, "//foo"))
        assert isinstance(element, Element)
        assert isinstance(element, object)

    def test_webpage(self):
        """Webpage --> object"""
        page = Webpage(self.driver)
        assert isinstance(page, Webpage)
        assert isinstance(page, object)

    def test_button(self):
        """Button --> Element --> object"""
        button = Button(self.driver, Locator(By.XPATH, "//foo"))
        assert isinstance(button, Button)
        assert isinstance(button, Clickable)
        assert isinstance(button, Element)
        assert isinstance(button, object)

    def test_radiobutton(self):
        """RadioButton --> Element --> object"""
        button = RadioButton(self.driver, Locator(By.XPATH, "//foo"))
        assert not isinstance(button, Button)
        assert isinstance(button, RadioButton)
        assert isinstance(button, Clickable)
        assert isinstance(button, Element)
        assert isinstance(button, object)

    def test_checkbox(self):
        """Checkbox --> Clickable --> Element --> object"""
        checkbox = Checkbox(self.driver, Locator(By.XPATH, "//foo"))
        assert isinstance(checkbox, Checkbox)
        assert isinstance(checkbox, Clickable)
        assert isinstance(checkbox, Element)
        assert isinstance(checkbox, object)

    def test_clickable(self):
        """Clickable --> Element --> object"""
        clickable = Clickable(self.driver, Locator(By.XPATH, "//foo"))
        assert isinstance(clickable, Clickable)
        assert isinstance(clickable, Element)
        assert isinstance(clickable, object)

    def test_dropdown(self):
        """Dropdown --> Clickable --> Element --> object"""
        dropdown = Dropdown(self.driver, Locator(By.XPATH, "//foo"))
        assert isinstance(dropdown, Dropdown)
        assert isinstance(dropdown, Clickable)
        assert isinstance(dropdown, Element)
        assert isinstance(dropdown, object)

    def test_image(self):
        """Image --> Element --> object"""
        image = Image(self.driver, Locator(By.XPATH, "//foo"))
        assert isinstance(image, Image)
        assert isinstance(image, Element)
        assert isinstance(image, object)

    def test_link(self):
        """Link --> Clickable --> Element --> object"""
        link = Link(self.driver, Locator(By.XPATH, "//foo"))
        assert isinstance(link, Link)
        assert isinstance(link, Clickable)
        assert isinstance(link, Element)
        assert isinstance(link, object)

    def test_table(self):
        """Table --> Element --> object"""
        table = Table(self.driver, Locator(By.XPATH, "//foo"))
        assert isinstance(table, Table)
        assert isinstance(table, Element)
        assert isinstance(table, object)

    def test_textelement(self):
        """TextElement --> Element --> object"""
        textelement = TextElement(self.driver, Locator(By.XPATH, "//foo"))
        assert isinstance(textelement, TextElement)
        assert isinstance(textelement, Element)
        assert isinstance(textelement, object)

    def test_textfield(self):
        """TextField --> TextElement --> Element --> object"""
        textfield = TextField(self.driver, Locator(By.XPATH, "//foo"))
        assert isinstance(textfield, TextField)
        assert isinstance(textfield, TextElement)
        assert isinstance(textfield, Element)
        assert isinstance(textfield, object)

    def test_widget(self):
        """Widget --> Clickable --> Element --> object"""
        widget = Widget(self.driver, Locator(By.XPATH, "//foo"))
        assert isinstance(widget, Widget)
        assert isinstance(widget, Clickable)
        assert isinstance(widget, Element)
        assert isinstance(widget, object)

    def test_panel(self):
        """Panel --> Widget --> Clickable --> Element --> object"""
        panel = Panel(self.driver, Locator(By.XPATH, "//foo"))
        assert isinstance(panel, Panel)
        assert isinstance(panel, Widget)
        assert isinstance(panel, Clickable)
        assert isinstance(panel, Element)
        assert isinstance(panel, object)

    def test_iframe(self):
        """IFrame --> Panel --> Widget --> Clickable --> Element --> object"""
        iframe = IFrame(self.driver, Locator(By.XPATH, "//foo"))
        assert isinstance(iframe, IFrame)
        assert isinstance(iframe, Panel)
        assert isinstance(iframe, Widget)
        assert isinstance(iframe, Clickable)
        assert isinstance(iframe, Element)
        assert isinstance(iframe, object)
