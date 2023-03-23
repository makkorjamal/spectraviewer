import sqlalchemy as db
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
    """ 
    Create a Spectra year
    you need to provide a year. Example Create_SPYear(1951)
    """
    spYear = SPYear(name=year)
    session.add(spYear)
    session.commit()

def Add_Spectrum(year, name, date, filename):
    """
    Each year contains multiple measurements (Spectra)
    Each spectrum in the the database need to be initialised
    Provide name, filename where the spectrum is stored etc.
    """
    #TODO add more metadate to the database
    spYear = session.query(SPYear).filter_by(name=year).one()
    additem = Spectrum(
        name=name,
        filename=filename,
        date=date,
        year_id=spYear.id)
    session.add(additem)
    session.commit()

def filldb(sp_path):
    """
    This function reads the spectra files and fill the database
    The tables 1950/51 are filled here
    """
    #file_path = os.path.join(sp_path)

    sp_files = glob(f"{sp_path}" + "/*.dat")
    print(sp_files)
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
    """
    This ones fetches the items from all tables in the database.
    """
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
    """
    This function fetches only spectra that belong to the same year
    This is useful to publich the dropdown menu in the web gui
    """
    spyears = session.query(SPYear).all()
    spDict = {}
    for spyr in spyears:
    
        key = spyr.name
        year_id = spyr.id

        spec = session.query(Spectrum).filter_by(year_id=year_id).all()
        lst_sp = []
        for sp in spec:
            lst_sp.append( sp.date)
        spDict[key] = lst_sp
    return spDict
def FindFilname(sp_date):
    item = session.query(Spectrum).filter_by(date=sp_date).one()
    return item.id, item.name,item.date, item.filename

if __name__ == '__main__':
    print('ELLO')
    panth = os.path.join('static','data')
    print(panth)
    #filldb(os.path.join('static','data'))
    filldb(panth)


