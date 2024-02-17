#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 14:19:10 2024

@author: javicolors
"""

"""

Unofficial wrapper of FlyBase Database

"""
from .classes.Synonyms import Synonyms
from .classes.Genes import Genes
from .classes.Gene_Ontology_annotation import Gene_Ontology_annotation
from .classes.Gene_groups import Gene_groups
from .classes.Homologs import Homologs
from .classes.Ontology_Terms import Ontology_Terms
from .classes.Organisms import Organisms
from .classes.Insertions import Insertions
from .classes.Clones import Clones
from .classes.References import References
from .classes.Alleles_Stocks import Alleles_Stocks
from .classes.Human_disease import Human_disease
from .classes.Annotation_Sequence import AnnSeq

from .utilities.authentication import Authentication
from .utilities.database import RTD
from .utilities.internet import Check_internet

#%%

class FBD():
    
    def __name__(self):
        self.__name__ = 'FlyBase Downloads'
    
    def __init__(self, email, internet = True, msg = False):
        
        self.email = email
        
        if internet:
            internet = Check_internet.check_internet_connection(msg=False)
        
        if internet:    
            auth = Authentication(internet, msg=msg)
            credential_key = auth.get_user(self.email, msg)
            self.rtd = RTD(credential_key)
        else:
            Check_internet.check_internet_connection()
            credential_key = False
        
        
        main_url = 'ftp://ftp.flybase.net/releases/current/precomputed_files/'
        
        self.Synonyms = Synonyms(main_url, credential_key)
        self.Genes = Genes(main_url, credential_key)
        self.GOAnn = Gene_Ontology_annotation(main_url, credential_key) 
        self.Gene_groups = Gene_groups(main_url, credential_key)
        self.Homologs = Homologs(main_url, credential_key)
        self.Ontology_Terms = Ontology_Terms(main_url, credential_key)
        self.Organisms = Organisms(main_url, credential_key)
        self.Insertions = Insertions(main_url, credential_key)
        self.Clones = Clones(main_url, credential_key)
        self.References = References(main_url, credential_key)
        self.Alleles_Stocks = Alleles_Stocks(main_url, credential_key)
        self.Human_disease = Human_disease(main_url, credential_key)
        
        fasta_url = "ftp://ftp.flybase.net/releases/current/dmel_r6.55/fasta"
        self.AnnSeq = AnnSeq(fasta_url, credential_key)
            
        

    def close_app(self):
        try:
            self.rtd.def_reg()
        except:
            pass
        

        
    