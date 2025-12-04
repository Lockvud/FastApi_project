from apps.user.repository import UserRepository
from apps.user.schemas import UserCreate, UserUpdate
from apps.user.models import UserOut
from utils.security import hash_password


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def list_users(self):
        return [UserOut(**u.model_dump()) for u in self.repo.list_users()]

    def get_user(self, uid: int):
        u = self.repo.get_user(uid)
        return UserOut(**u.model_dump()) if u else None

    def get_by_username(self, username: str):
        return self.repo.get_by_username(username)

    def create_user(self, payload: UserCreate):
        hashed = hash_password(payload.password)
        created = self.repo.create_user(payload, hashed)
        return UserOut(**created.model_dump())

    def create_users_bulk(self, payloads):
        created = []
        for p in payloads:
            if self.repo.get_by_username(p.username):
                continue  # пропускаем уже существующих
            created.append(self.create_user(p))
        return created

    def update_user(self, uid: int, payload: UserUpdate):
        data = payload.model_dump(exclude_unset=True)
        if "password" in data:
            data["hashed_password"] = hash_password(data.pop("password"))
        updated = self.repo.update_user(uid, **data)
        return UserOut(**updated.model_dump()) if updated else None

    def delete_user(self, uid: int):
        deleted = self.repo.delete_user(uid)
        return UserOut(**deleted.model_dump()) if deleted else None
