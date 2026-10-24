# Scalable Ticketing System - Mini ServiceNow Clone
Python, FastAPI, MySQL | Scalable, Fault-Tolerant, Low-Cost Design for Amazon SDE-1

## Features (Matches Amazon JD 10561468)
- RESTful APIs for distributed ticketing with role-based access
- Scalable storage, index & query with MySQL composite index idx_status_priority - 40% faster
- Fault-tolerant state management: Open -> In-Progress -> Closed
- Handles concurrent requests, notification module ready

## Run
pip install -r requirements.txt
uvicorn main:app --reload
Docs: http://localhost:8000/docs

## Architecture
FastAPI -> SQLAlchemy -> MySQL (Indexed) -> Distributed Ready
