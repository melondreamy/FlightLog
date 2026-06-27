"""Pydantic schemas for SkyLog flight and user data."""

from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr


# Flight Schemas

class FlightCreate(BaseModel):
    """Schema for creating a new flight entry."""
    date: date
    aircraft_type: str = Field(..., min_length=1, max_length=50)
    aircraft_reg: str = Field(..., min_length=1, max_length=20)
    departure: str = Field(..., min_length=1, max_length=10)
    arrival: str = Field(..., min_length=1, max_length=10)
    departure_time: Optional[str] = None
    arrival_time: Optional[str] = None
    total_time: float = Field(..., gt=0)
    night_time: Optional[float] = Field(default=0, ge=0)
    pic_time: Optional[float] = Field(default=0, ge=0)
    sic_time: Optional[float] = Field(default=0, ge=0)
    dual_received: Optional[float] = Field(default=0, ge=0)
    dual_given: Optional[float] = Field(default=0, ge=0)
    actual_instrument: Optional[float] = Field(default=0, ge=0)
    sim_instrument: Optional[float] = Field(default=0, ge=0)
    approaches: Optional[int] = Field(default=0, ge=0)
    pilot_in_command: str = Field(..., min_length=1, max_length=100)
    remarks: Optional[str] = None
    landings_day: Optional[int] = Field(default=0, ge=0)
    landings_night: Optional[int] = Field(default=0, ge=0)
    cross_country: Optional[bool] = Field(default=False)
    custom_fields: Optional[str] = None


class FlightUpdate(BaseModel):
    """Schema for updating an existing flight entry (all fields optional)."""
    date: Optional[date] = None
    aircraft_type: Optional[str] = Field(default=None, min_length=1, max_length=50)
    aircraft_reg: Optional[str] = Field(default=None, min_length=1, max_length=20)
    departure: Optional[str] = Field(default=None, min_length=1, max_length=10)
    arrival: Optional[str] = Field(default=None, min_length=1, max_length=10)
    departure_time: Optional[str] = None
    arrival_time: Optional[str] = None
    total_time: Optional[float] = Field(default=None, gt=0)
    night_time: Optional[float] = Field(default=None, ge=0)
    pic_time: Optional[float] = Field(default=None, ge=0)
    sic_time: Optional[float] = Field(default=None, ge=0)
    dual_received: Optional[float] = Field(default=None, ge=0)
    dual_given: Optional[float] = Field(default=None, ge=0)
    actual_instrument: Optional[float] = Field(default=None, ge=0)
    sim_instrument: Optional[float] = Field(default=None, ge=0)
    approaches: Optional[int] = Field(default=None, ge=0)
    pilot_in_command: Optional[str] = Field(default=None, min_length=1, max_length=100)
    remarks: Optional[str] = None
    landings_day: Optional[int] = Field(default=None, ge=0)
    landings_night: Optional[int] = Field(default=None, ge=0)
    cross_country: Optional[bool] = None
    custom_fields: Optional[str] = None


class FlightResponse(BaseModel):
    """Schema for returning flight data."""
    id: int
    date: str
    aircraft_type: str
    aircraft_reg: str
    departure: str
    arrival: str
    departure_time: Optional[str] = None
    arrival_time: Optional[str] = None
    total_time: float
    night_time: float = 0
    pic_time: float = 0
    sic_time: float = 0
    dual_received: float = 0
    dual_given: float = 0
    actual_instrument: float = 0
    sim_instrument: float = 0
    approaches: int = 0
    pilot_in_command: str
    remarks: Optional[str] = None
    landings_day: int = 0
    landings_night: int = 0
    cross_country: bool = False
    user_id: Optional[int] = None
    custom_fields: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    """Schema for dashboard statistics."""
    total_flights: int
    total_hours: float
    total_night_hours: float
    total_pic_hours: float
    total_sic_hours: float
    total_instrument_hours: float
    hours_last_30_days: float
    total_landings: int
    total_approaches: int
    unique_aircraft: int


# User Schemas

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    id: int
    is_admin: bool
    created_at: str
    settings: Optional[str] = None

    class Config:
        from_attributes = True


class UserMeResponse(UserResponse):
    show_welcome: bool = True
    setup_complete: bool = False


class WelcomeConfig(BaseModel):
    title: str
    description: str
    features: List[str]
    background_style: str = "default"


class PasswordReset(BaseModel):
    new_password: str = Field(..., min_length=8)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


# Endorsement Schemas

class EndorsementBase(BaseModel):
    date: date
    endorsement_type: str = Field(..., min_length=1, max_length=100)
    text: str = Field(..., min_length=1)
    instructor_id: Optional[int] = None


class EndorsementCreate(EndorsementBase):
    user_id: int


class EndorsementResponse(EndorsementBase):
    id: int
    user_id: int
    created_at: str

    class Config:
        from_attributes = True


# Certificate Schemas

class CertificateBase(BaseModel):
    certificate_type: str = Field(..., min_length=1, max_length=100)
    rating: str = Field(..., min_length=1, max_length=100)
    date_issued: date
    certificate_number: Optional[str] = None


class CertificateCreate(CertificateBase):
    pass


class CertificateResponse(CertificateBase):
    id: int
    user_id: int
    date_issued: str
    created_at: str

    class Config:
        from_attributes = True
