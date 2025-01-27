from datetime import datetime
from flask import request, jsonify
import uuid

from ... import db
from ..models.imm_model import InventoryManagementMaster
from ..models.imm_model import BaseStock
from flask import request, jsonify
import pandas as pd
import numpy as np
import csv
import sys


# ----------------------------------------------- #

# Query Object Methods => https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query
# Session Object Methods => https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session
# How to serialize SqlAlchemy PostgreSQL Query to JSON => https://stackoverflow.com/a/46180522

def list_all_inventory_controller():
    inventories = InventoryManagementMaster.query.all()
    response = []
    for inventory in inventories: response.append(inventory.to_dict())
    return jsonify(response)

def list_all_stock_controller():
    baseStocks = BaseStock.query.all()
    response = []
    for baseStock in baseStocks: response.append(baseStock.to_dict())
    return jsonify(response)


def create_inventory_management_master():
    # Parse JSON data from the request body
    request_data = request.get_json()

    # Access the data from the JSON payload
    EquipmentNumber = request_data.get('EquipmentNumber')
    FacilityGroupID = request_data.get('FacilityGroupID')
    FacilityGroupName = request_data.get('FacilityGroupName')
    InventoryManagementGroupID = request_data.get('InventoryManagementGroupID')
    InventoryManagementGroupName = request_data.get('InventoryManagementGroupName')
    StandardInventoryControlRange = request_data.get('StandardInventoryControlRange')
    StandardInventoryDays = request_data.get('StandardInventoryDays')

    # Check if required fields are present
    if not EquipmentNumber or not FacilityGroupID or not FacilityGroupName:
        return jsonify({"error": "Missing required fields"}), 400

    # Create the new inventory record
    new_inventory = InventoryManagementMaster(
        EquipmentNumber=EquipmentNumber,
        FacilityGroupID=FacilityGroupID,
        FacilityGroupName=FacilityGroupName,
        InventoryManagementGroupID=InventoryManagementGroupID,
        InventoryManagementGroupName=InventoryManagementGroupName,
        StandardInventoryControlRange=StandardInventoryControlRange,
        StandardInventoryDays=StandardInventoryDays
    )

    # Add and commit the new inventory record to the database
    db.session.add(new_inventory)
    db.session.commit()

    # Convert the new inventory object to a dictionary and return as JSON
    response = new_inventory.to_dict()  # Assuming to_dict() method exists in your model
    return jsonify(response)

def create_base_stock():
    """Endpoint to create a new BaseStock record."""
    
    # Parse JSON data from request
    request_data = request.get_json()

    # Extract values from the JSON payload
    InventoryManagementId = request_data.get('InventoryManagementId')
    BaseStockLevel = request_data.get('BaseStockLevel')

    # Validate required fields
    if not InventoryManagementId:
        return jsonify({"error": "InventoryManagementId is required"}), 400
    
    # Check if the referenced InventoryManagementMaster exists
    inventory_management = InventoryManagementMaster.query.get(InventoryManagementId)
    if not inventory_management:
        return jsonify({"error": "Invalid InventoryManagementId"}), 404

    # Create new BaseStock record
    new_base_stock = BaseStock(
        InventoryManagementId=InventoryManagementId,
        BaseStockLevel=BaseStockLevel,
        LastUpdated=datetime.now()  # Set current timestamp
    )

    # Add and commit to database
    db.session.add(new_base_stock)
    db.session.commit()

    # Return response
    return jsonify(new_base_stock.to_dict()), 201  # 201 Created

def insert_data_ims():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    try:
        # Read the Excel file into a Pandas DataFrame
        df = pd.read_excel(file)

        # Drop duplicate rows to get distinct data
        distinct_data = df.drop_duplicates()

        # Check if required columns exist in the Excel file
        required_columns = [
            'FacilityGroupID', 'EquipmentNumber', 'FacilityGroupName',
            'InventoryManagementGroupID', 'InventoryManagementGroupName',
            'StandardInventoryDays', 'StandardInventoryControlRange'
        ]

        if not all(col in distinct_data.columns for col in required_columns):
            return jsonify({'error': 'Missing required columns in the Excel file'}), 400

        # Convert numeric fields and handle errors
        numeric_columns = ['StandardInventoryDays', 'StandardInventoryControlRange']
        for col in numeric_columns:
            distinct_data[col] = pd.to_numeric(distinct_data[col], errors='coerce')

        # Check for invalid numeric values
        if distinct_data[numeric_columns].isnull().any().any():
            return jsonify({'error': 'Invalid numeric format in numeric columns'}), 400

        # Insert data row by row into the database
        records = []
        for _, row in distinct_data.iterrows():
            record = InventoryManagementMaster(
                FacilityGroupID=row['FacilityGroupID'],
                EquipmentNumber=row['EquipmentNumber'],
                FacilityGroupName=row['FacilityGroupName'],
                InventoryManagementGroupID=row['InventoryManagementGroupID'],
                InventoryManagementGroupName=row['InventoryManagementGroupName'],
                StandardInventoryDays=row['StandardInventoryDays'],
                StandardInventoryControlRange=row['StandardInventoryControlRange']
            )
            records.append(record)

        # Add all records in one bulk transaction
        db.session.bulk_save_objects(records)
        db.session.commit()

        return jsonify({'message': 'Data inserted successfully!'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
