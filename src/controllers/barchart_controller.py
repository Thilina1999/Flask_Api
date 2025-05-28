from datetime import datetime, timedelta
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
from sqlalchemy import distinct, inspect, func, cast, Date
from datetime import datetime


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

def insert_inventory_history_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    try:
        df = pd.read_csv(file)

        required_columns = [
            'ASSY品番', 'SUBASSY品番', 'メーカ', '出荷区分',
            '気密検査', 'SCU', '水蒸気検査', '特性検査', '特性検査端数品',
            'アクセサリ', 'FA', 'FA端数品', '外観検査', '更新日時'
        ]

        if not all(col in df.columns for col in required_columns):
            return jsonify({'error': 'Missing required columns in the CSV file'}), 400

        # Convert 更新日時 to datetime
        df['更新日時'] = pd.to_datetime(df['更新日時'], errors='coerce')
        df = df.dropna(subset=['ASSY品番', 'SUBASSY品番', 'メーカ', '出荷区分', '更新日時'])

        # Drop duplicates based on composite primary key
        df = df.drop_duplicates(subset=['ASSY品番', 'SUBASSY品番', 'メーカ', '出荷区分', '更新日時'])

        records = []
        for _, row in df.iterrows():
            record = InventoryHistory(
                ASSY品番=row['ASSY品番'],
                SUBASSY品番=row['SUBASSY品番'],
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
                更新日時=row['更新日時']
            )
            records.append(record)

        db.session.bulk_save_objects(records)
        db.session.commit()

        return jsonify({'message': 'Inventory history data inserted successfully!'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
def insert_mgt_thresh_hold_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    try:
        df = pd.read_csv(file)

        required_columns = [
            '品番', '在庫管理グループ名称',
            '基準在庫数', '基準在庫上限数', '基準在庫下限数'
        ]

        if not all(col in df.columns for col in required_columns):
            return jsonify({'error': 'Missing required columns in the CSV file'}), 400

        # Drop rows missing key columns and drop duplicates on composite PK
        df = df.dropna(subset=['品番', '在庫管理グループ名称'])
        df = df.drop_duplicates(subset=['品番', '在庫管理グループ名称'])

        records = []
        for _, row in df.iterrows():
            record = MgtThreshHold(
                品番=row['品番'],
                在庫管理グループ名称=row['在庫管理グループ名称'],
                基準在庫数=row['基準在庫数'],
                基準在庫上限数=row['基準在庫上限数'],
                基準在庫下限数=row['基準在庫下限数'],
            )
            records.append(record)

        db.session.bulk_save_objects(records)
        db.session.commit()

        return jsonify({'message': 'Threshold data inserted successfully!'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def get_group_name():
    try:
        group_name = db.session.query(distinct(MgtThreshHold.在庫管理グループ名称)).all()

        group_name_list = [m[0] for m in group_name]

        return jsonify(group_name_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

def list_all_Selected_History_controller():
    assy = request.args.get('ASSY品番')
    column = request.args.get('option')
    start_date = request.args.get('開始日')
    end_date = request.args.get('終了日')
    time_unit = request.args.get('time_unit')  # e.g., "日单位"

    if not all([assy, column, start_date, end_date]):
        return jsonify({'error': 'Missing required parameters: ASSY品番, option, 開始日, 終了日'}), 400

    try:
        # Parse ISO 8601 format
        start_datetime = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end_datetime = datetime.fromisoformat(end_date.replace('Z', '+00:00'))

        query = InventoryHistory.query.filter(
            InventoryHistory.ASSY品番 == assy,
            InventoryHistory.更新日時 >= start_datetime,
            InventoryHistory.更新日時 <= end_datetime
        )

        # Group by day if time_unit is "日单位"
        if time_unit == "日单位":
            # Get the actual results from the database
            results = (
                query
                .with_entities(
                    cast(InventoryHistory.更新日時, Date).label('day'),
                    func.sum(getattr(InventoryHistory, column)).label('total')
                )
                .group_by(cast(InventoryHistory.更新日時, Date))
                .order_by('day')
                .all()
            )
            
            # Convert results to a dictionary for easier lookup
            results_dict = {day: total for day, total in results}
            
            # Generate complete date range
            date_range = []
            current_date = start_datetime.date()
            end_date_date = end_datetime.date()
            
            while current_date <= end_date_date:
                date_range.append(current_date)
                current_date += timedelta(days=1)
            
            # Build response with 0 for missing days
            response = []
            for day in date_range:
                total = results_dict.get(day, 0)
                response.append({
                    'time': day.isoformat(),
                    'data': total
                })
                
        else:
            # Default: return raw records
            response = [{
                'time': record.更新日時.isoformat() + 'Z',
                'data': getattr(record, column, None)
            } for record in query.order_by(InventoryHistory.更新日時.asc()).all()]

        return jsonify(response)

    except ValueError as e:
        return jsonify({
            'error': 'Invalid date format. Expected ISO format (e.g., 2024-09-23T18:30:00.000Z)',
            'details': str(e)
        }), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    
def get_threshold_controller():
    part_number = request.args.get('品番')
    group_name = request.args.get('在庫管理グループ名称')
    
    if not part_number or not group_name:
        return jsonify({
            'error': 'Missing required parameters: 品番 and 在庫管理グループ名称'
        }), 400
    
    try:
        # Query the database for matching records
        records = MgtThreshHold.query.filter(
            MgtThreshHold.品番 == part_number,
            MgtThreshHold.在庫管理グループ名称 == group_name
        ).all()
        
        if not records:
            return jsonify({
                'error': 'No records found for the specified parameters'
            }), 404
        
        # Convert records to dictionaries
        response = [record.to_dict() for record in records]
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500