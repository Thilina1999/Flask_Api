from flask import request

from ...app import app
from ..controllers.imm_controller import list_all_inventory_controller

@app.route("/inventory", methods=['GET'])
def list_create_accounts():
    if request.method == 'GET': return list_all_inventory_controller()
    else: return 'Method is Not Allowed'