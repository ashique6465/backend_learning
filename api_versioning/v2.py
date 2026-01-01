from fastapi import APIRouter, Query

router = APIRouter(prefix="/api/v2", tags=["v2"])

users = [{"id": i, "name": f"user{i}"} for i in range(1, 101)]

@router.get("/users")
def get_users(
    limit: int = Query(5, le=50),
    cursor: int | None = None
):
    if cursor:
        filtered = [u for u in users if u["id"] > cursor]
    else:
        filtered = users

    data = filtered[:limit]
    next_cursor = data[-1]["id"] if data else None

    return {
        "version": "v2",
        "limit": limit,
        "next_cursor": next_cursor,
        "data": data
    }
