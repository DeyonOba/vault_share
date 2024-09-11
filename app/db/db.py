"""
DB module for handling database interactions.
"""
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from app.db.models import Base, User


class DB:
    """
    DB class
    """
    
    def __init__(self, database="app.db") -> None:
        url_object = URL.create("sqlite", database=database)
        self._engine = create_engine(url_object, echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None
        
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
    