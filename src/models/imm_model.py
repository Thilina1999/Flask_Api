from sqlalchemy import inspect
from datetime import datetime
from sqlalchemy.orm import validates
from sqlalchemy.types import String, Numeric
from flask_sqlalchemy import SQLAlchemy

# Assuming 'db' is initialized in __init__.py
db = SQLAlchemy()

# ----------------------------------------------- #

class InventoryManagementMaster(db.Model):
    # Table name
    __tablename__ = 'InventoryManagementMaster'

    # Columns
    FacilityGroupID = db.Column(String(20), primary_key=True, nullable=False)
    EquipmentNumber = db.Column(String(20), nullable=False)
    FacilityGroupName = db.Column(String(100))
    InventoryManagementGroupID = db.Column(String(20), primary_key=True, nullable=False)
    InventoryManagementGroupName = db.Column(String(100))
    StandardInventoryDays = db.Column(Numeric(18, 0))
    StandardInventoryControlRange = db.Column(Numeric(18, 2))

    # Auto Generated Fields
    created = db.Column(db.DateTime(timezone=True), default=datetime.now)                           # Creation date
    updated = db.Column(db.DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)    # Last update date

    # Validations
    @validates('FacilityGroupName', 'InventoryManagementGroupName')
    def empty_string_to_null(self, key, value):
        """Set an empty string to null for string fields."""
        if isinstance(value, str) and value.strip() == '':
            return None
        return value

    # Serialize model to dictionary
    def to_dict(self):
        """Convert the SQLAlchemy object to a dictionary."""
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        """String representation for debugging."""
        return (
            f"<InventoryManagementMaster(FacilityGroupID='{self.FacilityGroupID}', "
            f"InventoryManagementGroupID='{self.InventoryManagementGroupID}')>"
        )
