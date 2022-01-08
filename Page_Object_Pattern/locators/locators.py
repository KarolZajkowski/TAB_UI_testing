from selenium.webdriver.common.by import By


class FirstCycleStudiesLocators:

    policy_notification_xpath = (By.XPATH, "//button[text()='Akceptuję politykę plików cookies']")
    choose_studies_xpath = (By.XPATH, "//span/span[text()[normalize-space()='Studia i szkolenia']]")
    first_year_studies_xpath = (By.XPATH, "//a/span[text()[normalize-space()='Studia I stopnia']]")
    directions_specialties_xpath = (By.XPATH, "//div[@class='layout-content']//li/a[text()='Kierunki i specjalności']")
    studies_description_class = (By.CLASS_NAME, "study-description")
    checkbox_wroclaw_xpath = (By.XPATH, "//body//label/span[text()='Wrocław']/../div[@class='box']") #/html/body/div[1]/div/main/div/div/div[3]/div/aside/div/div[1]/div[9]/label/span
    checkbox_inzynierskie_xpath = (By.XPATH, "//body//label/span[text()='Studia inżynierskie']/../div[@class='box']")
    # checkbox_inzynierskie_xpath = (By.XPATH, "//label/span[text()='Studia inżynierskie']/../input[@type='checkbox']")

    popup_call_to_me_later_xpath = (By.XPATH, "//body//div/button[text()='Zadzwońcie do mnie teraz']")
    zapisz_sie_online_xpath = (By.XPATH, "//header//div/a[text()[normalize-space()='Zapisz się online']]")
    sort_selector_xpath = (By.XPATH, "//main//div[@class='current-selected']")

    table_banner_html = ('div', {'class': 'direction-title-wrap studies_i wsb'})




