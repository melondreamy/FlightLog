from fastapi import APIRouter, Depends, HTTPException, status
from sqlite3 import Connection
from typing import List

from app.routers.auth import get_current_user, get_db
from app.schemas import EndorsementCreate, EndorsementResponse, CertificateCreate, CertificateResponse

router = APIRouter()

# Endorsements

@router.get("/endorsements", response_model=List[EndorsementResponse])
async def list_endorsements(current_user = Depends(get_current_user), db: Connection = Depends(get_db)):
    """List endorsements for the current user."""
    rows = db.execute("SELECT * FROM endorsements WHERE user_id = ? ORDER BY date DESC", (current_user["id"],)).fetchall()
    return [dict(r) for r in rows]

@router.post("/endorsements", response_model=EndorsementResponse, status_code=201)
async def create_endorsement(endorsement: EndorsementCreate, current_user = Depends(get_current_user), db: Connection = Depends(get_db)):
    """Create a new endorsement. (Admins/Instructors should do this, but for now allow user/admin)."""
    # Authorization: only allow if user_id is current_user or current_user is admin
    if endorsement.user_id != current_user["id"] and not current_user["is_admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to create endorsement for another user")
    
    cursor = db.execute(
        "INSERT INTO endorsements (user_id, instructor_id, date, endorsement_type, text) VALUES (?, ?, ?, ?, ?)",
        (endorsement.user_id, endorsement.instructor_id, endorsement.date.isoformat(), endorsement.endorsement_type, endorsement.text)
    )
    db.commit()
    new_id = cursor.lastrowid
    row = db.execute("SELECT * FROM endorsements WHERE id = ?", (new_id,)).fetchone()
    return dict(row)

@router.delete("/endorsements/{endorsement_id}", status_code=204)
async def delete_endorsement(endorsement_id: int, current_user = Depends(get_current_user), db: Connection = Depends(get_db)):
    """Delete an endorsement (Admin only or owner of record)."""
    row = db.execute("SELECT * FROM endorsements WHERE id = ?", (endorsement_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Endorsement not found")
    
    if row["user_id"] != current_user["id"] and not current_user["is_admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    db.execute("DELETE FROM endorsements WHERE id = ?", (endorsement_id,))
    db.commit()

# Certificates

@router.get("/certificates", response_model=List[CertificateResponse])
async def list_certificates(current_user = Depends(get_current_user), db: Connection = Depends(get_db)):
    """List certificates for the current user."""
    rows = db.execute("SELECT * FROM certificates WHERE user_id = ? ORDER BY date_issued DESC", (current_user["id"],)).fetchall()
    return [dict(r) for r in rows]

@router.post("/certificates", response_model=CertificateResponse, status_code=201)
async def create_certificate(certificate: CertificateCreate, current_user = Depends(get_current_user), db: Connection = Depends(get_db)):
    """Create a new certificate for the current user."""
    cursor = db.execute(
        "INSERT INTO certificates (user_id, certificate_type, rating, date_issued, certificate_number) VALUES (?, ?, ?, ?, ?)",
        (current_user["id"], certificate.certificate_type, certificate.rating, certificate.date_issued.isoformat(), certificate.certificate_number)
    )
    db.commit()
    new_id = cursor.lastrowid
    row = db.execute("SELECT * FROM certificates WHERE id = ?", (new_id,)).fetchone()
    return dict(row)

@router.delete("/certificates/{certificate_id}", status_code=204)
async def delete_certificate(certificate_id: int, current_user = Depends(get_current_user), db: Connection = Depends(get_db)):
    """Delete a certificate."""
    row = db.execute("SELECT * FROM certificates WHERE id = ? AND user_id = ?", (certificate_id, current_user["id"])).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    db.execute("DELETE FROM certificates WHERE id = ?", (certificate_id,))
    db.commit()
