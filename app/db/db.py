"""
DB module for handling database interactions.
"""
from app.db.models import Base, User
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError


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
        self._engine = create_engine(url_object, echo=echo)
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
    
    def add_user(self, username: str, hashed_password: str) -> User:
        """
        Add user details to database.
        
        Args:
            username (str): The username of the user.
            hashed_password (str): The hashed password of the user.
            
        Returns:
            User: The created User object.
        """
        try:
            user = User(username=username, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
            return user
        except SQLAlchemyError as e:
            self._session.rollback()
            # TODO: Error would be logged using custom logger
            print(f"Error adding user: {e}")
            return None
        finally:
            self._close_session()
        
    def _close_session(self):
        """Closes the active session to prevent memory leaks."""
        if self.__session:
            self.__session.close()
            self.__session = None
