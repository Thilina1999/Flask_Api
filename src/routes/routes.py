from flask import request

from ...app import app
from ..controllers.ims_controller import list_all_Inventory_controller, get_distinct_manufacturers, insert_data, get_shipping_classification, list_all_Inventory_page_controller, get_inventory_sums
from ..controllers.imm_controller import list_all_Noxstatus_controller, insert_nox_data,  list_all_Noxstatus_page_controller, get_distinct_subproject, get_distinct_status
from ..controllers.iiav_controller import list_all_CapacityWeekly_controller, insert_capacity_data, list_all_CapacityWeekly_page_controller

# Inventory
@app.route("/inventory", methods=['GET'])
def list_inventory_data():
    if request.method == 'GET': return list_all_Inventory_controller()
    else: return 'Method is Not Allowed'

@app.route("/inventory_insert", methods=['POST'])
def list_create_inventory_insert():
    if request.method == 'POST': return insert_data()
    else: return 'Method is Not Allowed'

@app.route("/inventory_shipping_classification", methods=['GET'])
def list_get_shipping_classification():
    if request.method == 'GET': return get_shipping_classification()
    else: return 'Method is Not Allowed'

@app.route("/inventory_manufactures", methods=['GET'])
def list_get_manufactures():
    if request.method == 'GET': return get_distinct_manufacturers()
    else: return 'Method is Not Allowed'

@app.route("/inventory_page", methods=['GET'])
def list_get_iventory_paginate():
    if request.method == 'GET': return list_all_Inventory_page_controller()
    else: return 'Method is Not Allowed'

@app.route("/inventory_sum", methods=['GET'])
def list_get_iventory_sums():
    if request.method == 'GET': return get_inventory_sums()
    else: return 'Method is Not Allowed'

#NoxStatus
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
    
#WeeklyCapacity
@app.route("/capacity", methods=['GET'])
def list_get_capacity_weekly():
    if request.method == 'GET': return list_all_CapacityWeekly_controller()
    else: return 'Method is Not Allowed'
    
@app.route("/insert_capacity", methods=['POST'])
def list_create_weekly_capacity_insert():
    if request.method == 'POST': return insert_capacity_data()
    else: return 'Method is Not Allowed'
    
@app.route("/capacity_weekly_page", methods=['GET'])
def list_get_capacity_weekly_paginate():
    if request.method == 'GET': return list_all_CapacityWeekly_page_controller()
    else: return 'Method is Not Allowed'