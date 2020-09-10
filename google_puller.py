# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 10:12:09 2020

@author: Amber
"""

import requests
import logging
import sys
from datetime import datetime
from urllib.parse import unquote
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions

logging_levels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warn": logging.WARN,
        "error": logging.ERROR,
        "critical": logging.CRITICAL}
LOG_FORMAT = '%(asctime)-15s %(name)-12s %(levelname)-8s %(message).100s'
LOG_STREAM = sys.stdout

class Puller():
    def __init__(self, log_level="info"):
        self.base_url = "https://www.google.com/search?tbm=isch&q="
        self.driver = Firefox()
        LOG_NAME = "Puller Instance " + datetime.now().isoformat()
        LOG_LEVEL_DEFAULT = logging_levels[log_level.lower()]
        logging.basicConfig(stream=LOG_STREAM, level=LOG_LEVEL_DEFAULT, 
                                format=LOG_FORMAT)
        self.logger = logging.getLogger(LOG_NAME)
    
    def kill(self):
        self.driver.quit()
        
    def search(self, search_term):
        self.driver.get(self.base_url + search_term)
    
    def pull(self, index):
        result = self.driver.find_elements_by_class_name("isv-r")[index]
        result = result.find_element_by_class_name("wXeWr")
        # this only works if I "inspect element" on the proper image beforehand
        # looking into using action chains / action builder to use context menu
        url = result.get_attribute("href").replace("/imgres?imgurl=", "")
        url = unquote(url.replace("https://www.google.com", ""))
        self.image = requests.get(url).content
        
    def get_index_by_size(self, min_width=None, min_height=None,
                          max_width=None, max_height=None):
        results = self.driver.find_elements_by_class_name("isv-r")
        cur_index = 0
        satisfied = False
        while satisfied == False:
            img = results[cur_index]
            img_width = int(img.get_attribute("data-ow"))
            img_height = int(img.get_attribute("data-oh"))
            # using info level for now because debug level is saturated
            # debug level is used for many of the modules used here
            self.logger.info("Image Index #%s wxh %sx%s",
                        cur_index, img_width, img_height)
            if min_width is not None and img_width < min_width:
                self.logger.info("img width too small")
                cur_index += 1
            elif max_width is not None and img_width > max_width:
                self.logger.info("img width too large")
                cur_index += 1
            elif min_height is not None and img_height < min_height:
                self.logger.info("img height too small")
                cur_index += 1
            elif max_height is not None and img_height > min_height:
                self.logger.info("img height too large")
                cur_index += 1
            else:
                satisfied = True
        return cur_index
        
    def save_pulled(self, save_path):
        with open(save_path, "wb") as file:
            file.write(self.image)
