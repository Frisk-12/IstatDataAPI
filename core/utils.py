#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 12:35:26 2025

@author: andreadesogus
"""

class StringaFiltroGenerator:
    def __init__(self, tot_filters, applicati):
        self.tot_filters = tot_filters
        self.applicati = applicati
    
    def generate_url_string(self):
        slots = []
        for i in range(self.tot_filters):
            if i in self.applicati.keys():
                # Se il filtro è applicato in questo slot, lo inseriamo prima del punto
                if i == self.tot_filters-1:
                    slots.append(str(self.applicati[i]))
                else:
                    slots.append(str(self.applicati[i]) + ".")
            else:
                # Se non è applicato, manteniamo solo il punto
                slots.append(".")
        return "".join(slots)
