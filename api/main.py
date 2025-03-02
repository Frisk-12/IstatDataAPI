#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 13:09:44 2025

@author: andreadesogus
"""

import os
#import time
#import logging

from flask import Flask, request, jsonify
from flask_cors import CORS

from services.dataflow_service import DataflowRetriever, FiltersRetriever, DataRetriever

app = Flask(__name__)
CORS(app)

#logging.basicConfig(level=logging.INFO)

@app.route("/")
def get_dataflows():
    return "Benvenuto nell'app Flask!"

@app.route("/api/dataflow", methods=["GET"])
def get_index_data():
    try: 
        string = request.args.get("string")
        dfr = DataflowRetriever()        
        if not string:
            res = dfr.parse_dataflows()
        else:
            res = dfr.parse_dataflows(string)
        return jsonify(res)

    except ValueError as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/filters", methods=["GET"])
def get_filter_dict():
    try: 
        #logging.info("API /api/filters called")
        dataflow_id = request.args.get("dataflow_id")
        ref_id = request.args.get("ref_id")
        
        if not dataflow_id or not ref_id:
            return jsonify({"error": "I parametri dataflow_id e ref_id sono obbligatori"}), 400
        
        fr = FiltersRetriever(dataflow_id, ref_id)
        filters_dict = fr.get_filters_dictionary()
        
        #logging.info("Received response in %s seconds", time.time() - start_time)
        return jsonify(filters_dict)
    except ValueError as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/data", methods=["POST"])
def get_data():
    try:
        data = request.get_json()
        
        dataflow_id = data.get("dataflow_id")
        ref_id = data.get("ref_id")
        
        filters_dict = data.get("filters", {})
        
        if not dataflow_id or not ref_id:
            return jsonify({"error": "I parametri dataflow_id e ref_id sono obbligatori"}), 400
        

        if not isinstance(filters_dict, dict):
            return jsonify({"error": "Invalid input, expected a dictionary"}), 400
        
        data_ret = DataRetriever(dataflow_id, ref_id, filters_dict)
        df = data_ret.get_data()
        return df.to_dict(orient="records")  
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 500
        
      

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
