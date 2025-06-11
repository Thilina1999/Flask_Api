from flask import request
from ...app import app

from ..controllers.mgt_master_controller import ( list_all_mgt_master_controller, insert_mgt_master_data, list_all_mgtmaster_page_controller )

@app.route("/mgt_master", methods=['GET'])
def list_mgt_master_data():
    if request.method == 'GET': return list_all_mgt_master_controller()
    else: return 'Method is Not Allowed'
    
@app.route("/insert_mgt_master", methods=['POST'])
def list_mgt_master_insert():
    if request.method == 'POST': return insert_mgt_master_data()
    else: return 'Method is Not Allowed'
    
@app.route("/mgt_master_page", methods=['GET'])
def list_get_mgt_master_paginate():
    if request.method == 'GET': return list_all_mgtmaster_page_controller()
    else: return 'Method is Not Allowed'