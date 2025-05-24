from datetime import datetime
from flask import request, jsonify
import uuid

from ... import db
from ..models.iiav_model import CapacityWeekly
from flask import request, jsonify
import pandas as pd
import numpy as np
import csv
import sys
from sqlalchemy import distinct, inspect


def list_all_CapacityWeekly_controller():
    capacity_weekly = CapacityWeekly.query.all()
    response = []
    for capacity_weekly in capacity_weekly: response.append(capacity_weekly.to_dict())
    return jsonify(response)

def insert_capacity_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    try:
        df = pd.read_csv(file)

        # Drop duplicates based on primary key (品番)
        distinct_data = df.drop_duplicates(subset=['品番'])

        required_columns = [
            '品番', 'メーカ', '出荷区分', '気密検査', 'SCU',
            '水蒸気検査', '特性検査', '特性検査端数品', 'アクセサリ',
            'FA', 'FA端数品', '外観検査', '入庫実績', '出荷前在庫',
            '計画1', '計画2', '計画3', '計画4', '計画5', '計画6',
            '計画7', '更新日時'
        ]

        if not all(col in distinct_data.columns for col in required_columns):
            return jsonify({'error': 'Missing required columns in the CSV file'}), 400

        # Convert 更新日時 to datetime
        distinct_data['更新日時'] = pd.to_datetime(distinct_data['更新日時'], errors='coerce')
        distinct_data = distinct_data.dropna(subset=['品番', '更新日時'])

        records = []
        for _, row in distinct_data.iterrows():
            record = CapacityWeekly(
                品番=row['品番'],
                メーカ=row['メーカ'],
                出荷区分=row['出荷区分'],
                気密検査=int(row['気密検査']),
                SCU=int(row['SCU']),
                水蒸気検査=int(row['水蒸気検査']),
                特性検査=int(row['特性検査']),
                特性検査端数品=int(row['特性検査端数品']),
                アクセサリ=int(row['アクセサリ']),
                FA=int(row['FA']),
                FA端数品=int(row['FA端数品']),
                外観検査=int(row['外観検査']),
                入庫実績=int(row['入庫実績']),
                出荷前在庫=int(row['出荷前在庫']),
                計画1=int(row['計画1']),
                計画2=int(row['計画2']),
                計画3=int(row['計画3']),
                計画4=int(row['計画4']),
                計画5=int(row['計画5']),
                計画6=int(row['計画6']),
                計画7=int(row['計画7']),
                更新日時=row['更新日時']
            )
            records.append(record)

        db.session.bulk_save_objects(records)
        db.session.commit()

        return jsonify({'message': 'Capacity data inserted successfully!'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
def list_all_CapacityWeekly_page_controller():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    num = request.args.get('品番')
    maker = request.args.get('メーカ')
    shipping = request.args.get('出荷区分')
    range1 = request.args.get('開始工程')
    range2 = request.args.get('終了工程')
    
    # Start with base query
    query = CapacityWeekly.query

    if num:
        query = query.filter(CapacityWeekly.品番.like(f'{num}%'))
    if maker:
        query = query.filter(CapacityWeekly.メーカ == maker)
    if shipping:
        query = query.filter(CapacityWeekly.出荷区分 == shipping)
        
    # Paginate the query
    pagination = query.order_by(CapacityWeekly.品番).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    # Process all items to include range_sum where applicable
    items_data = []
    for item in pagination.items:
        item_dict = item.to_dict()
        
        # Calculate range sum for this item
        range_sum = calculate_range_sum(
            item,
            range1,
            range2
        )
        
        if range_sum is not None:
            item_dict['range_sum'] = range_sum
            
        items_data.append(item_dict)

    response = {
        "data": items_data,
        "meta": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total_pages": pagination.pages,
            "total_items": pagination.total
        }
    }

    return jsonify(response)


def get_distinct_manufacturers_buffer():
    try:
        manufacturers = db.session.query(distinct(CapacityWeekly.メーカ)).all()

        manufacturer_list = [m[0] for m in manufacturers]

        return jsonify(manufacturer_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def get_shipping_classification_buffer():
    try:
        shipping_classification = db.session.query(distinct(CapacityWeekly.出荷区分)).all()

        shipping_classification_list = [m[0] for m in shipping_classification]

        return jsonify(shipping_classification_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 
    
    
def calculate_range_sum(item, range1, range2):
    if not (range1 and range2):
        return None
    
    # Get the model class from the instance
    model_class = item.__class__
    
    # Use SQLAlchemy inspector to get columns in proper order
    inspector = inspect(model_class)
    columns = [column.name for column in inspector.columns]
    
    try:
        # Find positions of range columns
        start_idx = columns.index(range1)
        end_idx = columns.index(range2)
        
        # Swap if ranges are reversed
        if start_idx > end_idx:
            start_idx, end_idx = end_idx, start_idx
        
        # Calculate sum of all numeric values in range
        range_sum = 0
        for col in columns[start_idx:end_idx+1]:
            value = getattr(item, col)
            if isinstance(value, (int, float)):
                range_sum += value
        
        return range_sum
        
    except ValueError:  # If columns don't exist
        return None