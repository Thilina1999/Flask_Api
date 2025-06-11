from ...app import app

@app.route('/')
def hello():
    return "Inventory App"

from .inventory_routes import *
from .noxstatus_routes import *
from .capacity_routes import *
from .barchart_routes import *
from .mgt_master_routes import*

