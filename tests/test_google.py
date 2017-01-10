from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from testlib.google_page import GooglePage

class TestGoogle():

    """
        try {
            // Specifying where the tests will run will be based on URL
            DesiredCapabilities capabilities = new DesiredCapabilities();
            capabilities.setBrowserName("firefox");
            browser = new RemoteWebDriver(new URL(server), capabilities);
            Selenium sel = new SeleniumWebdriver(browser, new URI(google_url));
            GooglePageWebDriver google = new GooglePageWebDriver(sel);
            String searchTerm = "Cheese!";

            // Open Gurukula

            // And now use this to visit Google
            google.open();

            // Enter something to search for
            google.searchField.type(searchTerm);

            // Now submit the form. WebDriver will find the form for us from the element
            google.searchField.submit();

            // Check the title of the page
            String title = google.getTitle();
            System.out.println("Page title is: " + title);
            // Should see: "cheese! - Google Search"
            title = google.waitForTitle(searchTerm).getTitle();
            System.out.println("Page title is: " + title);
            Assert.assertEquals(title, searchTerm + " - Google Search", "Expecting the title to be the same as the search term");
            google.validate();
        } finally {
            //Close the browser
            if (browser != null)
                browser.quit();
        }
    """
    def test_search(self):
        server = 'http://localhost:4444/wd/hub'
        google_url = 'https://www.google.com'
        capabilities = {
            'browserName': 'firefox'
        }
        browser = None
        search_term = 'Cheese!'

        try:
            browser = RemoteWebDriver(command_executor=server, desired_capabilities=capabilities)
            google_page = GooglePage(browser, url=google_url)

            # And now use this to visit Google
            google_page.open()

            # Enter something to search for
            google_page.search_field.type(search_term)

            # Now submit the form. WebDriver will find the form for us from the element
            google_page.search_field.submit()

            # Check the title of the page
            title = google_page.get_title()
            print "Page title is: {}".format(title)
            # Should see: "cheese! - Google Search"
            title = google_page.wait_for_title(search_term).get_title()
            print "Page title is: {}".format(title)
            assert search_term in title, "Expected '{}' in '{}'".format(search_term, title)
            google_page.validate()
        finally:
            if browser:
                browser.quit()
