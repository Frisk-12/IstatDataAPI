# Descrizione di IstatDataAPI

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
  ],
  "10 - ITTER107": [
    {
      "ID": "IT",
      "Nome_IT": "Italia"
    },
  ]
}
```


### 3. `/api/data` - Recupera Dati Specifici

Questo endpoint consente di recuperare i dati specifici associati a un flusso di dati, utilizzando i parametri `dataflow_id`, `ref_id` e un insieme opzionale di filtri. I dati vengono restituiti come un array di record in formato JSON. Questo endpoint è utile per ottenere informazioni dettagliate, applicando filtri per affinare la selezione dei dati.

**Metodo:** `POST`  
**Parametri nel corpo della richiesta:**
- `dataflow_id` (obbligatorio): ID del flusso di dati per cui recuperare i dati
- `ref_id` (obbligatorio): ID di riferimento per ottenere i dati specifici
- `filters` (opzionale): un dizionario di filtri per affinare la selezione dei dati. Ogni filtro è una coppia chiave-valore.

**Risposta:**
Restituisce i dati specifici del flusso richiesto, in formato JSON, come un array di record. Ogni record è rappresentato come un dizionario con le colonne del flusso di dati come chiavi e i relativi valori come valori.

#### Esempio di richiesta:
```json
POST /api/data
{
  "dataflow_id": 1,
  "ref_id": 10,
  "filters": {
    "filter1": "valore1",
    "filter2": "valore2"
  }
}
```

#### Esempio di Risposta
[  
  {
    "ATTCONNESSE": "ALL",
    "CATEG_MANODOPERA": "THLF",
    "CLASSE_SUP": "TOT",
    "CONDUZ": "TOT",
    "FORMGIUR": "TOT",
    "FREQ": "A",
    "ITTER107": "ITG2",
    "ObsValue": "18275",
    "PROVENIENZA_MANOD": "WORLD",
    "TIME_PERIOD": "2013",
    "TIPCOLTIV": "ALL",
    "TIPI_MEZZIMEC": "ALL",
    "TIPO_ALLEVAMENTO": "ALL",
    "TIPO_DATO": "HO_MECH",
    "TIPO_ENERGRINN": "ALL",
    "TITOLO_STUDIO_CAPO_AZ": "99",
    "TIT_POSSES": "ALL",
    "TIT_POSSESUSO_MEZZIMEC": "THIRD_FARM"
  },
  
]
