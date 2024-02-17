#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 17:34:10 2023

@author: usuario
"""

from FlyBaseDownloads.downloads.Downloads import Downloads 
from FlyBaseDownloads.utilities.internet import Check_internet

class Clones():
    
    def __init__(self, main_url, cred):
        self.cred = cred
        self.main_url = main_url
        self.cl_url = 'clones/'
        self.header = None
        
    def cDNA_clone_data(self):
        self.un_url = 'cDNA_clone_data_fb_*.tsv.gz'
        self.header = 3
        return self.get()
    
    def genomic_clone_data(self):
        self.un_url = 'genomic_clone_data_fb_*.tsv.gz'
        self.header = 3
        return self.get()
    
    
    def get(self):    
        url = self.main_url + self.cl_url + self.un_url
        
        if not self.cred:
            connection_ = False
        else:
            connection_ =  Check_internet.check_internet_connection(msg=False)
        downloads = Downloads(url, self.cred, connection_)
        
        return downloads.get(self.header)
    
