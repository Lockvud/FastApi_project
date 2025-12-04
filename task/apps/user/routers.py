from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from apps.user.store_singleton import user_store
from apps.user.store import user_store_connection
from apps.user.repository import UserRepository
from apps.user.services import UserService
from apps.user.schemas import UserCreate, UserUpdate, BulkUsersCreate
from apps.user.models import UserOut
from apps.auth.depth import get_current_user

router = APIRouter()


def get_user_service():
    with user_store_connection(user_store):
        repo = UserRepository(user_store)
        svc = UserService(repo)
        yield svc


@router.post("/", response_model=UserOut, status_code=201)
def create_user(user: UserCreate, svc: UserService = Depends(get_user_service)):
    if svc.get_by_username(user.username):
        raise HTTPException(status_code=400, detail="Username уже существует")
    return svc.create_user(user)


@router.post("/bulk", response_model=List[UserOut], status_code=201)
def create_users_bulk(payload: BulkUsersCreate, svc: UserService = Depends(get_user_service)):
    return svc.create_users_bulk(payload.users)


@router.get("/", response_model=List[UserOut])
def list_users(svc: UserService = Depends(get_user_service)):
    return svc.list_users()


@router.get("/by_ids", response_model=List[UserOut])
def get_by_ids(ids: List[int] = Query(...), svc: UserService = Depends(get_user_service)):
    res = []
    for uid in ids:
        u = svc.get_user(uid)
        if u:
            res.append(u)
    return res


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, svc: UserService = Depends(get_user_service)):
    u = svc.get_user(user_id)
    if not u:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return u


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, svc: UserService = Depends(get_user_service), current_user=Depends(get_current_user)):
    updated = svc.update_user(user_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return updated


@router.delete("/{user_id}", response_model=UserOut)
def delete_user(user_id: int, svc: UserService = Depends(get_user_service),     current_user=Depends(get_current_user)):
    deleted = svc.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return deleted