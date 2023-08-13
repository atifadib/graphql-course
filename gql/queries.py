from graphene import ObjectType, List
from gql.types import JobObject, EmployerObject
from db.database import Session
from db.models import Job, Employer

class Query(ObjectType):
    jobs = List(JobObject)
    employers = List(EmployerObject)

    @staticmethod
    def resolve_jobs(root, info):
        with Session() as sess:
            return Session().query(Job).all()

    
    @staticmethod
    def resolve_employers(root, info):
        with Session() as sess:
            return Session().query(Employer).all()