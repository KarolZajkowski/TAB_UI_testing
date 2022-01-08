import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait


class DecoCallToMeNotification:
    """ reuse decorator for skipp 'Call to me later' """
    def __init__(self, func):
        self.func = func

    def __call__(self, **kwargs):
        """
        :param func: function to check with possible notification
        :return: Method just check and skipp 'call-to-me-later' notification if will show up
        and Finally return main function
        """
        try:
            print("\t>>> check condition with until segment")
            wait = WebDriverWait(kwargs['driver'], 3, 0.5,
                                 ignored_exceptions=(NoSuchElementException, StaleElementReferenceException))
            wait.until(
                EC.visibility_of_any_elements_located(kwargs['locator']))
            kwargs['driver'].find_element(*kwargs['locator']).send_keys(Keys.ESCAPE)

        except TimeoutException:
            print('Popup not show - skipped')

        finally:
            # find xpath
            kwargs['find_a_screen_xpath'] = self.xpath_soup(kwargs['studies'])
            self.func(**kwargs)

    @staticmethod
    def xpath_soup(element):
        # type: (typing.Union[bs4.element.Tag, bs4.element.NavigableString]) -> str
        """
        Generate xpath from BeautifulSoup4 element.
        :param element: BeautifulSoup4 element.
        :type element: bs4.element.Tag or bs4.element.NavigableString
        :return: xpath as string
        :rtype: str
        :from https://gist.github.com/ergoithz/6cf043e3fdedd1b94fcf
        Usage
        ----- /
        `>>> import bs4 /
        `>>> html = (
        ...     '<html><head><title>title</title></head>'
        ...     '<body><p>p <i>1</i></p><p>p <i>2</i></p></body></html>'
        ...     )
        `>>> soup = bs4.BeautifulSoup(html, 'html.parser')
        `>>> xpath_soup(soup.html.body.p.i)
        '/html/body/p[1]/i'
        `>>> import bs4
        `>>> xml = '<doc><elm/><elm/></doc>'
        `>>> soup = bs4.BeautifulSoup(xml, 'lxml-xml')
        `>>> xpath_soup(soup.doc.elm.next_sibling)
        '/doc/elm[2]'
        """
        components = []
        child = element if element.name else element.parent
        for parent in child.parents:  # type: bs4.element.Tag
            siblings = parent.find_all(child.name, recursive=False)
            components.append(
                child.name if 1 == len(siblings) else '%s[%d]' % (
                    child.name,
                    next(i for i, s in enumerate(siblings, 1) if s is child)
                    )
                )
            child = parent
        components.reverse()
        return '/%s' % '/'.join(components)


def xpath_soup(element):
    # type: (typing.Union[bs4.element.Tag, bs4.element.NavigableString]) -> str
    """
    Generate xpath from BeautifulSoup4 element.
    :param element: BeautifulSoup4 element.
    :type element: bs4.element.Tag or bs4.element.NavigableString
    :return: xpath as string
    :rtype: str
    :from https://gist.github.com/ergoithz/6cf043e3fdedd1b94fcf
    Usage
    ----- /
    `>>> import bs4 /
    `>>> html = (
    ...     '<html><head><title>title</title></head>'
    ...     '<body><p>p <i>1</i></p><p>p <i>2</i></p></body></html>'
    ...     )
    `>>> soup = bs4.BeautifulSoup(html, 'html.parser')
    `>>> xpath_soup(soup.html.body.p.i)
    '/html/body/p[1]/i'
    `>>> import bs4
    `>>> xml = '<doc><elm/><elm/></doc>'
    `>>> soup = bs4.BeautifulSoup(xml, 'lxml-xml')
    `>>> xpath_soup(soup.doc.elm.next_sibling)
    '/doc/elm[2]'
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:  # type: bs4.element.Tag
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name if 1 == len(siblings) else '%s[%d]' % (
                child.name,
                next(i for i, s in enumerate(siblings, 1) if s is child)
                )
            )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)
