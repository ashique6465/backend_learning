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
total = len(users)
    total_page = math.ceil(total / limit)
    start = (page - 1) * limit  
    end = start + limit 
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "next_page": page + 1 if page < total_page else None,
        "prev_page": page - 1 if page > 1 else None,
        "data": users[start:end]
    }