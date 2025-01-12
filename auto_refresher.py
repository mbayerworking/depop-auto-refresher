""" This module allows Depop store owners to automatically refresh their listings 24/7."""
from time import sleep
from selenium.common.exceptions import TimeoutException, NoSuchWindowException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver.v2 as uc
import time
import random


class AutoRefresher:
    """ This class can login, move sold items to bottom, and refresh listings for a depop profile"""

    def __init__(self, indefinite=False, frequency=3600):
        self.driver = uc.Chrome()
        self.wait = WebDriverWait(self.driver, 20)
        self.indefinite = indefinite
        self.frequency = frequency

    def login(self, username, password):
        """
        Logins to user's profile
        :param username: username of store owner
        :param password: password of store owner
        :return: True if successful
        """
        driver = self.driver
        wait = self.wait
        with driver:
            driver.get("https://www.depop.com/login/")
            #driver.refresh()
            #username_input = driver.find_element_by_id("username")
            #password_input = driver.find_element_by_id("password")
            # time.sleep(random.randint(3,15))
            # username_input.send_keys(username)
            # time.sleep(random.randint(3,15))
            # password_input.send_keys(password)
            # time.sleep(random.randint(3,15))
            # password_input.send_keys(Keys.RETURN)
            wait.until(EC.title_is("Depop - buy, sell, discover unique fashion"))
            driver.get("https://www.depop.com/" + username.lower())
        return True

    def move_sold_items_down(self):
        """
        Moves the sold items down on the user's depop profile (Must be logged in first)
        :return: True if successful
        """
        driver = self.driver
        wait = self.wait
        with driver:
            move_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#main > div:nth-child(1) > div.styles__ProfileLinks-sc-__r941b9-8.ikbvPG > div > div:nth-child(2) > button")))
            move_button.click() 
        return True

    def load_all_items(self):
        """
        Scrolls to bottom of store page to load all items
        :return: True if successful
        """
        driver = self.driver
        old_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            sleep(0.5)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == old_height:
                break
            old_height = new_height
        return True

    def get_item_links(self):
        """
        Retrieves reversed list of all non-sold items in store
        :return: reversed href links to each non-sold item
        """
        driver = self.driver
        wait = self.wait
        item_links = []
        with driver:
            item_list = wait.until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#products-tab > div > ul > li > a")))
            
            for item in item_list:
                item.get_attribute("#products-tab > div > ul > li:nth-child(3) > a")
                if item.get_property("textContent") == "Sold":
                    break
                
                """if not driver.find_elements_by_css_selector('#products-tab > div > ul > li:nth-child(60) > a > div > div.styles__SoldOverlay-sc-__sc-13q41bc-10.cfgZOw > h3'):"""
                split_link = item.get_attribute("href").split("/products/")
                edit_link = "https://www.depop.com/products/edit/" + split_link[1]
                item_links.append(edit_link)

            """not_sold_amt = len(item_links) - sold_amt
            print(not_sold_amt)
            item_links = item_links[:not_sold_amt]
            #item_links.reverse()"""
            print(item_links)
            return item_links

    def refresh_items(self, item_links):
        """
        Refreshes all non-sold items
        :param item_links: Reversed list of non-sold items
        :return: True if successful
        """
        driver = self.driver
        wait = self.wait
        for link in item_links:
            driver.get(link)            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(5)
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#main > form > div.styles__Wrapper-sc-__rha4k1-0.bDoeZg > button.sc-ehmTmK.iBXCJM.styles__SaveButton-sc-__rha4k1-1.fMuork")))
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#main > form > div:nth-child(3) > div:nth-child(9) > div")))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            save_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#main > form > div.styles__Wrapper-sc-__rha4k1-0.bDoeZg > button.sc-ehmTmK.iBXCJM.styles__SaveButton-sc-__rha4k1-1.fMuork")))

            while True:
                ActionChains(driver).move_to_element(save_button).click(save_button).perform()
                try:
                    WebDriverWait(self.driver, 3).until(EC.staleness_of(save_button))
                    break
                except TimeoutException:
                    continue
        if self.indefinite:
            print("Successfully refreshed listings.")
            for i in range(int(self.frequency / 10)):
                sleep(10)
                try:
                    driver.find_element_by_id("__next")
                except NoSuchWindowException:
                    break
            self.refresh_items(item_links)
        return True

    def close_driver(self):
        """
        Closes chrome driver
        :return: True if successful
        """
        sleep(5)
        self.driver.close()
        return True

    def accept_cookies(self):
        driver = self.driver
        wait = self.wait
        button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#__next > div.sc-kEYyzF.kzcxAl > div.sc-iAyFgw.JSbHK > button.sc-gZMcBi.sc-gqjmRU.sc-eHgmQL.jDewdN"))) 
        ActionChains(driver).move_to_element(button).click(button).perform()
    
    def check_exists_by_xpath(xpath):
        try:
            driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

if __name__ == "__main__":
    bot = AutoRefresher(indefinite=True, frequency=10)
    bot.login("username", "password")
    bot.move_sold_items_down()
    #bot.accept_cookies()
    bot.load_all_items()
    links = bot.get_item_links()
    bot.refresh_items(links)
    bot.close_driver()
