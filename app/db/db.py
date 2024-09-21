"""
DB module for handling database interactions.
"""
from app.db.models import Base, User, Workspace
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import (
    SQLAlchemyError,
    NoResultFound,
    InvalidRequestError,
    )
from sqlite3 import IntegrityError


class DB:
    """
    DB class provides methods for database interaction.
    
    Attributes:
        _engine: SQLAlchemy engine object for database connection.
        __session: Memoized session object for database transactions.
    """
    
    def __init__(
        self, database_url: str = "sqlite:///app.db", echo: bool = False
    ) -> None:
        """
        Initializes the DB class with a database connection.
        
        Args:
            database_url (str): The database connection URL. Defaults to
            "sqlite:///app.db"
            echo (bool): If True, SQLAlchemy logs all SQL statements.
            Defaults to False.
        """
        self._engine = create_engine(database_url, echo=echo)
        self.__session = None
        self._initialize_database()
        
    def _initialize_database(self):
        """
        Initializes the database schema by creating all tables.
        
        In other to avoid overwritting production data this should be used
        cautiously during testing. During testing production database should be
        changed, or in memory database ":memory:" should be used.
        """
        try:
            Base.metadata.create_all(self._engine)
        except SQLAlchemyError as e:
            # TODO: Error would be logged in using a custom logger
            # Also full exception would be logged
            print(f"Error initializing database schema: {e}")
        
    @property
    def _session(self) -> Session:
        """
        Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session
    
    def close_session(self):
        """Closes the active session to prevent memory leaks."""
        if self.__session:
            self.__session.close()
            self.__session = None
    
    def delete_tables(self):
        """Drops all tables from Base class metadata."""
        try:
            Base.metadata.drop_all(self._engine)
        except SQLAlchemyError as e:
            # TODO: Error would be logged using custom logger
            print(f"Error dropping tables for database schema: {e}")

    def create(self, model, **kwargs):
        """
        Add table details to database.
        
        Args:
            model: Valid table schema class from db.models
            kwargs: Argument needed to create the a table entry.
            
        Returns:
            Object: The created table object instance of the validate entry.
        """
        obj = model(**kwargs)
        self._session.add(obj)
        self._session.commit()
        return obj
    
    def retrieve(self, model, **kwargs) -> User:
        """
        Retrieves an entry for the specified model passed.
        
        Args:
            model: Valid table schema class from db.models
            kwargs: Filter cirteron
            
        Returns:
            obj: The retrieved entry found
        
        Raises:
            NoResultFound: When no entry satisfies the filter cirteron
        """
        obj = self._session.query(model).filter_by(**kwargs).first()
        
        if not obj:
            raise NoResultFound
        
        return obj
    
    def update(self, model, update_filter: dict, **kwargs) -> int:
        """
        Filters records using the update_filter and then update the records based on
        keyword paramater passed.
        
        Args:
            model: Valid table schema class from db.models
            update_filter (dict): Dictionary containing the parameter and argument used
            to filter out the entry to be updated
            **kwargs: Update cirteron
        Returns:
            num_of_updates (int): Number of records updated
        """
        num_of_updates = self._session.query(model).filter_by(**update_filter).update(kwargs)
        self._session.commit()
        return num_of_updates

    def delete(self, model, delete_filter: dict) -> int:
        """
        Filters records to be deleted using `delete_filter`, then delete filtered records.
        
        Args:
            model: Valid table schema class from db.models
            delete_filter (dict): Dictionary
        
        Returns:
            num_of_deletes: Number of records deleted
        """
        num_of_deletes = self._session.query(model).filter_by(**delete_filter).delete()
        return num_of_deletes
