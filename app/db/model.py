from sqlalchemy import (
    Column,
    Float,
    Integer,
    String,
    ForeignKey,
    DateTime,
    ARRAY,
    func,
)
from . import Base


class Hospital(Base):
    __tablename__ = "hospital"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    location = Column(String, nullable=False)
    coordinates = Column(ARRAY(Float), nullable=False)


class Admin(Base):
    __tablename__ = "admin"

    hospital_id = Column(Integer, ForeignKey("hospital.id"), nullable=False)
    id = Column(String, primary_key=True)
    password = Column(String, nullable=False)

    # Relationship
    # hospital = relationship("Hospital", back_populates="admins")


class Patient(Base):
    __tablename__ = "patient"

    id = Column(String, primary_key=True)
    hospital_id = Column(Integer, ForeignKey("hospital.id"), nullable=False)
    name = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    birth_year = Column(Integer, nullable=True)
    birth_month = Column(Integer, nullable=True)
    birth_day = Column(Integer, nullable=True)
    diagnosis = Column(String, nullable=True)
    severity = Column(String, nullable=True)
    eta_hour = Column(Integer, nullable=True)
    eta_min = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relationship
    # hospital = relationship("Hospital", back_populates="patients")


class Bed(Base):
    __tablename__ = "hospital_bed"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hospital_id = Column(Integer, ForeignKey("hospital.id"), nullable=False)
    patient_id = Column(String, ForeignKey("patient.id"), nullable=False)

    # Relationships
    # hospital = relationship("Hospital", back_populates="beds")
    # patient = relationship("Patient", back_populates="bed")
