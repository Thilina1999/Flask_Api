from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.mssql import NVARCHAR
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MgtThreshHold(db.Model):
    __tablename__ = 'mgt_thresh_hold'

    品番 = Column(NVARCHAR(20), nullable=False)
    在庫管理グループ名称 = Column(NVARCHAR(100), nullable=False)
    基準在庫数 = Column(NVARCHAR(50), nullable=True)
    基準在庫上限数 = Column(NVARCHAR(50), nullable=True)
    基準在庫下限数 = Column(NVARCHAR(50), nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint(
            '品番',
            '在庫管理グループ名称',
            name='PK_mgt_thresh_hold'
        ),
    )

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}

    def __repr__(self):
        return f"<MgtThreshHold(品番={self.品番}, 在庫管理グループ名称={self.在庫管理グループ名称})>"

