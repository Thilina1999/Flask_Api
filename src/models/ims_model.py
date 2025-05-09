from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, NCHAR, NVARCHAR, Integer, DateTime

db = SQLAlchemy()

class Inventory(db.Model):
    __tablename__ = 'inventory'

    ASSY品番 = db.Column(NVARCHAR(20), primary_key=True, nullable=False)
    SUBASSY品番 = db.Column(NCHAR(20), nullable=False)
    メーカ = db.Column(NVARCHAR(40), nullable=False)
    出荷区分 = db.Column(NVARCHAR(40), nullable=False)
    気密検査 = db.Column(Integer, nullable=False)
    SCU = db.Column(Integer, nullable=False)
    水蒸気検査 = db.Column(Integer, nullable=False)
    特性検査 = db.Column(Integer, nullable=False)
    特性検査端数品 = db.Column(Integer, nullable=False)
    アクセサリ = db.Column(Integer, nullable=False)
    FA = db.Column(Integer, nullable=False)
    FA端数品 = db.Column(Integer, nullable=False)
    外観検査 = db.Column(Integer, nullable=False)
    更新日時 = db.Column(DateTime, nullable=False, default=datetime.now)

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}

    def __repr__(self):
        return f"<Inventory(ASSY品番={self.ASSY品番})>"
