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
{
  "dataflows": [
    {"id": 1, "name": "Flusso 1", "description": "Descrizione del flusso 1"},
    {"id": 2, "name": "Flusso 2", "description": "Descrizione del flusso 2"}
  ]
}


