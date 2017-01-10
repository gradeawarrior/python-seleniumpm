from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Webpage(object):

    def __init__(self, driver, url=None):
        self.driver = driver
        self.url = url

    def open(self, url=None):
        if url:
            self.driver.get(url)
        elif self.url:
            self.driver.get(self.url)
        else:
            raise AttributeError("Url is not defined!")
        return self

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()

    def get_title(self):
        return self.driver.title

    def wait_for_title(self, title, timeout=10):
        WebDriverWait(driver=self.driver, timeout=timeout).until(EC.title_contains(title))
        return self

    def wait_for_page_load(self):
        raise NotImplementedError

    def validate(self):
        raise NotImplementedError
