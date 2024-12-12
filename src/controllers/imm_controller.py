from flask import request, jsonify
import uuid

from ... import db
from ..models.imm_model import InventoryManagementMaster

# ----------------------------------------------- #

# Query Object Methods => https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query
# Session Object Methods => https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session
# How to serialize SqlAlchemy PostgreSQL Query to JSON => https://stackoverflow.com/a/46180522

def list_all_inventory_controller():
    inventories = InventoryManagementMaster.query.all()
    response = []
    for inventory in inventories: response.append(inventory.to_dict())
    return jsonify(response)