from datetime import datetime
from flask import request, jsonify
import uuid

from ... import db
from ..models.imm_model import NoxStatus
from flask import request, jsonify
import pandas as pd
import numpy as np
import csv
import sys

def list_all_Noxstatus_controller():
    noxstatus = NoxStatus.query.all()
    response = []
    for noxstatus in noxstatus: response.append(noxstatus.to_dict())
    return jsonify(response)

def insert_nox_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    try:
        df = pd.read_csv(file)

        # Drop duplicates
        distinct_data = df.drop_duplicates()

        # Required columns
        required_columns = [
            '棚札ID', '品番', '次工程名称', '加工Lot',
            '数量', '作業状況', '棚札登録日時',
            '棚札更新日時', '滞留日数'
        ]

        if not all(col in distinct_data.columns for col in required_columns):
            return jsonify({'error': 'Missing required columns in the CSV file'}), 400

        # Convert datetime fields and handle errors
        for col in ['棚札登録日時', '棚札更新日時']:
            distinct_data[col] = pd.to_datetime(distinct_data[col], errors='coerce')  # Converts bad values to NaT
            distinct_data[col] = distinct_data[col].dt.strftime('%Y-%m-%d %H:%M:%S')  # Format for SQL Server

        # Drop rows where ID or datetime is missing
        distinct_data = distinct_data.dropna(subset=['棚札ID', '棚札登録日時', '棚札更新日時'])

        records = []
        for _, row in distinct_data.iterrows():
            record = NoxStatus(
                棚札ID=row['棚札ID'],
                品番=row['品番'],
                次工程名称=row['次工程名称'],
                加工Lot=row['加工Lot'],
                数量=int(row['数量']) if not pd.isnull(row['数量']) else None,
                作業状況=int(row['作業状況']) if not pd.isnull(row['作業状況']) else None,
                棚札登録日時=datetime.strptime(row['棚札登録日時'], '%Y-%m-%d %H:%M:%S'),
                棚札更新日時=datetime.strptime(row['棚札更新日時'], '%Y-%m-%d %H:%M:%S'),
                滞留日数=int(row['滞留日数']) if not pd.isnull(row['滞留日数']) else None
            )
            records.append(record)

        db.session.bulk_save_objects(records)
        db.session.commit()

        return jsonify({'message': 'Data inserted successfully!'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def list_all_Noxstatus_page_controller():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    # Start with base query
    query = NoxStatus.query

    # Paginate the query
    pagination = query.order_by(NoxStatus.棚札ID).paginate(
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

