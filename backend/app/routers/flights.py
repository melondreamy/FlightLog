"""Flight CRUD API routes."""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from sqlite3 import Connection

from app.database import get_connection
from app.schemas import FlightCreate, FlightUpdate, FlightResponse, DashboardStats
from app.routers.auth import get_current_user, get_db

router = APIRouter()


def row_to_flight_response(row) -> dict:
    """Convert a sqlite3.Row to a dict for FlightResponse."""
    return {
        "id": row["id"],
        "date": row["date"],
        "aircraft_type": row["aircraft_type"],
        "aircraft_reg": row["aircraft_reg"],
        "departure": row["departure"],
        "arrival": row["arrival"],
        "departure_time": row["departure_time"],
        "arrival_time": row["arrival_time"],
        "total_time": row["total_time"],
        "night_time": row["night_time"],
        "pic_time": row["pic_time"],
        "sic_time": row["sic_time"],
        "dual_received": row["dual_received"],
        "dual_given": row["dual_given"],
        "actual_instrument": row["actual_instrument"],
        "sim_instrument": row["sim_instrument"],
        "approaches": row["approaches"],
        "pilot_in_command": row["pilot_in_command"],
        "remarks": row["remarks"],
        "landings_day": row["landings_day"],
        "landings_night": row["landings_night"],
        "cross_country": bool(row["cross_country"]),
        "user_id": row["user_id"],
        "custom_fields": row["custom_fields"],
        "created_at": row["created_at"],
    }


@router.get("/flights", response_model=List[FlightResponse])
async def list_flights(current_user = Depends(get_current_user), db: Connection = Depends(get_db)):
    """Get all flight entries for the current user, ordered by date descending."""
    rows = db.execute(
        "SELECT * FROM flights WHERE user_id = ? ORDER BY date DESC, id DESC", 
        (current_user["id"],)
    ).fetchall()
    return [row_to_flight_response(r) for r in rows]


