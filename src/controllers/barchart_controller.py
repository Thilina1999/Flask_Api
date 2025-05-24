from datetime import datetime
from flask import request, jsonify
import uuid

from ... import db
from ..models.ih_model import InventoryHistory
from ..models.mgt_tresh import MgtThreshHold
from flask import request, jsonify
import pandas as pd
import numpy as np
import csv
import sys
from sqlalchemy import distinct, inspect

def list_all_inventory_history_controller():
    inventory_history = InventoryHistory.query.all()
    response = []
    for inventory_history in inventory_history: response.append(inventory_history.to_dict())
    return jsonify(response)

def list_all_msgt_threshold_controller():
    mgt_thresh_hold = MgtThreshHold.query.all()
    response = []
    for mgt_thresh_hold in mgt_thresh_hold: response.append(mgt_thresh_hold.to_dict())
    return jsonify(response)