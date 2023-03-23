import os
import sys
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
    filename = Column(String(250))
    year_id = Column(Integer,ForeignKey('spyear.id'))
    spyear = relationship(SPYear) 

    @property
    def serialize(self):
       
       return {
           'name'         : self.name,
           'filename'         : self.filename,
           'id'         : self.id,
       }
 