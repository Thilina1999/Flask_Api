from flask import request

from ...app import app
from ..controllers.imm_controller import list_all_inventory_controller, create_inventory_management_master, list_all_stock_controller, create_base_stock, insert_data_ims
from ..controllers.ims_controller import list_all_history_controller, create_inventory_history, insert_data

@app.route("/inventory", methods=['GET', 'POST'])
def list_create_accounts():
    if request.method == 'GET': return list_all_inventory_controller()
    if request.method == 'POST': return create_inventory_management_master()
    else: return 'Method is Not Allowed'

@app.route("/stock", methods=['GET', 'POST'])
def list_create_stock_accounts():
    if request.method == 'GET': return list_all_stock_controller()
    if request.method == 'POST': return create_base_stock()
    else: return 'Method is Not Allowed'

@app.route("/history", methods=['GET', 'POST'])
def list_create_history_accounts():
    if request.method == 'GET': return list_all_history_controller()
    if request.method == 'POST': return create_inventory_history()
    else: return 'Method is Not Allowed'

@app.route("/history_insert", methods=['POST'])
def list_create_history_insert():
    if request.method == 'POST': return insert_data()
    else: return 'Method is Not Allowed'

@app.route("/history_insert_ims", methods=['POST'])
def list_create_history_master():
    if request.method == 'POST': return insert_data_ims()
    else: return 'Method is Not Allowed'

