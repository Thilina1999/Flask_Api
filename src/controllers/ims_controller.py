from flask import request, jsonify
import uuid
from ... import db
from ..models.ims_model import Inventory
import pandas as pd
import numpy as np
from sqlalchemy import distinct, func

def list_all_Inventory_controller():
    inventory = Inventory.query.all()
    response = []
    for inventory in inventory: response.append(inventory.to_dict())
    return jsonify(response)

def list_all_Inventory_page_controller():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    subassy = request.args.get('SUBASSY品番')
    maker = request.args.get('メーカ')
    shipping = request.args.get('出荷区分')

    query = Inventory.query

    if subassy:
        query = query.filter(Inventory.SUBASSY品番.like(f'{subassy}%'))
    if maker:
        query = query.filter(Inventory.メーカ == maker)
    if shipping:
        query = query.filter(Inventory.出荷区分 == shipping)

    # Paginate the filtered query
    pagination = query.order_by(Inventory.ASSY品番).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    # Compute sums for the filtered data
    try:
        sums = query.with_entities(
            func.sum(Inventory.気密検査).label("気密検査"),
            func.sum(Inventory.SCU).label("SCU"),
            func.sum(Inventory.水蒸気検査).label("水蒸気検査"),
            func.sum(Inventory.特性検査).label("特性検査"),
            func.sum(Inventory.特性検査端数品).label("特性検査端数品"),
            func.sum(Inventory.アクセサリ).label("アクセサリ"),
            func.sum(Inventory.FA).label("FA"),
            func.sum(Inventory.FA端数品).label("FA端数品"),
            func.sum(Inventory.外観検査).label("外観検査"),
        ).one()

        summary = {
            "気密検査": sums.気密検査 or 0,
            "SCU": sums.SCU or 0,
            "水蒸気検査": sums.水蒸気検査 or 0,
            "特性検査": sums.特性検査 or 0,
            "特性検査端数品": sums.特性検査端数品 or 0,
            "アクセサリ": sums.アクセサリ or 0,
            "FA": sums.FA or 0,
            "FA端数品": sums.FA端数品 or 0,
            "外観検査": sums.外観検査 or 0,
        }

        response = {
            "data": [item.to_dict() for item in pagination.items],
            "meta": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total_pages": pagination.pages,
                "total_items": pagination.total
            },
            "summary": summary
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def insert_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400
    
    try:
        # Read the Excel file into a Pandas DataFrame
        df = pd.read_csv(file)

        # Drop duplicate rows to get distinct data
        distinct_data = df.drop_duplicates()

        # Check if required columns exist in the Excel file
        required_columns = [
            'ASSY品番', 'SUBASSY品番', 'メーカ', 
            '出荷区分', '気密検査', 'SCU', 
            '水蒸気検査', '特性検査', 
            '特性検査端数品', 'アクセサリ', 'FA', 
            'FA端数品', '外観検査', '更新日時'
        ]

        if not all(col in distinct_data.columns for col in required_columns):
            return jsonify({'error': 'Missing required columns in the Excel file'}), 400


        # Insert data row by row into the database
        records = []
        for _, row in distinct_data.iterrows():
            record = Inventory(
                ASSY品番=row['ASSY品番'],
                SUBASSY品番=row['SUBASSY品番'],
                メーカ=row['メーカ'],
                出荷区分=row['出荷区分'],
                気密検査=row['気密検査'],
                SCU=row['SCU'],
                水蒸気検査=row['水蒸気検査'],
                特性検査=row['特性検査'],
                特性検査端数品=row['特性検査端数品'],
                アクセサリ=row['アクセサリ'],
                FA=row['FA'],
                FA端数品=row['FA端数品'],
                外観検査=row['外観検査'],
                更新日時=row['更新日時']
            )
            records.append(record)

        # Add all records in one bulk transaction
        db.session.bulk_save_objects(records)
        db.session.commit()

        return jsonify({'message': 'Data inserted successfully!'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


def get_distinct_manufacturers():
    try:
        manufacturers = db.session.query(distinct(Inventory.メーカ)).all()

        manufacturer_list = [m[0] for m in manufacturers]

        return jsonify(manufacturer_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def get_shipping_classification():
    try:
        shipping_classification = db.session.query(distinct(Inventory.出荷区分)).all()

        shipping_classification_list = [m[0] for m in shipping_classification]

        return jsonify(shipping_classification_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 
    
def get_inventory_sums():
    try:
        result = db.session.query(
            func.sum(Inventory.気密検査).label("気密検査"),
            func.sum(Inventory.SCU).label("SCU"),
            func.sum(Inventory.水蒸気検査).label("水蒸気検査"),
            func.sum(Inventory.特性検査).label("特性検査"),
            func.sum(Inventory.特性検査端数品).label("特性検査端数品"),
            func.sum(Inventory.アクセサリ).label("アクセサリ"),
            func.sum(Inventory.FA).label("FA"),
            func.sum(Inventory.FA端数品).label("FA端数品"),
            func.sum(Inventory.外観検査).label("外観検査"),
        ).one()

        data = {
            "気密検査": result.気密検査 or 0,
            "SCU": result.SCU or 0,
            "水蒸気検査": result.水蒸気検査 or 0,
            "特性検査": result.特性検査 or 0,
            "特性検査端数品": result.特性検査端数品 or 0,
            "アクセサリ": result.アクセサリ or 0,
            "FA": result.FA or 0,
            "FA端数品": result.FA端数品 or 0,
            "外観検査": result.外観検査 or 0,
        }

        return jsonify(data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 