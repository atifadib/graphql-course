from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, Employer, Job
from settings.config import DB_URL

engine = create_engine(DB_URL)
Session = sessionmaker(engine)

def prepare_database():
    # Code Block for Adding data --> Do not uncommit
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session_obj = Session()
    
    emp = Employer(id=1, 
             name='Meta', 
             contact_email='peeps@meta.com', 
             industry='Social Media')
    session_obj.add(emp)
    emp = Employer(id=2, 
             name='Google', 
             contact_email='people@google.com', 
             industry='Internet')
    session_obj.add(emp)

    job = Job(id=1, title='Data Scientist', description="XYZ blah",
               employer_id=1)
    session_obj.add(job)
    job = Job(id=2, title='SWE', description="XYZ blah",
               employer_id=2)
    session_obj.add(job)

    session_obj.commit()
