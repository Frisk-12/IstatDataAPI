#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 12:45:39 2025

@author: andreadesogus
"""

import pandas as pd
from typing import Any, Dict, List, Optional, Tuple

from core.downloader import Downloader
from core.parsers import (
    DataflowParser,
    SeriesParser,
    DataSchemeExtractor,
    MetadataHelper,
    ValuesParser
)
from core.utils import StringaFiltroGenerator


class DataflowRetriever:
    """Classe per il recupero e l'analisi dei dataflow da SDMX."""

    def _download_dataflow(self) -> str:
        """Scarica i dati del dataflow."""
        downloader = Downloader("https://sdmx.istat.it/SDMXWS/rest/dataflow/IT1/")
        return downloader.download()

    def parse_dataflows(self, search_string: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Analizza i dataflow e ritorna una lista di dizionari.

        Se search_string è fornita, filtra i dataflow in base al nome.
        In caso di filtro senza risultati, viene mostrato un messaggio e vengono restituiti tutti i dataflow.
        """
        xml_data = self._download_dataflow()
        dataflow_parser = DataflowParser(xml_data)
        df_dataflows = (
            dataflow_parser
            .parse_dataflows()
            .sort_values(by="Nome IT")
            .reset_index(drop=True)
            .dropna()
        )
        if not search_string:
            return df_dataflows.to_dict(orient="records")
        else:
            df_filtered = dataflow_parser.filter_by_name(df_dataflows, search_string)
            if df_filtered.empty:
                print("La stringa inserita non ha prodotto risultati. Recupero tutti i dataflow.")
                return df_dataflows.to_dict(orient="records")
            return df_filtered.to_dict(orient="records")


class FiltersRetriever:
    """
    Classe per il recupero e la gestione dei filtri basati su un dataflow e una struttura dati.
    """

    def __init__(self, dataflow_id: str, ref_id: str) -> None:
        self.dataflow_id = dataflow_id
        self.ref_id = ref_id
        # Recupera e memorizza il dataframe della serie; si assume che parse_series ritorni una tupla
        _, _, self.df_series = self._parse_series()

    def _download_series(self) -> str:
        """Scarica i dati della serie per il dataflow specificato."""
        downloader = Downloader(f"http://sdmx.istat.it/SDMXWS/rest/data/{self.dataflow_id}")
        return downloader.download()

    def _download_filter_structure(self) -> str:
        """Scarica la struttura dei filtri per il riferimento specificato."""
        downloader = Downloader(f"https://sdmx.istat.it/SDMXWS/rest/datastructure/IT1/{self.ref_id}/")
        return downloader.download()

    def _download_codelist(self, codelist_id: str) -> str:
        """Scarica la codelist per il filtro specificato."""
        downloader = Downloader(f"http://sdmx.istat.it/SDMXWS/rest/codelist/IT1/{codelist_id}")
        return downloader.download()

    def _parse_series(self) -> Tuple[Any, Any, pd.DataFrame]:
        """
        Analizza i dati della serie e ritorna il risultato del parsing.
        Il risultato atteso è una tupla in cui il terzo elemento è il dataframe.
        """
        xml_data = self._download_series()
        series_parser = SeriesParser(xml_data)
        return series_parser.parse_series()

    def get_filters(self) -> pd.Index:
        """Ritorna le colonne (filtri) presenti nel dataframe della serie."""
        return self.df_series.columns

    def get_valid_filters(self) -> List[str]:
        """
        Ritorna una lista dei filtri (colonne) che contengono più di un valore unico,
        considerati validi.
        """
        return [col for col in self.df_series if self.df_series[col].nunique() > 1]

    def _parse_filter_structure(self) -> pd.DataFrame:
        """
        Analizza la struttura dei filtri e ritorna un DataFrame ordinato in base all'ID della dimensione.
        """
        xml_data = self._download_filter_structure()
        filter_parser = DataSchemeExtractor(xml_data)
        df_dimensions = filter_parser.parse_dimensions()
        # Imposta l'ordinamento basato sui filtri disponibili
        df_dimensions['Dimension ID'] = pd.Categorical(
            df_dimensions['Dimension ID'],
            categories=list(self.get_filters()),
            ordered=True
        )
        df_dimensions = df_dimensions.sort_values('Dimension ID').reset_index(drop=True)
        return df_dimensions

    def _get_filtered_dimensions(self) -> pd.DataFrame:
        """
        Recupera la struttura dei filtri filtrata per i valid filters.
        Restituisce un DataFrame contenente le colonne 'Dimension ID' e 'Codelist ID'.
        """
        valid_filters = self.get_valid_filters()
        df_filters = self._parse_filter_structure()
        return df_filters.loc[
            df_filters['Dimension ID'].isin(valid_filters),
            ['Dimension ID', 'Codelist ID']
        ]

    def get_filters_dictionary(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Costruisce e ritorna un dizionario contenente i filtri validi e le relative codelist.
    
        La chiave del dizionario è una stringa formata dall'indice della riga e dall'ID del filtro,
        mentre il valore è una lista di dizionari con i codici e i nomi corrispondenti.
        """
        df_filters = self._get_filtered_dimensions()
        filters_dict: Dict[str, List[Dict[str, Any]]] = {}
    
        for idx, row in df_filters.iterrows():
            filter_id = row['Dimension ID']
            codelist_id = row['Codelist ID']
            unique_values = self.df_series[filter_id].unique()
    
            xml_data = self._download_codelist(codelist_id)
            codelist_parser = MetadataHelper(xml_data)
            df_codelist = codelist_parser.get_codes()
            df_codelist = df_codelist[df_codelist['ID'].isin(unique_values)][['ID', "Nome_IT"]]
    
            filters_dict[f"{idx} - {filter_id}"] = df_codelist.to_dict(orient="records")
    
        # Ordina il dizionario per chiave
        filters_dict = {k: filters_dict[k] for k in sorted(filters_dict)}
        return filters_dict

    def generate_filter_url(self, filters: Dict[int, str]) -> str:
        """
        Genera e ritorna una stringa URL basata sui filtri forniti.

        Args:
            filters: Un dizionario dove la chiave è l'indice del filtro e il valore è il filtro selezionato.

        Returns:
            Una stringa contenente l'URL generato.
        """
        tot_filters = len(self.get_filters())
        generator = StringaFiltroGenerator(tot_filters, filters)
        return generator.generate_url_string()
    
    
class DataRetriever:
    def __init__(self, dataflow_id: str, ref_id: str, filters: Dict[int, str]) -> None:
        self.dataflow_id = dataflow_id
        self.ref_id = ref_id
        self.filters = filters
        self.fr = FiltersRetriever(self.dataflow_id, self.ref_id)
        
    def generate_filter_string(self) -> str:
        return self.fr.generate_filter_url(self.filters)
        
    def get_data(self) -> pd.DataFrame:
        """
        Fornisce il dataset finale con i valori osservati con i filtri prescelti.

        Args:
            filters: Un dizionario dove la chiave è l'indice del filtro e il valore è il filtro selezionato.
            
        Returns:
            Un Pandas Dataframe.
        """
        
        string = self.generate_filter_string()
        print(f"Filtered subURL string: {string}")
        url_data = f"https://sdmx.istat.it/SDMXWS/rest/data/{self.dataflow_id}/{string}"
        downloader_data = Downloader(url_data)
        xml_data = downloader_data.download()
            
        data_parser = ValuesParser(xml_data)
        return data_parser.parse()
    
    
