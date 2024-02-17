#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 17:04:19 2023

@author: javiera.quiroz
"""


import pandas as pd
import fnmatch
from ftplib import FTP
import re
import os

from .download_tsv import Download_tsv
from .download_json import Download_json
from .download_obo import Download_obo
from .download_fb import Download_fb
from .download_fasta import Download_fasta

from FlyBaseDownloads.utilities.database import RTD


class Downloads(Download_tsv, Download_json,
                Download_obo, Download_fb,
                Download_fasta):
    def __init__(self, url, cred, continue_):
        
        self.url = url
        self.cred = cred
        self.continue_ = continue_
        
    def download_file(self):
        #current_script_path = os.path.dirname(os.path.realpath(__file__))
        
        url = self.url
        file = url.split('/')[-1]
        file = file.split('*')[0]
        
        archivos_encontrados = os.listdir("../")
        for archivo in archivos_encontrados:
            if archivo.startswith(file):
                archivo_path = os.path.join("..", archivo)
                return archivo_path
        
        if self.continue_ and self.cred is not None:
            ftp = FTP(url.split('/')[2])
            ftp.login()
            directory_path = '/'.join(url.split('/')[3:-1])
            
            ftp.cwd(directory_path)
            
            remote_files = ftp.nlst()
            
            filtered_files = list(fnmatch.filter(remote_files, url.split('/')[-1]))
            
            files = []
            for file in filtered_files:
                file_path = '../' + file
                if not os.path.exists(file):
                    with open(file_path, 'wb') as local_file:
                        ftp.retrbinary('RETR ' + file, local_file.write)
            
                    files.append(file)
                else:
                    files.append(file)
            
            ftp.quit()
            if len(files) > 0:
                file = files[0]
                rtd = RTD(self.cred)
                rtd.save_reg(file)
                archivo_path = os.path.join("..", file)
                return archivo_path
            
        elif not self.continue_:
            print('The file is not in your enviroment')
        elif self.cred is None and self.continue_:
            print('Failed to download the file')
            return None
    
    def get(self, header = None):
        
        file = None
        
        try:
            file = self.download_file()
        except:
            print("This may be due to a lack of internet connection or due to an email form failure")
        patron = r"##?\s?\w+"
        
        def df_r(df):
            if re.search(r"FB\w{9}", df.columns[0]): 
                df_columns = pd.DataFrame(df.columns).T

                df.columns = range(len(df.columns))
                
               
                df = pd.concat([df_columns, df], ignore_index=True, axis = 0)
            
            if re.search(patron, df.iloc[-1,0]):
                df = df.iloc[:-1, :]
            
            return df
        
        
        if file is not None:
            if re.search('.obo', self.url):
                return Download_obo.open_obo(self,file)
            elif re.search('.json', self.url):
                try:
                    return df_r(Download_json.open_file_json(self, file))
                    
                except:
                    try:
                        df = Download_json.open_file_json(self, file)
                        df = pd.concat([df.drop(['driver'], axis=1), df['driver'].apply(pd.Series)], axis=1)

                        df = df.replace({None: pd.NA})
                        return df_r(df)
                    except:
                        return Download_json.open_file_json(self,file)
                    
            elif re.search('.fasta', self.url):
                return Download_fasta.open_fasta(self, file)
            else:
                return df_r(Download_tsv.open_file_tsv(self, file, header))
        return file
    
