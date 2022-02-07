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
    name='cvsclinic'
    def __init__(self,):
        baseurl='https://www.cvs.com/minuteclinic/clinic-locator/clinic-directory/'
        #statecodes=[code.lower()+'/' for code in pd.read_csv(r'C:\Users\cukel\OneDrive\Documents\upwork\cvsclinic\stateData.csv')['Code']]
       # urls=[f'{baseurl}{sc}' for sc in statecodes]
        self.start_urls=[baseurl]
    
    def parse(self, response):
        page = response.url
        soup=BeautifulSoup(response.text,'lxml')
        # get what we want
        locpages=[]
        for ana in soup.findAll('a'):
            try:
                ahref=ana['href']
                next_page=None
                if len(ahref)>len(page) and ahref[0:len(page)]==page and ana.parent.name=='li':
                    #yield {
                    #    'statepage':ahref
                    #    }
                    next_page=ahref
                if next_page is not None:
                    yield response.follow(next_page, callback=self.parse_state)
            except KeyError:
                pass
                #logging.warning('Failed on {}'.format(ana))
    def parse_state(self,response):
        page = response.url
        soup=BeautifulSoup(response.text,'lxml')
        # get what we want
        locpages=[]
        for ana in soup.findAll('a'):
            try:
                ahref=ana['href']
                next_page=None
                if len(ahref)>len(page) and ahref[0:len(page)]==page and ana.parent.name=='li':
                    #yield {
                    #    'clinicpage':ahref
                    #    }
                    next_page=ahref
                if next_page is not None:
                    yield response.follow(next_page, callback=self.parse_clinic)
            except KeyError:
                pass
                #logging.warning('Failed on {}'.format(ana))

    def parse_clinic(self,response):
        # parses clinic data
        page=response.url
        soup=BeautifulSoup(response.text,'lxml')
        for loc in soup.findAll('h2', {'class':'browse-locations-header jump-regions is-single-location'}):
            servicelist=loc.findNext('ul')
            services=[ana.text for ana in servicelist.findAll('a')]
            yield{
                'location':loc.text[0:len(loc.text)-10], #removes 'view clinic '
                'services':services
                }