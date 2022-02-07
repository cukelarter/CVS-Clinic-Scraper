# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 20:58:49 2022

@author: Luke
"""

import scrapy
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging

class CVSClinicSpider(scrapy.Spider):
    name='cvsclinic_sc'
    def __init__(self,):
        baseurl='https://www.cvs.com/minuteclinic/clinic-locator/clinic-directory/'
        statecodes=[code.lower()+'/' for code in pd.read_csv(r'C:\Users\cukel\OneDrive\Documents\upwork\cvsclinic\stateData.csv')['Code']]
        urls=[f'{baseurl}{sc}' for sc in statecodes]
        self.start_urls=urls 
    
    def parse(self, response):
        page = response.url
        soup=BeautifulSoup(response.text,'lxml')
        # get what we want
        locpages=[]
        for ana in soup.findAll('a'):
            try:
                ahref=ana['href']
                if len(ana)!=len(page) and ahref[0:len(page)]==page:
                    yield {
                        'locpage':ana['href']
                        }
            except:
                logging.warning('Failed on {}'.format(ana))