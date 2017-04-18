from seleniumpm.webpage import Webpage
from seleniumpm.iframe import IFrame


class GooglePage(Webpage):
    def __init__(self, driver, url=None):
        super(GooglePage, self).__init__(driver=driver, url=url)
        self.iframe = FictionalIframe(driver)


class FictionalIframe(IFrame):
    def __init__(self, driver, locator=None):
        super(FictionalIframe, self).__init__(driver=driver, locator=locator)