from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import TypeVar, Generic, Type, Optional, List, Any
from pathlib import Path
import os

T = TypeVar('T')

class Database:
    def __init__(self, connection_string: str | None = None):
        """Initialize database connection.
        
        Args:
            connection_string (str, optional): Database connection string. If not provided,
                                             will use SQLite with default configuration.
        """
        if connection_string is None:
            # Get the project root directory
            root_dir = Path(__file__).parent.parent.parent
            # Ensure data directory exists
            os.makedirs(root_dir / "data", exist_ok=True)
            # Use SQLite by default
            connection_string = f"sqlite:///{root_dir}/data/chatbot.db"

        self.engine = create_engine(
            connection_string,
            # SQLite specific configurations
            connect_args={"check_same_thread": False} if "sqlite" in connection_string else {}
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

    def get_session(self) -> Session:
        """Get a new database session.
        
        Returns:
            Session: SQLAlchemy session
        """
        return self.SessionLocal()

    def create_all(self):
        """Create all tables in the database."""
        self.Base.metadata.create_all(bind=self.engine)

    def add(self, session: Session, item: Any) -> Any:
        """Add an item to the database.
        
        Args:
            session (Session): Database session
            item (Any): Item to add
            
        Returns:
            Any: Added item
        """
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

    def get(self, session: Session, model: Type[T], id: Any) -> Optional[T]:
        """Get an item by ID.
        
        Args:
            session (Session): Database session
            model (Type[T]): Model class
            id (Any): Item ID
            
        Returns:
            Optional[T]: Found item or None
        """
        return session.query(model).filter(model.id == id).first()

    def get_all(self, session: Session, model: Type[T]) -> List[T]:
        """Get all items of a model.
        
        Args:
            session (Session): Database session
            model (Type[T]): Model class
            
        Returns:
            List[T]: List of items
        """
        return session.query(model).all()

    def update(self, session: Session, item: Any) -> Any:
        """Update an item.
        
        Args:
            session (Session): Database session
            item (Any): Item to update
            
        Returns:
            Any: Updated item
        """
        session.commit()
        session.refresh(item)
        return item

    def delete(self, session: Session, item: Any):
        """Delete an item.
        
        Args:
            session (Session): Database session
            item (Any): Item to delete
        """
        session.delete(item)
        session.commit()
