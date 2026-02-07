from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from license_server.database import SessionLocal
from license_server.models import License

router = APIRouter(prefix="/license", tags=["License"])


# -------------------------------------------------
# ADMIN: PROVISION A NEW LICENSE (30 DAYS)
# -------------------------------------------------
@router.post("/provision")
def provision_license(device_id: str):
    """
    ADMIN ONLY
    Create a new 30-day license for a device
    """
    db: Session = SessionLocal()

    existing = db.query(License).filter(
        License.device_id == device_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="License already exists for this device"
        )

    now = datetime.utcnow()

    license_obj = License(
        device_id=device_id,
        issued_at=now,
        expires_at=now + timedelta(days=30),
        status="ACTIVE"
    )

    db.add(license_obj)
    db.commit()

    return {
        "status": "CREATED",
        "device_id": device_id,
        "issued_at": license_obj.issued_at.isoformat(),
        "expires_at": license_obj.expires_at.isoformat()
    }


# -------------------------------------------------
# DEVICE: CHECK LICENSE STATUS
# -------------------------------------------------
@router.post("/check")
def check_license(device_id: str):
    """
    Device calls this endpoint at startup
    """
    db: Session = SessionLocal()

    lic = db.query(License).filter(
        License.device_id == device_id
    ).first()

    if not lic:
        raise HTTPException(
            status_code=403,
            detail="Device not registered"
        )

    now = datetime.utcnow()
    lic.last_check = now
    db.commit()

    # License expired
    if now > lic.expires_at:
        return {
            "status": "EXPIRED",
            "expires_at": lic.expires_at.isoformat(),
            "last_check": lic.last_check.isoformat()
        }

    # License valid
    return {
        "status": "VALID",
        "expires_at": lic.expires_at.isoformat(),
        "last_check": lic.last_check.isoformat()
    }
