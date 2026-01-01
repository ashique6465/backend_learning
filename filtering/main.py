from fastapi import FastAPI
app = FastAPI()
users = [
    {"id":i, "name": f"user{i}"} for i in range(1,101)
]

@app.get("/users")
def get_users(
    page: int = 1,
    limit: int = 10,
    name: str | None = None
):
    filtered_users = users
    if name:
        filtered_users = [
            u for u in users  if name.lower() in u["name"].lower()
        ]

        start = (page - 1 ) * limit
        end = start + limit

        return {
            "total":len(filtered_users),
            "data":filtered_users[start:end]
        }