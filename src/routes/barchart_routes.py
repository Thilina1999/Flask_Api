from flask import request
from ...app import app

from ..controllers.barchart_controller import *

@app.route("/history", methods=['GET'])
def list_get_inventory_history():
    if request.method == 'GET': return list_all_inventory_history_controller()
    else: return 'Method is Not Allowed'
    
@app.route("/history", methods=['GET'])
def list_get_inventory_history():
    if request.method == 'GET': return list_all_msgt_threshold_controller()
    else: return 'Method is Not Allowed'