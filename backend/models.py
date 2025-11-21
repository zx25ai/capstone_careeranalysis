from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Association table: Users ↔ Skills
user_skills = Table(
    "user_skills",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("skill_id", Integer, ForeignKey("skills.id")),
)

# Association table: Job Roles ↔ Skills
jobrole_skills = Table(
    "jobrole_skills",
    Base.metadata,
    Column("jobrole_id", Integer, ForeignKey("job_roles.id")),
    Column("skill_id", Integer, ForeignKey("skills.id")),
)


# ==============================
# MAIN TABLES
# ==============================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    education = Column(String)
    coursework = Column(String)  # JSON string or comma separated list

    skills = relationship(
        "Skill",
        secondary=user_skills,
        back_populates="users"
    )


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship(
        "User",
        secondary=user_skills,
        back_populates="skills"
    )

    job_roles = relationship(
        "JobRole",
        secondary=jobrole_skills,
        back_populates="skills"
    )


class JobRole(Base):
    __tablename__ = "job_roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    skills = relationship(
        "Skill",
        secondary=jobrole_skills,
        back_populates="job_roles"
    )
