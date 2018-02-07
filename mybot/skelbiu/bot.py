import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException,
)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

urls = {
    'login': 'https://www.skelbiu.lt/users/signin',
}

credentials = {
    'username': 'bin.trash+skelbiu@protonmail.com',
    'password': '8*NM5nKrF2WbRXSfFJpf',
}

locators = {
    'login': {
        'username': (By.XPATH, '//*[@id="user"]/input'),
        'password': (By.XPATH, '//input[@id="password"]'),
        'submit': (By.XPATH, '//input[@type="submit"]'),
        }
    }

class Advertisement():
    urls = {'new': 'https://www.skelbiu.lt/naujas-skelbimas/'}
    locators = {
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
                'submit': (By.XPATH, '//*[@id="orderButton"]'),
            }
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

    def publish(
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


def login(driver):
    driver.get(urls['login'])
    username_field = driver.find_element(*locators['login']['username'])
    username_field.send_keys(credentials['username'])
    password_field = driver.find_element(*locators['login']['password'])
    password_field.send_keys(credentials['password'])
    submit_button = driver.find_element(*locators['login']['submit'])
    return submit_button.submit()
