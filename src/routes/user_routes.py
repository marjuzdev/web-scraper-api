from fastapi import APIRouter

router = APIRouter()

class UserRoutes:
    @router.get("/users")
    async def get_users():
        return {"message": "Lista de usuarios"}

    @router.post("/users")
    async def create_user(user: dict):
        return {"message": "Usuario creado", "user": user}

    @router.get("/users/{user_id}")
    async def get_user(user_id: str):
        return {"message": f"Detalles del usuario {user_id}"}
