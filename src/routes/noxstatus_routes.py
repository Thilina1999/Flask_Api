from flask import request
from ...app import app
from ..controllers.imm_controller import (
    list_all_Noxstatus_controller,
    insert_nox_data,
    list_all_Noxstatus_page_controller,
    get_distinct_subproject,
    get_distinct_status
)

# NoxStatus Routes
@app.route("/status", methods=['GET'])
def list_noxstatus_data():
    if request.method == 'GET': return list_all_Noxstatus_controller()
    else: return 'Method is Not Allowed'

@app.route("/status_insert", methods=['POST'])
def list_create_noxstatus_insert():
    if request.method == 'POST': return insert_nox_data()
    else: return 'Method is Not Allowed'

@app.route("/status_page", methods=['GET'])
def list_get_status_paginate():
    if request.method == 'GET': return list_all_Noxstatus_page_controller()
    else: return 'Method is Not Allowed'

@app.route("/subproject", methods=['GET'])
def list_get_subproject():
    if request.method == 'GET': return get_distinct_subproject()
    else: return 'Method is Not Allowed'
    
@app.route("/status_all", methods=['GET'])
def list_get_status_num():
    if request.method == 'GET': return get_distinct_status()
    else: return 'Method is Not Allowed'