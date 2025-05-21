from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.dialects.mssql import NVARCHAR
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CapacityWeekly(db.Model):
    __tablename__ = 'CapacityWeekly'

    品番 = Column(NVARCHAR(20), primary_key=True, nullable=False, unique=True)
    メーカ = Column(NVARCHAR(40), nullable=False)
    出荷区分 = Column(NVARCHAR(40), nullable=False)
    気密検査 = Column(Integer, nullable=False)
    SCU = Column(Integer, nullable=False)
    水蒸気検査 = Column(Integer, nullable=False)
    特性検査 = Column(Integer, nullable=False)
    特性検査端数品 = Column(Integer, nullable=False)
    アクセサリ = Column(Integer, nullable=False)
    FA = Column(Integer, nullable=False)
    FA端数品 = Column(Integer, nullable=False)
    外観検査 = Column(Integer, nullable=False)
    入庫実績 = Column(Integer, nullable=False)
    出荷前在庫 = Column(Integer, nullable=False)
    計画1 = Column(Integer, nullable=False)
    計画2 = Column(Integer, nullable=False)
    計画3 = Column(Integer, nullable=False)
    計画4 = Column(Integer, nullable=False)
    計画5 = Column(Integer, nullable=False)
    計画6 = Column(Integer, nullable=False)
    計画7 = Column(Integer, nullable=False)
    更新日時 = Column(DateTime, nullable=False)

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}

    def __repr__(self):
        return f"<CapacityWeekly(品番={self.品番})>"
