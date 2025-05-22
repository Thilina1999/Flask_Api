from flask import request
from ...app import app
from ..controllers.iiav_controller import (
    list_all_CapacityWeekly_controller,
    insert_capacity_data,
    list_all_CapacityWeekly_page_controller,
    get_distinct_manufacturers_buffer,
    get_shipping_classification_buffer
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
    
@app.route("/manufacture_buffer", methods=['GET'])
def list_get_manufacuture_buffer():
    if request.method == 'GET': return get_distinct_manufacturers_buffer()
    else: return 'Method is Not Allowed'
    
@app.route("/shipping_classification_buffer", methods=['GET'])
def list_get_shipping_classification_buffer():
    if request.method == 'GET': return get_shipping_classification_buffer()
    else: return 'Method is Not Allowed'