from flask_login import UserMixin
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    lastname = Column(String(150), nullable=False, index=True)
    firstname = Column(String(150), nullable=False, index=True)
    email = Column(String(150), nullable=False, index=True, unique=True)
    password = Column(String(200), nullable=False)

    clients = relationship("Client", back_populates="user", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    lastname = Column(String(150), nullable=False, index=True)
    firstname = Column(String(150), nullable=False, index=True)
    enterprise = Column(String(150), index=True)
    address = Column(String(250))
    zip_code = Column(String(20), index=True)
    city = Column(String(150))
    country = Column(String(150))
    phone_number = Column(String(20), index=True)
    email = Column(String(150), index=True)
    note = Column(Text)

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="clients")

    projects = relationship("Project", back_populates="client", cascade="all, delete-orphan")

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    name_project = Column(String(150), nullable=False, index=True)
    description = Column(Text)
    url = Column(String(250))
    hosting_server = Column(String(150))
    status = Column(String(50))
    
    hourly_rate = Column(Float, default=0.0, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))

    user = relationship("User", back_populates="projects")
    client = relationship("Client", back_populates="projects")

    tasks = relationship("Task", back_populates="projects", cascade="all, delete-orphan")

    @property
    def total_time(self):
        return sum(task.time_spent for task in self.tasks)
    
    @property
    def total_cost(self):
        return self.total_time * self.hourly_rate
    
class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    name_task = Column(String(150), nullable=False, index=True)
    status = Column(String(50))
    time_spent = Column(Float, default=0.0, nullable=False)
    
    project_id = Column(Integer, ForeignKey("projects.id"))

    projects = relationship("Project", back_populates="tasks")