from seleniumpm.webelements.widget import Widget

class Panel(Widget):
    """
    The Panel type is a construct for describing a specific section of a page. This is conceptually the same
    as a Widget type, but a Panel appears to be a generally accepted term. Again, A Panel/Widget is way to
    organize the elements/operations of a section of a Webpage. A Panel can contain an Element type, or even
    another (sub-)Panel/Widget.

    Since a Panel/Widget represents a specific section of a page (e.g. a Header or Footer), then it also
    has a Location associated with it.
    """

    def __init__(self, driver, locator):
        super(Panel, self).__init__(driver=driver, locator=locator)