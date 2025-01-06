from flask import request

from ...app import app
from ..controllers.imm_controller import list_all_inventory_controller, create_inventory_management_master, list_all_stock_controller

@app.route("/inventory", methods=['GET', 'POST'])
def list_create_accounts():
    if request.method == 'GET': return list_all_inventory_controller()
    if request.method == 'POST': return create_inventory_management_master()
    else: return 'Method is Not Allowed'

@app.route("/stock", methods=['GET'])
def list_create_stock_accounts():
    if request.method == 'GET': return list_all_stock_controller()
    else: return 'Method is Not Allowed'