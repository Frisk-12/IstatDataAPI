#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 12:35:26 2025

@author: andreadesogus
"""

class StringaFiltroGenerator:
    def __init__(self, tot_filters, applicati):
        self.tot_filters = tot_filters
        self.applicati = self.convert_keys_to_int(applicati)

    def convert_keys_to_int(self, input_dict):
        """Converts dictionary keys from strings to integers where possible."""
        output_dict = {}
        for key, value in input_dict.items():
            try:
                output_dict[int(key)] = value
            except ValueError:
                print(f"KEY '{key}' NOT TRASFORMED IN INTEGER")
                output_dict[key] = value  # Keep original key if conversion fails
        return output_dict
    
    def generate_url_string(self):
        slots = []
        if not bool(self.applicati):
            return "." * (self.tot_filters - 1)
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
        print(f"SUBSTRING RETURNED: {''.join(slots)}\nN. FILTERS: {self.tot_filters}\nFILTERS: {self.applicati}")
        return "".join(slots)

import pandas as pd

class PatternMatcher:
    """
    Classe generica per verificare se almeno una riga di un DataFrame soddisfa un pattern.

    Il pattern è una stringa in cui i campi sono separati da un delimitatore (default: '.').
    Ogni campo corrisponde a una colonna, secondo l'ordine definito dalla lista `columns`.
    Se un campo è vuoto (cioè, non c'è nessun carattere tra due delimitatori), viene interpretato
    come wildcard, e il valore nella colonna corrispondente non viene controllato.

    Parametri:
      - df: il DataFrame su cui effettuare la verifica.
      - columns: (opzionale) lista delle colonne da utilizzare per il confronto.
                 Se non specificata, viene usato l'ordine delle colonne del DataFrame.
      - delimiter: (opzionale) il carattere usato per separare i campi nel pattern (default: '.').
    """
    
    def __init__(self, df, columns=None, delimiter='.'):
        self.df = df
        self.columns = columns if columns is not None else list(df.columns)
        self.delimiter = delimiter
        
    def match(self, pattern):
        """
        Verifica se esiste almeno una riga nel DataFrame che corrisponde al pattern.

        Il pattern deve contenere un numero di campi uguale al numero di colonne specificate
        (o al numero di colonne del DataFrame se `columns` non è definito). Se il pattern contiene
        meno campi, quelli mancanti sono considerati wildcard; se ne contiene di più, viene sollevato
        un errore.

        Esempi:
          - pattern = "M..EXT_EU..TBV" -> Verifica la prima colonna uguale a "M", la terza a "EXT_EU",
            la quinta a "TBV", mentre la seconda e la quarta sono wildcard.
          - pattern = "M.0010..ITTOT." -> Verifica la prima colonna uguale a "M", la seconda a "0010",
            la quarta a "ITTOT"; la terza e la quinta sono wildcard.

        :param pattern: stringa contenente il pattern.
        :return: True se almeno una riga soddisfa il pattern, altrimenti False.
        """
        parts = pattern.split(self.delimiter)
        
        # Se il numero di parti è minore delle colonne, estende con wildcard (stringa vuota)
        if len(parts) < len(self.columns):
            parts.extend([""] * (len(self.columns) - len(parts)))
        # Se il numero di parti è maggiore delle colonne, solleva un errore
        elif len(parts) > len(self.columns):
            print(f"COLONNE: {self.columns}")
            print(f"PATTERN: {pattern}")
            print(f"N. COLONNE: {len(self.columns)} VS N. PARTS: {len(parts)}")
            raise ValueError("Il pattern contiene più elementi rispetto alle colonne specificate.")
        
        # Inizializzo una maschera con True per tutte le righe
        mask = pd.Series(True, index=self.df.index)
        # Applico il confronto per ogni colonna (salto se il campo è vuoto)
        for col, pat in zip(self.columns, parts):
            if pat != "":
                mask &= (self.df[col] == pat)
        
        return mask.any()
