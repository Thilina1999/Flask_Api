from datetime import datetime, timedelta
from flask import request, jsonify
import uuid

from ... import db
from ..models.master_model import MgtMaster

from flask import request, jsonify
import pandas as pd
import numpy as np
import csv
import sys
from sqlalchemy import distinct, inspect, func, cast, Date
from datetime import datetime


def list_all_mgt_master_controller():
    mgt_master = MgtMaster.query.all()
    response = []
    for mgt_master in mgt_master: response.append(mgt_master.to_dict())
    return jsonify(response)

def insert_mgt_master_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    try:
        df = pd.read_csv(file)

        required_columns = [
            '設備グループID', '設備機番', '設備グループ名称', '在庫管理グループID',
            '在庫管理グループ名称', '基準在庫日数', '基準在庫管理幅'
        ]

        if not all(col in df.columns for col in required_columns):
            return jsonify({'error': 'Missing required columns in the CSV file'}), 400

        # Convert numeric columns
        df['基準在庫日数'] = pd.to_numeric(df['基準在庫日数'], errors='coerce')
        df['基準在庫管理幅'] = pd.to_numeric(df['基準在庫管理幅'], errors='coerce')

        # Drop rows with missing required fields (composite key and numerics)
        df = df.dropna(subset=['設備グループID', '設備機番', '基準在庫日数', '基準在庫管理幅'])

        # Drop duplicates based on composite primary key
        df = df.drop_duplicates(subset=['設備グループID', '設備機番'])

        records = []
        for _, row in df.iterrows():
            record = MgtMaster(
                設備グループID=row['設備グループID'],
                設備機番=row['設備機番'],
                設備グループ名称=row['設備グループ名称'],
                在庫管理グループID=row['在庫管理グループID'],
                在庫管理グループ名称=row['在庫管理グループ名称'],
                基準在庫日数=row['基準在庫日数'],
                基準在庫管理幅=row['基準在庫管理幅']
            )
            records.append(record)

        db.session.bulk_save_objects(records)
        db.session.commit()

        return jsonify({'message': 'MgtMaster data inserted successfully!'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
def list_all_mgtmaster_page_controller():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    # Start with base query
    query = MgtMaster.query

    # Paginate the query
    pagination = query.order_by(MgtMaster.設備グループID, MgtMaster.設備機番).paginate(
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