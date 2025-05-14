from flask import request

from ...app import app
from ..controllers.imm_controller import list_all_inventory_controller, create_inventory_management_master, list_all_stock_controller, create_base_stock, insert_data_ims, delete_master_items
from ..controllers.ims_controller import list_all_Inventory_controller, get_distinct_manufacturers, insert_data, get_shipping_classification, list_all_Inventory_page_controller

@app.route("/inventory_data", methods=['GET', 'POST'])
def list_create_accounts():
    if request.method == 'GET': return list_all_inventory_controller()
    if request.method == 'POST': return create_inventory_management_master()
    else: return 'Method is Not Allowed'

@app.route("/stock", methods=['GET', 'POST'])
def list_create_stock_accounts():
    if request.method == 'GET': return list_all_stock_controller()
    if request.method == 'POST': return create_base_stock()
    else: return 'Method is Not Allowed'

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

# Histroy
@app.route("/history_insert_ims", methods=['POST'])
def list_create_history_master():
    if request.method == 'POST': return insert_data_ims()
    else: return 'Method is Not Allowed'

@app.route("/delete_master", methods=['POST'])
def delete_master():
    if request.method == 'POST': return delete_master_items()
    else: return 'Method is Not Allowed'
