from typing import List, Optional
from apps.user.store import UserStore
from apps.user.models import UserInDB
from apps.user.schemas import UserCreate


class UserRepository:
    def __init__(self, store: UserStore):
        self.store = store

    def list_users(self) -> List[UserInDB]:
        return self.store.get_all()

    def get_user(self, uid: int) -> Optional[UserInDB]:
        return self.store.get_by_id(uid)

    def get_by_username(self, username: str) -> Optional[UserInDB]:
        return self.store.get_by_username(username)

    def create_user(self, payload: UserCreate, hashed_password: str) -> UserInDB:
        user = UserInDB(id=0, username=payload.username, email=payload.email, hashed_password=hashed_password)
        return self.store.add(user)

    def create_users_bulk(self, payloads: List[UserCreate], hashed_passwords: List[str]) -> List[UserInDB]:
        created = []
        for p, hp in zip(payloads, hashed_passwords):
            created.append(self.create_user(p, hp))
        return created

    def update_user(self, uid: int, **kwargs) -> Optional[UserInDB]:
        return self.store.update(uid, **kwargs)

    def delete_user(self, uid: int) -> Optional[UserInDB]:
        return self.store.remove(uid)
