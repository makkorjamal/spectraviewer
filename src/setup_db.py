from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class SPYear(Base):
    __tablename__ = 'spyear'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
 
class Spectrum(Base):
    __tablename__ = 'spectrum'


    name =Column(String(80), nullable = False)
    date =Column(String(120), nullable = False)
    id = Column(Integer, primary_key = True)
    sp_filename = Column(String(250))
    dg_filename = Column(String(250))
    im_filename = Column(String(250))
    im_height = Column(Integer)
    year_id = Column(Integer,ForeignKey('spyear.id'))
    spyear = relationship(SPYear) 