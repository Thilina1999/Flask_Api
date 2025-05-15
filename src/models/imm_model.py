from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.mssql import NVARCHAR
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class NoxStatus(db.Model):
    __tablename__ = 'assy_status'  # Adjust table name if needed

    棚札ID = Column(NVARCHAR(16), nullable=True)
    品番 = Column(NVARCHAR(20), nullable=True)
    次工程名称 = Column(NVARCHAR(200), nullable=True)
    加工Lot = Column(NVARCHAR(24), primary_key=True)
    数量 = Column(Integer, nullable=True)
    作業状況 = Column(Integer, nullable=True)
    棚札登録日時 = Column(DateTime, nullable=True)
    棚札更新日時 = Column(DateTime, nullable=True)
    滞留日数 = Column(Integer, nullable=True)

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}

    def __repr__(self):
        return f"<NoxStatus(加工Lot={self.加工Lot})>"