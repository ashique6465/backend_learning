from fastapi import FastAPI, Query, APIRouter
import math 

app = FastAPI()

users = [{"id":i, "name":f"user{i}"} for i in range(1,100)]

router_v1 = APIRouter(prefix="api/v1", tags=["v1"])

@router_v1.get("/users")
def get_users_v1(
    page: int = Query(1,ge=1),
    limit: int = Query(10,le=100)
):
total = len(users)
total_pages = math.ceil(total / limit)

start = (page - 1) * limit
end = start + limit

return {
    "version": "v1",
    "page": page,
    "limit": limit,
    "total": total,
    "total_pages":total_pages,
    "data": users[start:end]
}

app.include_router(router_v1)