# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 10:12:09 2020

@author: Amber
"""

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Puller():
    def __init__(self):
        self.base_url = "https://www.google.com/search?tbm=isch&q="
        self.driver = Firefox()
    
    def kill(self):
        self.driver.quit()
        
    def search(self, search_term):
        self.driver.get(self.base_url + search_term)
    
    def pull(self, index):
        result = self.driver.find_elements_by_class_name("rg_i")[index]
