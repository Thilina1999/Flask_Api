from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.types import String, Integer, BigInteger, DateTime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ----------------------------------------------- #

class InventoryHistory(db.Model):
    """Model representing Inventory History Table."""
    
    __tablename__ = 'inventory_history'

    # Columns
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    assy_part_number = db.Column(BigInteger, nullable=False)
    subassy_product_number = db.Column(BigInteger, nullable=False)
    manufacturer = db.Column(String(255), nullable=False)
    shipping_classification = db.Column(String(50), nullable=False)
    airtightness_inspection = db.Column(Integer, nullable=False)
    scu = db.Column(Integer, nullable=False)
    water_vapor_test = db.Column(Integer, nullable=False)
    characteristic_inspection = db.Column(Integer, nullable=False)
    char_inspection_fractional_items = db.Column(Integer, nullable=False)
    accessor = db.Column(Integer, nullable=False)
    fa = db.Column(Integer, nullable=False)
    fa_fractional_items = db.Column(Integer, nullable=False)
    visual_inspection = db.Column(Integer, nullable=False)
    update_date_time = db.Column(DateTime, nullable=False, default=datetime.now)

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}

    def __repr__(self):
        return f"<InventoryHistory(BaseStockID={self.BaseStockID})>"
