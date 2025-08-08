import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
from sqlalchemy.sql import func

Base = declarative_base()

class Airport(Base):
    __tablename__ = "airports"

    id = sa.Column(PG_UUID(as_uuid=True),primary_key=True,default=uuid4)
    name = sa.Column(sa.String(100),nullable=False)
    iata_code = sa.Column(sa.String(3),nullable=False,index=True,unique=True)
    city = sa.Column(sa.String(100),nullable=False)
    country = sa.Column(sa.String(100),nullable=False)

class User(Base):
    __tablename__ = "users"

    id = sa.Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = sa.Column(sa.String(50), nullable=False, unique=True, index=True)
    email = sa.Column(sa.String(100),nullable=False,unique=True,index=True)
    hashed_password = sa.Column(sa.String(128), nullable=False)
    role = sa.Column(sa.String(20),nullable=False,default="user")
    created_at = sa.Column(sa.DateTime(timezone=True),server_default=func.now())


    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "iata_code": self.iata_code,
            "city": self.city,
            "country": self.country,
        }

    def to_public_dict(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created else None
        }