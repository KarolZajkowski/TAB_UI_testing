## Page UI testing
- Program prepered for https://www.wsb.pl/


_**Envoronment**_
  > * Install Python 3.9.1 (3+) and add to environment variable
  > * Install JAVA JDK and add to your environment variable
  > * If Selenium Grid will be used – be sure that you have **chrome client** web browser (webdriver inside package)
  > * If Selenium Grid will be used – be sure that you have **firefox client** web browser (webdriver inside package)
  > * Install allure: https://docs.qameta.io/allure/
  

_**Usage:**_
> 1. Run install_all_and_run.bat and wait for the process to complete
>> - script create virtual environment
>> - runs env
>> - install requirements
>> - run pytest with allure 
>> - create report in allure service
>> 
>> green dot - pass
>> red dot - fail
>>...F (3xpass, 1 fail)

![Screenshot_1](https://user-images.githubusercontent.com/84734946/148660699-dccd5912-a50d-4151-bf7b-dc40708c5e04.png)

> 2. Can be usage in IDLE
>> - python 3+ (3.9.1) 
>> - create project with venv
>> - install requirements.txt from repository
>> - run/debug configuration > add pytest
>>
>> pytest --alluredir=<<your_dir_from_Page_Object_Pattern>>\\report
>>
>> allure serve <<your_dir_from_Page_Object_Pattern>>\\report



_**OPTIONS:**_
> 1. Selenium grid (remote) or local (ChromeDriverManager)
> > * open Page_Object_Pattern\utils\driver_factory.py file
> > * variable LAUNCH_DRIVER [remote: will use selenium grid, local: will use ChromeDriverManager]

![Screenshot_2](https://user-images.githubusercontent.com/84734946/148661377-e86a5282-65e8-4269-812a-5aac3ce5a807.png)

> 2. Run multiple webdriver 
> > * add webdriver to params list in conftest.py

![Screenshot_4](https://user-images.githubusercontent.com/84734946/148661527-1bc0e71f-8d72-427b-919f-6b1d024e7f1a.png)

> 3. Params for test 
> > * url - url for testing
> > * tudies_wroclaw_len - minimum number of elements tab

![Screenshot_5](https://user-images.githubusercontent.com/84734946/148661572-a989d226-3e09-4eab-8128-e3428bf2c188.png)