@router.get("/flights/{flight_id}", response_model=FlightResponse)
async def get_flight(flight_id: int, current_user = Depends(get_current_user), db: Connection = Depends(get_db)):
    """Get a single flight entry by ID."""
    row = db.execute(
        "SELECT * FROM flights WHERE id = ? AND user_id = ?", 
        (flight_id, current_user["id"])
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Flight not found")
    return row_to_flight_response(row)


@router.post("/flights", response_model=FlightResponse, status_code=201)
async def create_flight(flight: FlightCreate, current_user = Depends(get_current_user), db: Connection = Depends(get_db)):
    """Create a new flight entry."""
    cursor = db.execute(
        """INSERT INTO flights 
            (date, aircraft_type, aircraft_reg, departure, arrival, 
            departure_time, arrival_time, total_time, night_time,
            pic_time, sic_time, dual_received, dual_given,
            actual_instrument, sim_instrument, approaches,
            pilot_in_command, remarks, landings_day, landings_night, 
            cross_country, user_id, custom_fields)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            flight.date.isoformat(),
            flight.aircraft_type,
            flight.aircraft_reg,
            flight.departure,
            flight.arrival,
            flight.departure_time,
            flight.arrival_time,
            flight.total_time,
            flight.night_time or 0,
            flight.pic_time or 0,
            flight.sic_time or 0,
            flight.dual_received or 0,
            flight.dual_given or 0,
            flight.actual_instrument or 0,
            flight.sim_instrument or 0,
            flight.approaches or 0,
            flight.pilot_in_command,
            flight.remarks,
            flight.landings_day or 0,
            flight.landings_night or 0,
            1 if flight.cross_country else 0,
            current_user["id"],
            flight.custom_fields
        ),
    )
    db.commit()
    flight_id = cursor.lastrowid
    row = db.execute(
        "SELECT * FROM flights WHERE id = ?", (flight_id,)
    ).fetchone()
    return row_to_flight_response(row)


@router.put("/flights/{flight_id}", response_model=FlightResponse)
async def update_flight(flight_id: int, flight: FlightUpdate, current_user = Depends(get_current_user), db: Connection = Depends(get_db)):
    """Update an existing flight entry."""
    # Check flight exists and belongs to user
    existing = db.execute(
        "SELECT * FROM flights WHERE id = ? AND user_id = ?", 
        (flight_id, current_user["id"])
    ).fetchone()
    if not existing:
        raise HTTPException(status_code=404, detail="Flight not found")

    # Build update fields dynamically (only non-None fields)
    updates = {}
    if flight.date is not None:
        updates["date"] = flight.date.isoformat()
    if flight.aircraft_type is not None:
        updates["aircraft_type"] = flight.aircraft_type
    if flight.aircraft_reg is not None:
        updates["aircraft_reg"] = flight.aircraft_reg
    if flight.departure is not None:
        updates["departure"] = flight.departure
    if flight.arrival is not None:
        updates["arrival"] = flight.arrival
    if flight.departure_time is not None:
        updates["departure_time"] = flight.departure_time
    if flight.arrival_time is not None:
        updates["arrival_time"] = flight.arrival_time
    if flight.total_time is not None:
        updates["total_time"] = flight.total_time
    if flight.night_time is not None:
        updates["night_time"] = flight.night_time
    if flight.pic_time is not None:
        updates["pic_time"] = flight.pic_time
    if flight.sic_time is not None:
        updates["sic_time"] = flight.sic_time
    if flight.dual_received is not None:
        updates["dual_received"] = flight.dual_received
    if flight.dual_given is not None:
        updates["dual_given"] = flight.dual_given
    if flight.actual_instrument is not None:
        updates["actual_instrument"] = flight.actual_instrument
    if flight.sim_instrument is not None:
        updates["sim_instrument"] = flight.sim_instrument
    if flight.approaches is not None:
        updates["approaches"] = flight.approaches
    if flight.pilot_in_command is not None:
        updates["pilot_in_command"] = flight.pilot_in_command
    if flight.remarks is not None:
        updates["remarks"] = flight.remarks
    if flight.landings_day is not None:
        updates["landings_day"] = flight.landings_day
    if flight.landings_night is not None:
        updates["landings_night"] = flight.landings_night
    if flight.cross_country is not None:
        updates["cross_country"] = 1 if flight.cross_country else 0
    if flight.custom_fields is not None:
        updates["custom_fields"] = flight.custom_fields

    if not updates:
        return row_to_flight_response(existing)

    set_clause = ", ".join(f"{k} = ?" for k in updates)
    values = list(updates.values())
    values.append(flight_id)
    values.append(current_user["id"])

    db.execute(
        f"UPDATE flights SET {set_clause} WHERE id = ? AND user_id = ?", values
    )
    db.commit()

    row = db.execute(
        "SELECT * FROM flights WHERE id = ?", (flight_id,)
    ).fetchone()
    return row_to_flight_response(row)


@router.delete("/flights/{flight_id}", status_code=204)
async def delete_flight(flight_id: int, current_user = Depends(get_current_user), db: Connection = Depends(get_db)):
    """Delete a flight entry."""
    cursor = db.execute(
        "DELETE FROM flights WHERE id = ? AND user_id = ?", 
        (flight_id, current_user["id"])
    )
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Flight not found")


@router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(current_user = Depends(get_current_user), db: Connection = Depends(get_db)):
    """Get aggregated dashboard statistics for the current user."""
    uid = current_user["id"]
    
    total_flights = db.execute(
        "SELECT COUNT(*) FROM flights WHERE user_id = ?", (uid,)
    ).fetchone()[0]

    total_hours = db.execute(
        "SELECT COALESCE(SUM(total_time), 0) FROM flights WHERE user_id = ?", (uid,)
    ).fetchone()[0]

    total_night_hours = db.execute(
        "SELECT COALESCE(SUM(night_time), 0) FROM flights WHERE user_id = ?", (uid,)
    ).fetchone()[0]

    total_pic_hours = db.execute(
        "SELECT COALESCE(SUM(pic_time), 0) FROM flights WHERE user_id = ?", (uid,)
    ).fetchone()[0]

    total_sic_hours = db.execute(
        "SELECT COALESCE(SUM(sic_time), 0) FROM flights WHERE user_id = ?", (uid,)
    ).fetchone()[0]

    total_instrument_hours = db.execute(
        "SELECT COALESCE(SUM(actual_instrument + sim_instrument), 0) FROM flights WHERE user_id = ?", (uid,)
    ).fetchone()[0]

    hours_last_30_days = db.execute(
        """SELECT COALESCE(SUM(total_time), 0) FROM flights 
            WHERE user_id = ? AND date >= date('now', '-30 days')""", (uid,)
    ).fetchone()[0]

    total_landings = db.execute(
        "SELECT COALESCE(SUM(landings_day + landings_night), 0) FROM flights WHERE user_id = ?", (uid,)
    ).fetchone()[0]

    total_approaches = db.execute(
        "SELECT COALESCE(SUM(approaches), 0) FROM flights WHERE user_id = ?", (uid,)
    ).fetchone()[0]

    unique_aircraft = db.execute(
        "SELECT COUNT(DISTINCT aircraft_reg) FROM flights WHERE user_id = ?", (uid,)
    ).fetchone()[0]

    return DashboardStats(
        total_flights=total_flights,
        total_hours=round(total_hours, 2),
        total_night_hours=round(total_night_hours, 2),
        total_pic_hours=round(total_pic_hours, 2),
        total_sic_hours=round(total_sic_hours, 2),
        total_instrument_hours=round(total_instrument_hours, 2),
        hours_last_30_days=round(hours_last_30_days, 2),
        total_landings=total_landings,
        total_approaches=total_approaches,
        unique_aircraft=unique_aircraft,
    )
