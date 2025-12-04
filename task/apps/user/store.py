from contextlib import contextmanager
from typing import List, Optional
from apps.user.models import UserInDB


class UserStore:

    def __init__(self):
        self._data: List[UserInDB] = []
        self._next_id = 1

    def get_all(self) -> List[UserInDB]:
        return list(self._data)

    def get_by_id(self, uid: int) -> Optional[UserInDB]:
        return next((u for u in self._data if u.id == uid), None)

    def get_by_username(self, username: str) -> Optional[UserInDB]:
        return next((u for u in self._data if u.username == username), None)

    def add(self, user: UserInDB) -> UserInDB:
        user.id = self._next_id
        self._next_id += 1
        self._data.append(user)
        return user

    def remove(self, uid: int) -> Optional[UserInDB]:
        u = self.get_by_id(uid)
        if u:
            self._data.remove(u)
        return u

    def update(self, uid: int, **kwargs) -> Optional[UserInDB]:
        u = self.get_by_id(uid)
        if not u:
            return None
        data = u.model_dump()
        for k, v in kwargs.items():
            if v is not None:
                data[k] = v
        updated = UserInDB(**data)
        idx = self._data.index(u)
        self._data[idx] = updated
        return updated


@contextmanager
def user_store_connection(store: UserStore):
    print("Открытие соединения UserStore")
    try:
        yield store
    finally:
        print("Закрытие соединения UserStore")
