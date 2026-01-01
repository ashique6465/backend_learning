from fastapi import FastAPI, Query

app = FastAPI()

users = [
    {"id": i, "name": f"user{i}"} for i in range(1,101)
]

@app.get("/users")
def get_users(
    page: int = Query(1,ge=1),
    limit: int = Query(10,le=100)
):
    start = (page - 1) * limit  
    end = start + limit 
    return {
        "page": page,
        "limit": limit,
        "total": len(users),
        "data": users[start:end]
    }