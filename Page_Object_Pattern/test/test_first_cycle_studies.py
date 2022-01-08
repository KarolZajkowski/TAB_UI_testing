
import time

import allure
import pytest

from Page_Object_Pattern.pages.first_cycle_studies import FirstCycleStudies
"""" Karol Zajkowski """


@pytest.mark.usefixtures('setup')
class TestFirstCycleStudies:

    @allure.title("First-Cycle Studies Wroclaw")
    @allure.description("Complex auto TC for search engineering, First-Cycle Studies in Wroclaw")
    @pytest.mark.parametrize("url, studies_wroclaw_len", [("https://www.wsb.pl/", 3)])  # parameters from request
    def test_wroclaw_first_cycle(self, url, studies_wroclaw_len):
        search_first_cycle_studies = FirstCycleStudies(self.driver)
        search_first_cycle_studies.open_page(url)
        search_first_cycle_studies.policy_notification_popup()
        time.sleep(5)  # flowing shift notification | wait.until > event this method throw error thy why sleep is needed

        search_first_cycle_studies.choose_studies_bar()
        search_first_cycle_studies.directions_and_specialties_tab()
        if self.web_browser == 'chrome':
            search_first_cycle_studies.select_checkbox_wroclaw_chrome()
            search_first_cycle_studies.select_checkbox_inzynierskie_chrome()
        elif self.web_browser == 'firefox':
            """methods are not ready - you have to switch to java and scrolling doesn't work very well"""
            search_first_cycle_studies.select_checkbox_wroclaw_firefox()
            search_first_cycle_studies.select_checkbox_inzynierskie_firefix()

        time.sleep(5)  # reload new content after selected checkbox

        assert search_first_cycle_studies.is_zapisz_sie_online_displayed()  # Zapisz się online
        assert search_first_cycle_studies.is_sort_selector_displayed()  # sort selector
        assert search_first_cycle_studies.studies_description_bar_xpath(studies_wroclaw_len)  # len of studies

        # checking image, title and city
        elements = search_first_cycle_studies.parsed_element_and_make_screen()
        for parsed_element in elements:
            assert parsed_element[0] is not None
            assert parsed_element[1] is not None
            assert parsed_element[2] is not None

        # elements = search_first_cycle_studies.get_element_from_baner()
        # assert elements
        # i = 1
        # for studies in elements:
        #     studies_param = search_first_cycle_studies.parsed_element_and_make_screen(studies, i)
        #     assert studies_param[0] is not None
        #     assert studies_param[1] is not None
        #     assert studies_param[2] is not None
        #     i += 1
