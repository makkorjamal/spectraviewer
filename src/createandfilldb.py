import sqlalchemy as db
import pandas as pd
from glob import glob
import os
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from setup_db import Base, SPYear, Spectrum
from sqlalchemy.sql import text
engine = db.create_engine('sqlite:///spectra.db')
Base.metadata.create_all(engine)
connection = engine.connect()
DBSession = sessionmaker(bind=engine)
session = DBSession()

def readfiles(sp_path):
    file_path = os.path.join(sp_path)
    sp_files = glob(file_path + '*.dat')
    years = [datetime.strptime(file.split('_')[1], '%d%m%Y%H%M%S%f') for file in sp_files]
    sp_dic = [{'year': yr.year, 'filename':fn} for yr, fn in zip(years, sp_files)]   
    return sp_dic
def Create_SPYear(year):
    spYear = SPYear(name=year)
    session.add(spYear)
    session.commit()
def Add_Spectrum(year, name, filename):
    spYear = session.query(SPYear).filter_by(name=year).one()
    additem = Spectrum(
        name=name,
        filename=filename,
        year_id=spYear.id)
    session.add(additem)
    session.commit()    

if __name__ == '__main__':
    print('ELLO')
    Create_SPYear('1951')
    Add_Spectrum('1951', 'jfj1951', 'jfj1951.dat')

