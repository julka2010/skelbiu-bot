import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    WebDriverException,
    TimeoutException,
)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class SkelbiuLtBot():
    urls = {
        'login': 'https://www.skelbiu.lt/users/signin',
        'new': 'https://www.skelbiu.lt/naujas-skelbimas/',
        'my_active_ads': 'https://www.skelbiu.lt/mano-skelbimai/',
        'my_passive_ads': 'https://www.skelbiu.lt/mano-skelbimai/index.php?mod=myData&action=myAds&tab=1&p=1&tab=0',
    }
    locators = {
        'delete': {
            'in_list': (By.XPATH, '//a[contains(@class, "deleteLink")]'),
            'confirm_button': (
                By.XPATH, '//input[@type="button" and @id="deleteButtonYes"]'
            )
        },
        'login': {
            'username': (By.XPATH, '//*[@id="user"]/input'),
            'password': (By.XPATH, '//input[@id="password"]'),
            'submit': (By.XPATH, '//input[@type="submit"]'),
        },
        'new': {
            'action': (By.XPATH, '//input[@id="propose"]'),
            'title': (By.XPATH, '//input[@id="adsName"]'),
            'description': (By.XPATH, '//*[@id="adsDesciption"]'),
            'photos': (By.XPATH, '//form//input[@type="file"]'),
            'photos_progress_bar': (
                By.XPATH, '//form//*[contains(@class, "progress-bar")]'),
            'being': (By.XPATH, '//input[@id="privateUser"]'),
            'price': (By.XPATH, '//input[@id="adsPrice"]'),
            'phone': (By.XPATH, '//input[@id="adsPhone"]'),
            'city': (By.XPATH, '//*[contains(@class, "citiesAreaOneCity")]'),
            'user_type': (By.XPATH, '//radio[@id="privateUser"]'),
            'submit': (By.XPATH, '//*[@id="orderButton"]/a'),
            'submit_chosen_payables': (By.XPATH, '//form[@id="submitForm"]'),
        },
    }

    def _find_category_element(self, depth, category):
        words = category.split()
        _xpath_list = 'ul[@data-area="{depth}"]'.format(depth=depth)
        _xpath_for_words = (
            'contains(., "' +
            '") and contains(., "'.join(words) +
            '")'
        )
        _xpath = '//' + _xpath_list + '/li//text()[' + _xpath_for_words + ']/..'
        return self.wait.until(
            EC.element_to_be_clickable((By.XPATH, _xpath)))

    def __init__(self, driver, max_wait=10, **kwds):
        super().__init__(**kwds)
        self.driver = driver
        self.driver.implicitly_wait(max_wait)
        self.wait = WebDriverWait(driver, 3 * max_wait)

    def delete_all_ads(self):
        def _delete_all_in_list():
            while True:
                try:
                    el_delete_ad = self.driver.find_element(
                        *self.locators['delete']['in_list']
                    )
                except NoSuchElementException:
                    break
                else:
                    try:
                        el_delete_ad.click()
                    except WebDriverException:
                        continue
                    try:
                        self.driver.find_element(
                            *self.locators['delete']['confirm_button']).click()
                    except (WebDriverException, NoSuchElementException):
                        continue
        self.driver.get(self.urls['my_active_ads'])
        _delete_all_in_list()
        self.driver.get(self.urls['my_passive_ads'])
        _delete_all_in_list()

    def login(self, username, password):
        self.driver.get(self.urls['login'])
        username_field = self.driver.find_element(*self.locators['login']['username'])
        username_field.clear()
        username_field.send_keys(username)
        password_field = self.driver.find_element(*self.locators['login']['password'])
        password_field.clear()
        password_field.send_keys(password)
        submit_button = self.driver.find_element(*self.locators['login']['submit'])
        return submit_button.submit()

    def publish_ad(
            self,
            category,
            action,
            title,
            description,
            photos,
            price,
            phone,
            city,
            ):
        if not action.lower() in ("propose", "siūlau"):
            raise NotImplementedError()
        self.driver.get(self.urls['new'])
        for depth, subcategory in enumerate(category):
            try:
                el = self._find_category_element(depth + 1, subcategory)
            except TimeoutException:
                raise TimeoutException(subcategory)
            el.click()
        el_action = self.wait.until(
            EC.element_to_be_clickable(self.locators['new']['action']))
        el_action.click()
        el_title = self.driver.find_element(*self.locators['new']['title'])
        el_title.send_keys(title)
        el_description = self.driver.find_element(
            *self.locators['new']['description'])
        el_description.send_keys(description)
        el_price = self.driver.find_element(*self.locators['new']['price'])
        el_price.send_keys(price)
        for photo in photos:
            el_photo = self.wait.until(
                EC.presence_of_element_located(self.locators['new']['photos']))
            el_photo.send_keys(photo)
            self.wait.until(EC.invisibility_of_element_located(
                self.locators['new']['photos_progress_bar']
            ))
        el_being = self.driver.find_element(*self.locators['new']['being'])
        try:
            el_being.click()
        except WebDriverException:
            pass
        el_phone = self.driver.find_element(*self.locators['new']['phone'])
        el_phone.clear()
        el_phone.send_keys('+370' + phone)
        el_city = self.driver.find_element(*self.locators['new']['city'])
        el_city.send_keys(city)
        self.driver.find_element(*self.locators['new']['submit']).submit()
        try:
            self.driver.find_element(
                *self.locators['new']['submit_chosen_payables']).submit()
        except NoSuchElementException:
            pass
