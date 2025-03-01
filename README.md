# Descrizione dell'API Flask

Questa applicazione Python, costruita con Flask, espone un'API che consente di recuperare informazioni relative a flussi di dati, filtri e dati specifici. È progettata per interagire con sistemi che gestiscono dati complessi e offre una serie di endpoint per eseguire operazioni di estrazione e filtraggio dei dati. L'API è costruita in modo da essere facilmente estendibile e utilizzabile in contesti di analisi e gestione dei dati.

## Funzionalità Principali

L'API mette a disposizione tre endpoint principali:

### 1. `/api/dataflow` - Recupera i Flussi di Dati
Questo endpoint consente di ottenere i flussi di dati disponibili nel sistema. La chiamata accetta un parametro opzionale `string`, che può essere utilizzato per filtrare i dati dei flussi di dati. Se il parametro non viene fornito, verranno restituiti tutti i flussi di dati disponibili.

**Metodo:** `GET`  
**Parametri (opzionali):**
- `string`: stringa per filtrare i flussi di dati

**Risposta:**
Restituisce una lista di flussi di dati in formato JSON.

#### Esempi di richiesta:
- GET /api/dataflow
- GET /api/dataflow?string=agri


#### Esempio di risposta:
```json
[
  {
    "Dataflow ID": "93_48",
    "Nome EN": "Agriculture, forestry and fishing accounts",
    "Nome IT": "Conti della branca agricoltura, silvicoltura e pesca",
    "Ref ID": "DCCN_VAAGSIPET"
  },
  {
    "Dataflow ID": "750_1118",
    "Nome EN": "Agriculture, forestry and fishing accounts in the 2011 version",
    "Nome IT": "Conti della branca agricoltura, silvicoltura e pesca - versione 2011",
    "Ref ID": "DCCN_VAAGSIPET_B11"
  },
  ...
  ]
```



### 2. `/api/filters` - Recupera i Filtri per un Dataflow Specifico

Questo endpoint consente di ottenere i filtri associati a un determinato flusso di dati. Per utilizzare questo endpoint, è necessario fornire i parametri `dataflow_id` e `ref_id`. I filtri restituiti possono essere utilizzati per affinare la selezione dei dati in base a criteri specifici.

**Metodo:** `GET`  
**Parametri:**
- `dataflow_id` (obbligatorio): ID del flusso di dati di cui recuperare i filtri
- `ref_id` (obbligatorio): ID di riferimento per ottenere i filtri specifici per il flusso

**Risposta:**
Restituisce un dizionario di filtri applicabili al flusso di dati richiesto.

#### Esempio di richiesta:
GET /api/filters?dataflow_id=102_974&ref_id=DCSP_SPA


#### Esempio di risposta:
```json
{
  "1 - TITOLO_STUDIO_CAPO_AZ": [
    {
      "ID": "99",
      "Nome_IT": "totale"
    },
  ...
  ],

  "10 - ITTER107": [
    {
      "ID": "IT",
      "Nome_IT": "Italia"
    },
  ]
}
```
