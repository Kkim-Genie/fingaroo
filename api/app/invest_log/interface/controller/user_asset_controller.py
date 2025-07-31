from fastapi import APIRouter, Depends, HTTPException, Query
from dependency_injector.wiring import inject, Provide

from app.containers import Container
from app.invest_log.application.user_asset_service import UserAssetService
from app.invest_log.domain.user_asset import CreateUserAssetBody, DeleteUserAssetBody, UpdateUserAssetBody, UserAsset
from app.utils.id_utils import verify_access_token, verify_refresh_token

router = APIRouter(prefix="/invest_log/user_asset", tags=["user_asset"])

@router.get("/", status_code=200, response_model=list[UserAsset])
@inject
def get_user_asset(
    access_token:str=Query(None),
    refresh_token:str=Query(None),
    user_asset_service: UserAssetService = Depends(Provide[Container.user_asset_service]),
):
    user = None
    user = verify_access_token(access_token)
    if(user is None):
        user = verify_refresh_token(refresh_token)

    if(user is None):
        raise HTTPException(status_code=401, detail="Invalid token")

    user_asset = user_asset_service.search_by_user_id(user.id)
    return user_asset

@router.post("/", status_code=201)
@inject
def create_user_asset(
    create_user_asset_body: CreateUserAssetBody,
    user_asset_service: UserAssetService = Depends(Provide[Container.user_asset_service]),
):
    user = None

    user = verify_access_token(create_user_asset_body.access_token)
    if(user is None):
        user = verify_refresh_token(create_user_asset_body.refresh_token)

    if(user is None):
        raise HTTPException(status_code=401, detail="Invalid token")

    user_asset_service.create(user.id, create_user_asset_body.stock_code, create_user_asset_body.stock_name, create_user_asset_body.amount)
    return {"status": "success"}

@router.put("/", status_code=201)
@inject
def update_user_asset(
    update_user_asset_body: UpdateUserAssetBody,
    user_asset_service: UserAssetService = Depends(Provide[Container.user_asset_service]),
):
    user = None

    user = verify_access_token(update_user_asset_body.access_token)
    if(user is None):
        user = verify_refresh_token(update_user_asset_body.refresh_token)

    if(user is None):
        raise HTTPException(status_code=401, detail="Invalid token")

    user_asset_service.update(update_user_asset_body.user_asset)
    return {"status": "success"}

@router.delete("/", status_code=201)
@inject
def delete_user_asset(
    delete_user_asset_body: DeleteUserAssetBody,
    user_asset_service: UserAssetService = Depends(Provide[Container.user_asset_service]),
):
    user = None

    user = verify_access_token(delete_user_asset_body.access_token)
    if(user is None):
        user = verify_refresh_token(delete_user_asset_body.refresh_token)

    if(user is None):
        raise HTTPException(status_code=401, detail="Invalid token")

    user_asset_service.delete(delete_user_asset_body.asset_id)
    return {"status": "success"}