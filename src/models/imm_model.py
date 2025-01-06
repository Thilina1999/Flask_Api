from sqlalchemy import inspect, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship, validates
from sqlalchemy.types import String, Numeric, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ----------------------------------------------- #

class InventoryManagementMaster(db.Model):
    """Model representing Inventory Management Master Table."""
    
    __tablename__ = 'InventoryManagementMaster'

    # Columns
    Id = db.Column(Integer, primary_key=True, autoincrement=True)
    FacilityGroupID = db.Column(String(20), nullable=False)
    EquipmentNumber = db.Column(String(20), nullable=False)
    FacilityGroupName = db.Column(String(100))
    InventoryManagementGroupID = db.Column(String(20), nullable=False)
    InventoryManagementGroupName = db.Column(String(100))
    StandardInventoryDays = db.Column(Numeric(18, 0))
    StandardInventoryControlRange = db.Column(Numeric(18, 2))

    # Auto Generated Fields
    created = db.Column(DateTime(timezone=True), default=datetime.now)                           # Creation date
    updated = db.Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)    # Last update date

    # Relationships
    base_stocks = relationship("BaseStock", back_populates="inventory_management", cascade="all, delete-orphan")

    # Validations
    @validates('FacilityGroupName', 'InventoryManagementGroupName')
    def empty_string_to_null(self, key, value):
        return None if isinstance(value, str) and value.strip() == '' else value

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"<InventoryManagementMaster(Id={self.Id})>"

# ----------------------------------------------- #

class BaseStock(db.Model):
    """Model representing Base Stock Table."""
    
    __tablename__ = 'BaseStock'

    # Columns
    BaseStockID = db.Column(Integer, primary_key=True, autoincrement=True)
    InventoryManagementId = db.Column(Integer, ForeignKey('InventoryManagementMaster.Id'), nullable=False)
    BaseStockLevel = db.Column(Numeric(18,2))
    LastUpdated = db.Column(DateTime, nullable=False, default=datetime.now)

    # Relationships
    inventory_management = relationship("InventoryManagementMaster", back_populates="base_stocks")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"<BaseStock(BaseStockID={self.BaseStockID}, InventoryManagementId={self.InventoryManagementId})>"
