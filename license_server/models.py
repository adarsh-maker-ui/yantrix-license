from sqlalchemy import Column, String, DateTime
from datetime import datetime, timedelta

from license_server.database import Base


class License(Base):
    __tablename__ = "licenses"

    device_id = Column(String, primary_key=True, index=True)
    issued_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    last_check = Column(DateTime, nullable=True)
    status = Column(String, default="ACTIVE")

    @staticmethod
    def new(device_id: str):
        now = datetime.utcnow()
        return License(
            device_id=device_id,
            issued_at=now,
            expires_at=now + timedelta(days=30),
            status="ACTIVE"
        )
