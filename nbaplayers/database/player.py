from sqlalchemy import Column, Integer, String, SmallInteger, Index
from nbaplayers.database.base import Base
from sqlalchemy.sql import func
from sqlalchemy import cast, literal
from sqlalchemy.dialects.postgresql import REGCONFIG


class Player(Base):
    """
    Our Book class
    """
    __tablename__ = 'player'

    player_id = Column(Integer, primary_key=True, index=True, nullable=False)
    player_name = Column(String, index=True)
    position = Column(String(100))
    first_nba_season = Column(SmallInteger)  
    last_nba_season = Column(SmallInteger, nullable=True)
    height = Column(String(100))
    weight = Column(String(100))
    __table_args__ = (
        Index(
            'ix_player_tsv',
            func.to_tsvector(cast(literal("english"), type_=REGCONFIG), player_name),
            postgresql_using='gin'
            ),
        )

    def __repr__(self):
        return "<Player(id='%s', name='%s')>" % (
            self.id, self.name)

    def __init__(self, data):
        self.from_dict(data)

    def from_dict(self, data):
        """
        When client passes a player representation as a dictionary in a
        request, parse it and convert it to a Player object.
        """
        for field in  Player.__table__.columns.keys():
            if field != 'id' and field in data:
                setattr(self, field, data[field])        