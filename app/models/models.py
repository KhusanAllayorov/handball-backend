from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)     # login uchun (bcrypt)
    password_plain = Column(String, nullable=True)     # ochiq parol (nazorat uchun)

    # Rol ma'lumotlari (Flutter UserRole bilan mos)
    role_name = Column(String, nullable=False)          # "Murabbiy", "Defektolog", ...
    mode = Column(String, nullable=False, default="specialist")  # specialist | parent | student
    clinical = Column(Boolean, default=False)
    emoji = Column(String, default="🧑‍🏫")
    role_description = Column(String, default="")

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    children = relationship("Child", back_populates="specialist", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="specialist", cascade="all, delete-orphan")


class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    color_hex = Column(String, default="#FF6B35")   # AppColors.primary
    percentile = Column(String, default="—")
    pre_score = Column(Integer, default=0)
    post_score = Column(Integer, default=0)

    specialist_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    specialist = relationship("User", back_populates="children")

    assessments = relationship("Assessment", back_populates="child", cascade="all, delete-orphan")


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    child_name = Column(String, nullable=False)
    age_years = Column(Integer, default=9)
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # 8 ta item standart balli (1–19)
    placing_pegs = Column(Integer, default=10)        # MD1
    threading_lace = Column(Integer, default=10)      # MD2
    drawing_trail = Column(Integer, default=10)       # MD3
    catching = Column(Integer, default=10)            # AC1
    throwing = Column(Integer, default=10)            # AC2
    one_board_balance = Column(Integer, default=10)   # Bal1
    walking_heel_toe = Column(Integer, default=10)    # Bal2
    hopping_mats = Column(Integer, default=10)        # Bal3

    # Hisoblangan natijalar (Flutter tomonidan yuboriladi)
    total_raw = Column(Integer, default=80)
    total_standard_score = Column(Integer, default=10)
    total_percentile = Column(Float, default=50.0)
    zone = Column(String, default="green")            # red | amber | green

    specialist_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    specialist = relationship("User", back_populates="assessments")

    child_id = Column(Integer, ForeignKey("children.id"), nullable=True)
    child = relationship("Child", back_populates="assessments")
