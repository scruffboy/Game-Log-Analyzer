from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from config import DB_PATH
from typing import List


engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class LogModel(Base):
    """Table model for storing the history of player actions"""

    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    identification = Column(Boolean)
    action = Column(String)
    player_id = Column(String)
    data = Column(JSON)


# Create table
Base.metadata.create_all(bind=engine)


def save_logs_to_db(entries_list: List):
    """Function for bulk saving of log entries to the database"""
    session = SessionLocal()
    try:
        for entry in entries_list:
            new_entry = LogModel(
                timestamp=entry.timestamp,
                identification=entry.identification,
                action=entry.action,
                player_id=entry.player_id,
                data=entry.data,
            )
            session.add(new_entry)
        session.commit()
        print(f"[Success] Logs saved: {len(entries_list)}")
    except Exception as e:
        session.rollback()
        print(f"[Warning] Failed to save logs: {str(e)}")
    finally:
        session.close()
