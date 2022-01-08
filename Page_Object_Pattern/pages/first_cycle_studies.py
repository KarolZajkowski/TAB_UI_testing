
import time
from bs4 import BeautifulSoup

import allure
from allure_commons.types import AttachmentType

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from selenium.common.exceptions import TimeoutException, NoSuchElementException, \
    StaleElementReferenceException, ElementClickInterceptedException, MoveTargetOutOfBoundsException

from Page_Object_Pattern.locators.locators import FirstCycleStudiesLocators
"""" Karol Zajkowski """


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
            time.sleep(1)
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


class FirstCycleStudies:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10, 0.5,
                                  ignored_exceptions=(NoSuchElementException, StaleElementReferenceException))
        self.action = ActionChains(driver)

        self.policy_notification = FirstCycleStudiesLocators.policy_notification_xpath
        self.choose_studies = FirstCycleStudiesLocators.choose_studies_xpath
        self.first_year_studies = FirstCycleStudiesLocators.first_year_studies_xpath
        self.directions_specialties = FirstCycleStudiesLocators.directions_specialties_xpath
        self.studies_description = FirstCycleStudiesLocators.studies_description_class
        self.checkbox_wroclaw_locator = FirstCycleStudiesLocators.checkbox_wroclaw_xpath
        self.checkbox_inzynierskie_locator = FirstCycleStudiesLocators.checkbox_inzynierskie_xpath

        self.popup_call_to_me_later = FirstCycleStudiesLocators.popup_call_to_me_later_xpath
        self.zapisz_sie_online = FirstCycleStudiesLocators.zapisz_sie_online_xpath
        self.sort_selector = FirstCycleStudiesLocators.sort_selector_xpath
        self.table_banner = FirstCycleStudiesLocators.table_banner_html

    def open_page(self, url):
        self.driver.get(url)

    @allure.step("1. Policy notification popup acceptable")
    def policy_notification_popup(self):
        allure.attach(self.driver.get_screenshot_as_png(), name="popup_policy", attachment_type=AttachmentType.PNG)
        try:
            self.wait.until(
                EC.element_to_be_clickable(
                    self.policy_notification)).click()

        except TimeoutException:
            raise TimeoutError("Not notification available")

    @allure.step("2. Choose studies")
    def choose_studies_bar(self):  # change web page - 2nd
        self.wait.until(
            EC.element_to_be_clickable(
                self.choose_studies)).click()
        allure.attach(self.driver.get_screenshot_as_png(), name="Choose_studies", attachment_type=AttachmentType.PNG)
        self.driver.find_element(*self.first_year_studies).click()

    @allure.step("3. Change tab")
    def directions_and_specialties_tab(self):
        self.driver.find_element(*self.directions_specialties).click()

        # check len of the studies description
        # more then required for wait content display
        self.wait.until(
            lambda wd: len(wd.find_elements(*self.studies_description)) >= 3)
        allure.attach(self.driver.get_screenshot_as_png(), name="tab_changed", attachment_type=AttachmentType.PNG)

    @allure.step("4. Select checkbox wroclaw")
    def select_checkbox_wroclaw_chrome(self):
        """Mark checkbox - city wroclaw"""
        checkbox_wroclaw = self.driver.find_element(*self.checkbox_wroclaw_locator)

        try:
            self.action.move_to_element(checkbox_wroclaw).perform()  # chrome
            time.sleep(2)
            checkbox_wroclaw.click()  # chrome

        except ElementClickInterceptedException:  # popup shows up
            self.wait.until(EC.visibility_of_any_elements_located(self.popup_call_to_me_later))
            self.driver.find_element(*self.popup_call_to_me_later).send_keys(Keys.ESCAPE)

            self.action.move_to_element(checkbox_wroclaw).perform()
            if checkbox_wroclaw.is_selected():
                checkbox_wroclaw.click()

        finally:
            allure.attach(self.driver.get_screenshot_as_png(), name="checkbox_wroclaw",
                          attachment_type=AttachmentType.PNG)

    @allure.step("5. Select checkbox engineering studies")
    def select_checkbox_inzynierskie_chrome(self):
        """Mark checkbox - city engineering studies"""
        checkbox_inzynierskie = self.driver.find_element(*self.checkbox_inzynierskie_locator)

        try:
            self.action.move_to_element(checkbox_inzynierskie).perform()  # chrome
            time.sleep(2)
            checkbox_inzynierskie.click()  # chrome

        except ElementClickInterceptedException:  # popup shows up
            self.wait.until(EC.visibility_of_any_elements_located(self.popup_call_to_me_later))
            self.driver.find_element(*self.popup_call_to_me_later).send_keys(Keys.ESCAPE)

            self.action.move_to_element(checkbox_inzynierskie).perform()
            if checkbox_inzynierskie.is_selected():
                checkbox_inzynierskie.click()

        finally:
            allure.attach(self.driver.get_screenshot_as_png(), name="checkbox_inzynierskie",
                          attachment_type=AttachmentType.PNG)

    @allure.step("4. Select checkbox wroclaw")
    def select_checkbox_wroclaw_firefox(self):
        checkbox_wroclaw = self.driver.find_element(*self.checkbox_wroclaw_locator)

        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox_wroclaw)  # firefox
            time.sleep(2)
            self.driver.execute_script("argument[0].click();", checkbox_wroclaw)  # firefox

        except ElementClickInterceptedException:  # popup shows up
            self.wait.until(EC.visibility_of_any_elements_located(self.popup_call_to_me_later))
            self.driver.find_element(*self.popup_call_to_me_later).send_keys(Keys.ESCAPE)

            self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox_wroclaw)  # firefox
            if checkbox_wroclaw.is_selected():
                self.driver.execute_script("argument[0].click();", checkbox_wroclaw)  # firefox

        finally:
            allure.attach(self.driver.get_screenshot_as_png(), name="checkbox_wroclaw",
                          attachment_type=AttachmentType.PNG)

    @allure.step("5. Select checkbox engineering studies")
    def select_checkbox_inzynierskie_firefix(self):
        checkbox_inzynierskie = self.driver.find_element(*self.checkbox_inzynierskie_locator)

        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox_inzynierskie)  # firefox
            time.sleep(2)
            self.driver.execute_script("argument[0].click();", checkbox_inzynierskie)  # firefox

        except ElementClickInterceptedException:  # popup shows up
            self.wait.until(EC.visibility_of_any_elements_located(self.popup_call_to_me_later))
            self.driver.find_element(*self.popup_call_to_me_later).send_keys(Keys.ESCAPE)

            self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox_inzynierskie)  # firefox
            if checkbox_inzynierskie.is_selected():
                self.driver.execute_script("argument[0].click();", checkbox_inzynierskie)  # firefox

        finally:
            allure.attach(self.driver.get_screenshot_as_png(), name="checkbox_inzynierskie",
                          attachment_type=AttachmentType.PNG)

    @allure.step("Assertion check is 'Zapisz się online' is visible")
    def is_zapisz_sie_online_displayed(self):
        """ Sign up online is checked in this step """
        return self.driver.find_element(*self.zapisz_sie_online).is_displayed()

    @allure.step("Assertion check sorting selector is displayed on the page ")
    def is_sort_selector_displayed(self):
        """ Whether sorting is displayed"""
        return self.driver.find_element(*self.zapisz_sie_online).is_displayed()

    @allure.step("Assertion check len of elements >= {1}")
    def studies_description_bar_xpath(self, studies_wroclaw_eng_len):
        """ In this step, the number of available studies should be checked - compare greater or equal """
        return len(self.driver.find_elements(*self.studies_description)) >= studies_wroclaw_eng_len

    @allure.step("Assertion check banner table")
    def parsed_element_and_make_screen(self):
        """ This step check web parcel of 3 elements (image, title, city)"""
        page_html = self.driver.page_source
        parsed_html = BeautifulSoup(page_html, 'html.parser')
        i = 1
        list_of_elements = []

        @DecoCallToMeNotification
        def _inner_func(**kwargs):
            nonlocal i, list_of_elements

            image = kwargs['studies'].find('img')
            title = kwargs['studies'].find('span', {'class': 'title'})
            city = kwargs['studies'].find('div', {'class': 'cities'})

            all_take_a_screen_xpath = kwargs['find_a_screen_xpath']
            picture_locator = self.driver.find_element(By.XPATH, all_take_a_screen_xpath)
            try:
                self.action.move_to_element(picture_locator).perform()
            except MoveTargetOutOfBoundsException:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", picture_locator)  # firefox

            list_of_elements.append((image, title, city))
            allure.attach(self.driver.get_screenshot_as_png(), name=f"banner_{i}",
                          attachment_type=AttachmentType.PNG)
            i += 1
            # time.sleep(2)

        for studies in parsed_html.find_all(*self.table_banner):
            _inner_func(driver=self.driver, locator=self.popup_call_to_me_later, studies=studies)

        return list_of_elements

