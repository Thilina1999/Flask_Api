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
from sqlalchemy import distinct


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

    # Start with base query
    query = CapacityWeekly.query

    # Paginate the query
    pagination = query.order_by(CapacityWeekly.品番).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    response = {
        "data": [item.to_dict() for item in pagination.items],
        "meta": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total_pages": pagination.pages,
            "total_items": pagination.total
        }
    }

    return jsonify(response)