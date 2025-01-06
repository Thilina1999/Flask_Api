from sqlalchemy import inspect
from datetime import datetime
from sqlalchemy.orm import validates
from sqlalchemy.types import String, Numeric
from flask_sqlalchemy import SQLAlchemy

# Assuming 'db' is initialized in __init__.py
db = SQLAlchemy()

class BaseStock(db.Model):
    __tablename__ = 'BaseStock'

    BaseStockID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    InventoryManagementId = db.Column(db.Integer, db.ForeignKey('InventoryManagementMaster.Id'), nullable=False)
    BaseStockLevel = db.Column(Numeric(18,2))
    LastUpdated = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # Relationship with InventoryManagementMaster
    inventory_management = db.relationship("InventoryManagementMaster", back_populates="base_stocks")

    def __repr__(self):
        return f"<BaseStock(BaseStockID={self.BaseStockID}, InventoryManagementId={self.InventoryManagementId})>"
