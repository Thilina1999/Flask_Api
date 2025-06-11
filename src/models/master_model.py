from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, NVARCHAR, Numeric

db = SQLAlchemy()

class MgtMaster(db.Model):
    __tablename__ = 'mgt_master'

    設備グループID = db.Column(NVARCHAR(20), primary_key=True, nullable=False)
    設備機番 = db.Column(NVARCHAR(20), primary_key=True, nullable=False)
    設備グループ名称 = db.Column(NVARCHAR(100))
    在庫管理グループID = db.Column(NVARCHAR(20))
    在庫管理グループ名称 = db.Column(NVARCHAR(100))
    基準在庫日数 = db.Column(Numeric(18, 0))
    基準在庫管理幅 = db.Column(Numeric(18, 2))

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}

    def __repr__(self):
        return (f"<MgtMaster(設備グループID={self.設備グループID}, "
                f"設備機番={self.設備機番})>")
