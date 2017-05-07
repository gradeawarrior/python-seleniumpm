# highlevel selenium debug flag
debug = False

# Page and element timeouts for Selenium
page_timeout_in_sec = 30
element_timeout_in_sec = 10

def reset_timeouts():
    global page_timeout_in_sec
    global element_timeout_in_sec
    page_timeout_in_sec = 30
    element_timeout_in_sec = 10

# Screenshot variables
screenshot_dir = "./screenshots"
screenshot_enabled = True
test_screenshot_enabled = True

# Selenium Checks
disable_check_for_selenium_webdriver = False
failfast_check_element = True

# Debugging configs
debug_logger_object = None
