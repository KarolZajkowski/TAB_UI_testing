import sys
import pytest
import requests

from Page_Object_Pattern.utils.driver_factory import DriverFactory, LAUNCH_DRIVER


@pytest.fixture(scope='session')
def check_environment():
    """ test prepared just for windows environment
        :skip system version"""
    if not sys.platform.startswith("win"):
        pytest.mark.skipif('Test prepared for windows')
    assert sys.platform == 'win32'


@pytest.fixture(scope='class')
def check_connection(check_environment):
    """ Checking connection with endpoint - just respond
        :skip status code"""
    r = requests.get('https://www.wsb.pl/')  # need to be changed
    print(f"\n>> Connected response code: {r.status_code}")
    if r.status_code != 200:
        pytest.mark.skipif('No connection! - check webpage manualy')


@pytest.fixture(scope='session')
def setup_server_and_node():
    """ Process launch """
    if LAUNCH_DRIVER != 'remote':
        return

    from Page_Object_Pattern.utils.lunch_remote_server import Main
    underTest = Main()
    underTest.main()


@pytest.fixture(params=['chrome', 'firefox', 'chrome'])
def setup(request, check_connection, setup_server_and_node):
    """
    :param request: remote webdrver >> in 2 way - remote (selenium grid & local DriverManager)
    :param check_connection: endpoint check for connection
    :return:
        1. webdriver for POP
        2. also close driver after test
    """
    print(f"\n\n\n\t>>> Test started for platform: {request.param} --------\n\n")
    driver = DriverFactory.get_driver(request.param)
    driver.implicitly_wait(15)
    request.cls.driver = driver
    request.cls.web_browser = request.param
    yield
    driver.quit()
