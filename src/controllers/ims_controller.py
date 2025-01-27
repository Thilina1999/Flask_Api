from flask import request, jsonify
import uuid
from datetime import datetime
from ... import db
from ..models.ims_model import InventoryHistory
import pandas as pd
import numpy as np
import csv
import sys

def list_all_history_controller():
    inventoryHistories = InventoryHistory.query.all()
    response = []
    for inventoryHistory in inventoryHistories: response.append(inventoryHistory.to_dict())
    return jsonify(response)

def create_inventory_history():
    """Endpoint to create a new InventoryHistory record."""
    
    # Parse JSON data from request
    request_data = request.get_json()

    # Extract values from the JSON payload
    assy_part_number = request_data.get('assy_part_number')
    subassy_product_number = request_data.get('subassy_product_number')
    manufacturer = request_data.get('manufacturer')
    shipping_classification = request_data.get('shipping_classification')
    airtightness_inspection = request_data.get('airtightness_inspection')
    scu = request_data.get('scu')
    water_vapor_test = request_data.get('water_vapor_test')
    characteristic_inspection = request_data.get('characteristic_inspection')
    char_inspection_fractional_items = request_data.get('char_inspection_fractional_items')
    accessor = request_data.get('accessor')
    fa = request_data.get('fa')
    fa_fractional_items = request_data.get('fa_fractional_items')
    visual_inspection = request_data.get('visual_inspection')

    # Validate required fields
    required_fields = [
        'assy_part_number', 'subassy_product_number', 'manufacturer', 'shipping_classification',
        'airtightness_inspection', 'scu', 'water_vapor_test', 'characteristic_inspection',
        'char_inspection_fractional_items', 'accessor', 'fa', 'fa_fractional_items', 'visual_inspection'
    ]
    
    missing_fields = [field for field in required_fields if request_data.get(field) is None]
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    # Create new InventoryHistory record
    new_inventory_history = InventoryHistory(
        assy_part_number=assy_part_number,
        subassy_product_number=subassy_product_number,
        manufacturer=manufacturer,
        shipping_classification=shipping_classification,
        airtightness_inspection=airtightness_inspection,
        scu=scu,
        water_vapor_test=water_vapor_test,
        characteristic_inspection=characteristic_inspection,
        char_inspection_fractional_items=char_inspection_fractional_items,
        accessor=accessor,
        fa=fa,
        fa_fractional_items=fa_fractional_items,
        visual_inspection=visual_inspection,
        update_date_time=datetime.now()  # Set current timestamp
    )

    # Add and commit to database
    db.session.add(new_inventory_history)
    db.session.commit()

    # Return response
    return jsonify(new_inventory_history.to_dict()), 201  # 201 Created

def insert_data():
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
            'assy_part_number', 'subassy_product_number', 'manufacturer', 
            'shipping_classification', 'airtightness_inspection', 'scu', 
            'water_vapor_test', 'characteristic_inspection', 
            'char_inspection_fractional_items', 'accessor', 'fa', 
            'fa_fractional_items', 'visual_inspection', 'update_date_time'
        ]

        if not all(col in distinct_data.columns for col in required_columns):
            return jsonify({'error': 'Missing required columns in the Excel file'}), 400

        # Process date column
        distinct_data['update_date_time'] = pd.to_datetime(distinct_data['update_date_time'], errors='coerce')

        # Handle invalid dates
        if distinct_data['update_date_time'].isnull().any():
            return jsonify({'error': 'Invalid date format in update_date_time column'}), 400

        # Insert data row by row into the database
        records = []
        for _, row in distinct_data.iterrows():
            record = InventoryHistory(
                assy_part_number=row['assy_part_number'],
                subassy_product_number=row['subassy_product_number'],
                manufacturer=row['manufacturer'],
                shipping_classification=row['shipping_classification'],
                airtightness_inspection=row['airtightness_inspection'],
                scu=row['scu'],
                water_vapor_test=row['water_vapor_test'],
                characteristic_inspection=row['characteristic_inspection'],
                char_inspection_fractional_items=row['char_inspection_fractional_items'],
                accessor=row['accessor'],
                fa=row['fa'],
                fa_fractional_items=row['fa_fractional_items'],
                visual_inspection=row['visual_inspection'],
                update_date_time=row['update_date_time']
            )
            records.append(record)

        # Add all records in one bulk transaction
        db.session.bulk_save_objects(records)
        db.session.commit()

        return jsonify({'message': 'Data inserted successfully!'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


