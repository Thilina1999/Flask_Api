from flask import request
from ...app import app

from ..controllers.barchart_controller import *

@app.route("/history", methods=['GET'])
def list_get_inventory_history():
    if request.method == 'GET': return list_all_inventory_history_controller()
    else: return 'Method is Not Allowed'
    
@app.route("/threshold", methods=['GET'])
def list_get_threshold():
    if request.method == 'GET': return list_all_msgt_threshold_controller()
    else: return 'Method is Not Allowed'
    
@app.route("/insert_history", methods=['POST'])
def list_history_inventory_insert():
    if request.method == 'POST': return insert_inventory_history_data()
    else: return 'Method is Not Allowed'

@app.route("/insert_threshold", methods=['POST'])
def list_mgt_threshold_insert():
    if request.method == 'POST': return insert_mgt_thresh_hold_data()
    else: return 'Method is Not Allowed' 

@app.route("/group_name", methods=['GET'])
def list_get_group_name():
    if request.method == 'GET': return get_group_name()
    else: return 'Method is Not Allowed' 
    
@app.route("/inventory_history", methods=['GET'])
def list_get_selected_inventory_history():
    if request.method == 'GET': return list_all_Selected_History_controller()
    else: return 'Method is Not Allowed' 
    
@app.route("/threshold_data", methods=['GET'])
def list_get_selected__mgt_threshold():
    if request.method == 'GET': return get_threshold_controller()
    else: return 'Method is Not Allowed' 
    
@app.route("/number_list", methods=['GET'])
def list_get_distinct_assy_number():
    if request.method == 'GET': return get_distinct_history_assy_number()
    else: return 'Method is Not Allowed' 
