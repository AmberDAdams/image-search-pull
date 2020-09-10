# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 10:12:09 2020

@author: Amber
"""

import requests
import logging
import sys
from selenium.webdriver import Firefox

class Puller():
    def __init__(self, log_level):
        self.base_url = "https://www.google.com/search?tbm=isch&q="
        self.driver = Firefox()
        
    
    def kill(self):
        self.driver.quit()
        
    def search(self, search_term):
        self.driver.get(self.base_url + search_term)
    
    def pull(self, index):
        result = self.driver.find_elements_by_class_name("rg_i")[index]
        self.image = requests.get(result.get_attribute("src"))
        
    def save_pulled(self, save_path):
        with file as open(save_path, "wb"):
            file.write(response.content)
