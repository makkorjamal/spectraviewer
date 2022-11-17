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


def Create_SPYear(year):
    spYear = SPYear(name=year)
    session.add(spYear)
    session.commit()

def Add_Spectrum(year, name, date, filename):
    spYear = session.query(SPYear).filter_by(name=year).one()
    additem = Spectrum(
        name=name,
        filename=filename,
        date=date,
        year_id=spYear.id)
    session.add(additem)
    session.commit()

def filldb(sp_path):
    file_path = os.path.join(sp_path)

    sp_files = glob(file_path + '*.dat')
    Create_SPYear('1950')
    Create_SPYear('1951')
    for sp_file in zip(sp_files):
        sp_file = sp_file[0]
        date =datetime.strptime(sp_file.split('_')[1], '%d%m%Y%H%M%S%f')
        str_date = datetime.strftime(date,'%d/%m/%y %H:%M')
        year =datetime.strptime(sp_file.split('_')[1], '%d%m%Y%H%M%S%f').year 
        if year == 1950:
            Add_Spectrum(year,sp_file.split('_')[1], str_date, sp_file)
        if year == 1951:
            Add_Spectrum(year,sp_file.split('_')[1],str_date, sp_file)

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
            print ("Date", item.date)
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
            lst_c.append( c.date)
        myDict[key] = lst_c
    return myDict
def FindFilname(sp_date):
    item = session.query(Spectrum).filter_by(date=sp_date).one()
    return item.id, item.name,item.date, item.filename

if __name__ == '__main__':
    print('ELLO')

    filldb('data/')


