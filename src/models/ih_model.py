from sqlalchemy import Column, Integer, DateTime, PrimaryKeyConstraint
from sqlalchemy.dialects.mssql import NVARCHAR, NCHAR
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class InventoryHistory(db.Model):
    __tablename__ = 'inventory_history'

    ASSY品番 = Column(NVARCHAR(10), nullable=False)
    SUBASSY品番 = Column(NCHAR(10), nullable=False)
    メーカ = Column(NVARCHAR(20), nullable=False)
    出荷区分 = Column(NVARCHAR(20), nullable=False)
    気密検査 = Column(Integer, nullable=True)
    SCU = Column(Integer, nullable=True)
    水蒸気検査 = Column(Integer, nullable=True)
    特性検査 = Column(Integer, nullable=True)
    特性検査端数品 = Column(Integer, nullable=True)
    アクセサリ = Column(Integer, nullable=True)
    FA = Column(Integer, nullable=True)
    FA端数品 = Column(Integer, nullable=True)
    外観検査 = Column(Integer, nullable=True)
    更新日時 = Column(DateTime, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint(
            'ASSY品番',
            'SUBASSY品番',
            'メーカ',
            '出荷区分',
            '更新日時',
            name='PK_inventory_history'
        ),
    )

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}

    def __repr__(self):
        return f"<InventoryHistory(ASSY品番={self.ASSY品番}, SUBASSY品番={self.SUBASSY品番}, メーカ={self.メーカ}, 出荷区分={self.出荷区分}, 更新日時={self.更新日時})>"
