from graphene import Schema, ObjectType, String, Int, Field, List, Mutation

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
Mutation Define how data will be updated or added
"""
class Mutation(ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()


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
mutation createUser{
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
mutation updateUser{
    updateUser(id: 6, age: 27){
        user{
            id
            name
            age
        }
    }
}
"""

if __name__ == "__main__":
    output = schema.execute(gql1, root_value='Root-Value-Dummy')
    print(output)
    output = schema.execute(gql2)
    print(output)
    output = schema.execute(gql3)
    print(output)