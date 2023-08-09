from graphene import Schema, ObjectType, String, Int, Field, List

class userType(ObjectType):
    id = Int()
    name = String()
    age = Int()

class Query(ObjectType):
    user = Field(userType, user_id=Int())
    users_by_min_age = List(userType, min_age=Int())

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

schema = Schema(query=Query)

gql = """
query getUsers{
   usersByMinAge(minAge: 300){
        id
        name
        age
   }
}
"""

if __name__ == "__main__":
    output = schema.execute(gql, root_value='Root-Value-Dummy')
    print(output)
