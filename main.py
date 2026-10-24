from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Enum, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import enum

DATABASE_URL = "sqlite:///./tickets.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class TicketStatus(str, enum.Enum):
    open = "Open"
    in_progress = "In-Progress"
    closed = "Closed"

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String(1000))
    status = Column(Enum(TicketStatus), default=TicketStatus.open)
    priority = Column(String(20), index=True)
    __table_args__ = (Index('idx_status_priority', 'status', 'priority'),)

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Scalable Ticketing System - Mini ServiceNow Clone")

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@app.post("/tickets/")
def create_ticket(title: str, description: str, priority: str = "Medium", db: Session = Depends(get_db)):
    ticket = Ticket(title=title, description=description, priority=priority)
    db.add(ticket); db.commit(); db.refresh(ticket)
    return ticket

@app.get("/tickets/")
def list_tickets(status: TicketStatus = None, priority: str = None, db: Session = Depends(get_db)):
    query = db.query(Ticket)
    if status: query = query.filter(Ticket.status == status)
    if priority: query = query.filter(Ticket.priority == priority)
    return query.all()

@app.put("/tickets/{ticket_id}/status")
def update_status(ticket_id: int, new_status: TicketStatus, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket: raise HTTPException(status_code=404, detail="Not found")
    valid = {"Open": ["In-Progress"], "In-Progress": ["Closed", "Open"], "Closed": []}
    if new_status.value not in valid.get(ticket.status.value, []):
        raise HTTPException(status_code=400, detail=f"Invalid {ticket.status} -> {new_status}")
    ticket.status = new_status; db.commit(); return ticket

@app.get("/")
def health():
    return {"status": "Running", "features": "Scalable storage, indexed queries, fault-tolerant state"}
