#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 12:34:03 2025

@author: andreadesogus
"""

import xml.etree.ElementTree as ET
import pandas as pd

class DataflowParser:
    """
    Classe per il parsing dei dataflow da XML.
    """
    def __init__(self, xml_text: str):
        self.root = ET.fromstring(xml_text)
        self.namespaces = {
            "structure": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
            "common": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"
        }
    
    def parse_dataflows(self) -> pd.DataFrame:
        dataflows = []
        for dataflow in self.root.findall(".//structure:Dataflow", self.namespaces):
            dataflow_id = dataflow.get("id")
            name_it = next((n.text for n in dataflow.findall("common:Name", self.namespaces) 
                           if n.get("{http://www.w3.org/XML/1998/namespace}lang") == "it"), None)
            name_en = next((n.text for n in dataflow.findall("common:Name", self.namespaces) 
                           if n.get("{http://www.w3.org/XML/1998/namespace}lang") == "en"), None)
            ref_element = dataflow.find(".//structure:Structure/Ref", self.namespaces)
            ref_id = ref_element.get("id") if ref_element is not None else None
            
            dataflows.append({
                "Dataflow ID": dataflow_id,
                "Nome IT": name_it,
                "Nome EN": name_en,
                "Ref ID": ref_id
            })
        return pd.DataFrame(dataflows)
    
    def filter_by_name(self, df: pd.DataFrame, substring: str) -> pd.DataFrame:
        return df[df['Nome IT'].str.contains(substring, na=False)]

class SeriesParser:
    """
    Classe per il parsing delle serie (SeriesKey) da XML.
    """
    def __init__(self, xml_text: str):
        self.root = ET.fromstring(xml_text)
        self.namespaces = {
            "message": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
            "common": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common",
            "generic": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic"
        }
    
    def parse_series(self) -> (str, str, pd.DataFrame):
        # Estrae lo structureID e il Ref ID
        structure_element = self.root.find(".//message:Structure", self.namespaces)
        structure_id = structure_element.get("structureID") if structure_element is not None else None
        
        ref_element = self.root.find(".//common:Structure/Ref", self.namespaces)
        ref_id = ref_element.get("id") if ref_element is not None else None
        
        # Estrae le chiavi delle serie
        series_keys = []
        for series in self.root.findall(".//generic:Series", self.namespaces):
            series_key = series.find("generic:SeriesKey", self.namespaces)
            if series_key is not None:
                keys = {value.get("id"): value.get("value") for value in series_key.findall("generic:Value", self.namespaces)}
                series_keys.append(keys)
        df_series = pd.DataFrame(series_keys)
        return structure_id, ref_id, df_series

class DataSchemeExtractor:
    """
    Classe per il parsing delle dimensioni dal XML.
    """
    def __init__(self, xml_text: str):
        self.root = ET.fromstring(xml_text)
        self.namespaces = {
            "structure": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure"
        }
    
    def parse_dimensions(self) -> pd.DataFrame:
        dimensions_data = []
        for dimension in self.root.findall(".//structure:Dimension", self.namespaces):
            dim_id = dimension.get("id")
            urn = dimension.get("urn")
            position = dimension.get("position")
            
            # Parsing del ConceptIdentity
            concept_identity = dimension.find("structure:ConceptIdentity", self.namespaces)
            if concept_identity is not None:
                concept_ref = concept_identity.find("structure:Ref", self.namespaces)
                if concept_ref is None:
                    concept_ref = concept_identity.find("Ref")
                concept_id = concept_ref.get("id") if concept_ref is not None else "NOT FOUND"
            else:
                concept_id = "NOT FOUND"
            
            # Parsing del codelist_id
            local_enum = dimension.find("structure:LocalRepresentation/structure:Enumeration", self.namespaces)
            if local_enum is not None:
                codelist_ref = local_enum.find("structure:Ref", self.namespaces)
                if codelist_ref is None:
                    codelist_ref = local_enum.find("Ref")
                codelist_id = codelist_ref.get("id") if codelist_ref is not None else "NOT FOUND"
            else:
                codelist_id = "NOT FOUND"
            
            dimensions_data.append({
                "Dimension ID": dim_id,
                "URN": urn,
                "Position": position,
                "Concept ID": concept_id,
                "Codelist ID": codelist_id
            })
        return pd.DataFrame(dimensions_data)

class MetadataHelper:
    def __init__(self, xml_text):
        self.root = ET.fromstring(xml_text)
        self.namespaces = {
            "message": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
            "structure": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
            "common": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common",
            "xml": "http://www.w3.org/XML/1998/namespace"
        }
    
    def get_codes(self):
        data = []
        codes = self.root.findall(".//structure:Code", self.namespaces)
        
        for code in codes:
            code_id = code.get("id")
            name_it = self._get_element_text(code, "common:Name[@xml:lang='it']")
            name_en = self._get_element_text(code, "common:Name[@xml:lang='en']")
            
            data.append({"ID": code_id, "Nome_IT": name_it, "Nome_EN": name_en})
        
        return pd.DataFrame(data)
    
    def _get_element_text(self, parent, xpath):
        element = parent.find(xpath, self.namespaces)
        return element.text if element is not None else None



class ValuesParser:
    
    """
    Classe per il parsing di un XML SDMX e la creazione di un DataFrame Pandas.
    """
    
    def __init__(self, xml_text, namespaces=None):
        """
        Inizializza il parser con il testo XML e i namespace da utilizzare.
        
        :param xml_text: Stringa contenente il documento XML.
        :param namespaces: Dizionario dei namespace. Se non fornito, vengono usati quelli di default.
        """
        self.xml_text = xml_text
        self.namespaces = namespaces or {
            'message': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message',
            'generic': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic',
            'common': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common'
        }
        self.root = ET.fromstring(self.xml_text)

    def _extract_series_key(self, series):
        """
        Estrae la SeriesKey da un elemento Series.
        
        :param series: Elemento XML della Series.
        :return: Dizionario contenente la SeriesKey oppure None se non presente.
        """
        series_key = {}
        series_key_el = series.find("generic:SeriesKey", self.namespaces)
        if series_key_el is None:
            return None
        for val in series_key_el.findall("generic:Value", self.namespaces):
            series_key[val.attrib['id']] = val.attrib['value']
        return series_key

    def _extract_obs_data(self, series_key, obs):
        """
        Estrae i dati di un'osservazione e li combina con la SeriesKey.
        
        :param series_key: Dizionario contenente la SeriesKey.
        :param obs: Elemento XML dell'osservazione.
        :return: Dizionario con i dati combinati.
        """
        # Inizializza la riga con i dati della SeriesKey
        row = series_key.copy() if series_key else {}
        
        # Estrai la dimensione temporale (ad es. TIME_PERIOD)
        time_dim = obs.find("generic:ObsDimension", self.namespaces)
        if time_dim is not None:
            row[time_dim.attrib['id']] = time_dim.attrib['value']
        
        # Estrai il valore osservato
        obs_value = obs.find("generic:ObsValue", self.namespaces)
        row['ObsValue'] = obs_value.attrib.get('value') if obs_value is not None else None
        
        return row

    def parse(self):
        """
        Esegue il parsing dell'XML e restituisce un DataFrame con i dati estratti.
        
        :return: DataFrame Pandas contenente tutte le osservazioni.
        """
        rows = []
        for series in self.root.findall(".//generic:Series", self.namespaces):
            series_key = self._extract_series_key(series)
            if series_key is None:
                continue  # Salta le series senza SeriesKey
            for obs in series.findall("generic:Obs", self.namespaces):
                row = self._extract_obs_data(series_key, obs)
                rows.append(row)
        return pd.DataFrame(rows)