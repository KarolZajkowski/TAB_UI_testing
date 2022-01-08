from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
"""" Karol Zajkowski """

LAUNCH_DRIVER = 'remote'  # 'local' >> use webdriver_manager :: 'remote' >> use webdriver.Remote - for grid


class DriverFactory:

    @staticmethod
    def get_driver(browser):
        if browser == 'chrome':
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-extensions")
            options.add_argument('--disable-notifications')  # notification handler
            options.add_argument('--ignore-certificate-errors')
            options.add_argument("--no-sandbox")
            options.add_argument("--verbose")

            if LAUNCH_DRIVER == 'local':
                return webdriver.Chrome(ChromeDriverManager().install(), options=options)  # local
            elif LAUNCH_DRIVER == 'remote':
                options.set_capability("browserName", "chrome")  # grid
                return webdriver.Remote("http://localhost:4444/wd/hub", options=options)  # grid

        elif browser == 'firefox':
            options = webdriver.FirefoxOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-extensions")
            options.add_argument('--disable-notifications')  # notification handler
            options.add_argument('--ignore-certificate-errors')
            options.add_argument("--no-sandbox")
            options.add_argument("--verbose")

            if LAUNCH_DRIVER == 'local':
                # service = FirefoxService(executable_path=GeckoDriverManager().install())  # local future
                # return webdriver.Firefox(service=service, options=options)  # local future
                return webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)  # local
            elif LAUNCH_DRIVER == 'remote':
                options.set_capability("browserName", "firefox")  # grid
                return webdriver.Remote("http://localhost:4444/wd/hub", options=options)  # grid

        raise Exception('Provide valid driver name')