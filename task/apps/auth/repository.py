from apps.user.store import UserStore
from apps.user.repository import UserRepository


class AuthRepository:
    def __init__(self, store: UserStore):
        self.user_repo = UserRepository(store)

    def get_user_by_username(self, username: str):
        return self.user_repo.get_by_username(username)
