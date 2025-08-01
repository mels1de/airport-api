import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4

Base = declarative_base()

class Airport(Base):
    __tablename__ = "airports"

    id = sa.Column(PG_UUID(as_uuid=True),primary_key=True,default=uuid4)
    name = sa.Column(sa.String(100),nullable=False)
    iata_code = sa.Column(sa.String(3),nullable=False,index=True,unique=True)
    city = sa.Column(sa.String(100),nullable=False)
    country = sa.Column(sa.String(100),nullable=False)

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "iata_code": self.iata_code,
            "city": self.city,
            "country": self.country,
        }
