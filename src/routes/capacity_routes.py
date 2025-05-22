from flask import request
from ...app import app
from ..controllers.iiav_controller import (
    list_all_CapacityWeekly_controller,
    insert_capacity_data,
    list_all_CapacityWeekly_page_controller
)

# WeeklyCapacity Routes
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