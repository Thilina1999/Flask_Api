from flask import request
from ...app import app
from ..controllers.ims_controller import (
    list_all_Inventory_controller,
    get_distinct_manufacturers,
    insert_data,
    get_shipping_classification,
    list_all_Inventory_page_controller,
    get_inventory_sums
)

# Inventory Routes
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