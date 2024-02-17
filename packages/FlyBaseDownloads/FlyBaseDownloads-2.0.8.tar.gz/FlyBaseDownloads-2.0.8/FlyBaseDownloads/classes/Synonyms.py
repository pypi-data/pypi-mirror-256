#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 17:04:57 2023

@author: usuario
"""

from FlyBaseDownloads.downloads.Downloads import Downloads 
from FlyBaseDownloads.utilities.internet import Check_internet

class Synonyms():
    
    def __init__(self, main_url, cred):
        self.cred = cred
        self.main_url = main_url
        self.syn_url = 'synonyms/fb_synonym_*.tsv.gz'
        self.header = 3
        
    
    def get(self):
        
        url = self.main_url + self.syn_url
        if not self.cred:
            connection_ = False
        else:
            connection_ =  Check_internet.check_internet_connection(msg=False)
        downloads = Downloads(url, self.cred, connection_)
        
        return downloads.get(self.header)
