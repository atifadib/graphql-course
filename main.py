from graphene import Schema, ObjectType, String, Int, Field, List, Mutation
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String as StringSQL, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DB_URL = """postgresql://postgres:9bm2vSQqfXDreRo4QAMu@containers-us-west-104.railway.app:6194/railway"""
engine = create_engine(DB_URL)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session_obj = Session()

class Employer(Base):
    __tablename__ =  "employers"

    id = Column(Integer, primary_key=True)
    name = Column(StringSQL)
    contact_email = Column(StringSQL)
    industry = Column(StringSQL)
    jobs = relationship("Job", back_populates="employer")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    title = Column(StringSQL)
    description = Column(StringSQL)
    employer_id = Column(Integer, ForeignKey("employers.id"))
    employer = relationship("Employer", back_populates='jobs')

Base.metadata.create_all(engine)

# Code Block for Adding data --> Do not uncommit
# emp = Employer(id=1, 
#          name='Meta', 
#          contact_email='peeps@meta.com', 
#          industry='Social Media')
# session_obj.add(emp)
# emp = Employer(id=2, 
#          name='Google', 
#          contact_email='people@google.com', 
#          industry='Internet')
# session_obj.add(emp)

# job = Job(id=1, title='Data Scientist', description="XYZ blah",
#            employer_id=1)
# session_obj.add(job)
# job = Job(id=2, title='SWE', description="XYZ blah",
#            employer_id=2)
# session_obj.add(job)

# session_obj.commit()

"""
Fields Stored in the User
"""
class UserType(ObjectType):
    id = Int()
    name = String()
    age = Int()

"""
Defines how Data will be queried
"""
class Query(ObjectType):
    user = Field(UserType, user_id=Int())
    users_by_min_age = List(UserType, min_age=Int())

    users = [
        {"id": 1, "name": "atif", "age": 30},
        {"id": 2, "name": "atif1", "age": 310},
        {"id": 3, "name": "atif2", "age": 301},
        {"id": 4, "name": "atif23", "age": 3011},
        {"id": 5, "name": "atif34", "age": 30111},
    ]

    @staticmethod
    def resolve_users_by_min_age(root, info, min_age):
        matches = [user for user in Query.users if user['age'] > min_age]
        return matches if matches else None

    @staticmethod
    def resolve_user(root, info, user_id):
        matches = [user for user in Query.users if user["id"] == user_id]
        return matches[0] if matches else None
    
"""
Create User Mutation Methods
"""
class CreateUser(Mutation):
    class Arguments:
        name = String()
        age = Int()

    user = Field(UserType)
    
    @staticmethod
    def mutate(root, info, name, age):
        user = {"id": len(Query.users) + 1, "name": name, "age": age}
        Query.users.append(user)
        return CreateUser(user=user)
    
"""
Update User Mutation Methods
"""
class UpdateUser(Mutation):
    class Arguments:
        id = Int(required=True)
        name = String()
        age = Int()

    user = Field(UserType)

    @staticmethod
    def mutate(root, info, id, name=None, age=None):
        user = None
        for _ in Query.users:
            if _['id'] == id:
                user = _
                break
        if user is not None:
            user['name'] = name if name else user['name']
            user['age'] = age if age else user['age']
            return UpdateUser(user=user)
        
        return None    

"""
Delete User Mutation
"""
class DeleteUser(Mutation):
    class Arguments:
        id = Int(required=True)

    user = Field(UserType)

    @staticmethod
    def mutate(root, info, id):
        position = None
        for idx, _ in enumerate(Query.users):
            if _['id'] == id:
                position = idx
                break
        if position is not None:
            user = Query.users.pop(idx)
            return DeleteUser(user=user)
        return None

"""
Mutation Define how data will be updated or added
"""
class Mutation(ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


schema = Schema(query=Query, mutation=Mutation)

gql1 = """
query getUsers{
   usersByMinAge(minAge: 300){
        id
        name
        age
   }
}
"""

gql2 = """
mutation {
    createUser(name: "Atif", age: 28){
        user{
            id
            name
            age
        }
    }
}
"""

gql3 = """
mutation {
    updateUser(id: 6, age: 27){
        user{
            id
            name
            age
        }
    }
}
"""

gql4 = """
mutation {
    deleteUser(id: 1){
        user{
            id
            name
            age
        }
    }
}
"""

app = FastAPI()
app.mount("/graphql", GraphQLApp(
    schema=schema,
    on_get=make_graphiql_handler()
))

# if __name__ == "__main__":
#     output = schema.execute(gql1, root_value='Root-Value-Dummy')
#     print(output)
#     output = schema.execute(gql2)
#     print(output)
#     output = schema.execute(gql3)
#     print(output)
#     output = schema.execute(gql4)
#     print(output)