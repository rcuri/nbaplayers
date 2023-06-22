from sqlalchemy import Column, Integer, Float, ForeignKey
from nbaplayers.database.base import Base
from sqlalchemy.orm import relationship
from nbaplayers.database.player import Player

class Stat(Base):
    """
    Our Book class
    """
    __tablename__ = 'stat'

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey(Player.player_id))
    player = relationship('Player', foreign_keys="Stat.player_id")
    
    field_goal_made = Column(Float(31), nullable=True)
    field_goal_attempted = Column(Float(31), nullable=True)
    field_goal_pct = Column(Float(21), nullable=True)
    three_pt_made = Column(Float(31), nullable=True)
    three_pt_attempted = Column(Float(31), nullable=True)
    three_pt_pct = Column(Float(21), nullable=True)
    free_throw_made = Column(Float(31), nullable=True)
    free_throw_attempted = Column(Float(31), nullable=True)
    free_throw_pct = Column(Float(21), nullable=True)
    points = Column(Float(21), nullable=True)
    off_reb = Column(Float(21), nullable=True)
    def_reb = Column(Float(21), nullable=True)
    tot_reb = Column(Float(21), nullable=True)
    assists = Column(Float(21), nullable=True)
    steals = Column(Float(21), nullable=True)
    blocks = Column(Float(21), nullable=True)
    turnovers = Column(Float(21), nullable=True)  
    personal_fouls = Column(Float(21), nullable=True)

    def __repr__(self):
        return "<Stat(id='%s')>" % (
            self.id)

    def __init__(self, data):
        self.from_dict(data)

    def from_dict(self, data):
        """
        When client passes a player representation as a dictionary in a
        request, parse it and convert it to a Player object.
        """
        for field in  Stat.__table__.columns.keys():
            if field != 'id' and field in data:
                setattr(self, field, data[field])