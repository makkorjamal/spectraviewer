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
def FetchAll(fetch_yr = False, fetch_sp = False):
    if fetch_yr:
        items = session.query(SPYear).all()
        for item in items:
            print ("ID:", item.id)
            print ("SPName:", item.name)
        return items

    if fetch_sp:
        items = session.query(Spectrum).all()
        for item in items:
            print ("Item ID:", item.id)
            print ("Name:", item.name)
            print ("Filename", item.filename)
            print ("Year Id", item.year_id)
        return items
def FetchSameYear():
    spyears = session.query(SPYear).all()
    myDict = {}
    for p in spyears:
    
        key = p.name
        year_id = p.id

        # Select all car models that belong to a car brand
        q = session.query(Spectrum).filter_by(year_id=year_id).all()
    
        # build the structure (lst_c) that includes the names of the car models that belong to the car brand
        lst_c = []
        for c in q:
            lst_c.append( c.name)
        myDict[key] = lst_c
    return myDict

if __name__ == '__main__':
    print('ELLO')
    #Create_SPYear('1950')
    #Add_Spectrum('1950', 'jfj1950', 'jfj1950.dat')
    #FetchAll(False, True)
    print(FetchSameYear())


