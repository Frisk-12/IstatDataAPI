#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 12:32:39 2025

@author: andreadesogus
"""

import requests

class Downloader:
    """
    Classe per scaricare dati da un URL.
    """
    def __init__(self, url: str):
        self.url = url
    
    def download(self) -> str:
        response = requests.get(self.url)
        if response.status_code == 200:
            print(f"Download completed successfully from {self.url}")
            return response.text
        else:
            raise Exception(f"Request error in {self.url}: {response.status_code}")
