"""
DB module for handling database interactions.
"""
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from app.db.models import Base, User


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
        # TODO: Remove database initialization drop_all from instance
        # initialization
        # Drop all is useful in testing, but would delete impotant data
        # from production database table when initialized
        # Base.metadata.drop_all(self._engine)
        # Base.metadata.create_all(self._engine)
        
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
        """
        user = User(username=username, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user
    