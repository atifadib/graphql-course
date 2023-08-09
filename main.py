from graphene import Schema, ObjectType, String, Int, Field

class userType(ObjectType):
    id = Int()
    name = String()
    age = Int()

class Query(ObjectType):
    user = Field(userType, user_id=Int())

    users = [
        {"id": 1, "name": "atif", "age": 30},
        {"id": 2, "name": "atif1", "age": 310},
        {"id": 3, "name": "atif2", "age": 301},
        {"id": 4, "name": "atif23", "age": 3011},
        {"id": 5, "name": "atif34", "age": 30111},
    ]
    def resolve_user(self, info, user_id):
        matches = [user for user in Query.users if user["id"] == user_id]
        return matches[0] if matches else None

schema = Schema(query=Query)

gql = """
query getUsers{
   user(userId: 4){
        id
        name
        age
   }
}
"""

if __name__ == "__main__":
    output = schema.execute(gql)
    print(output)
