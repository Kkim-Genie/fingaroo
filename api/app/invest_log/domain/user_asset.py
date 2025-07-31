from datetime import datetime
from pydantic import BaseModel

class UserAsset(BaseModel):
    id: str
    user_id: str
    stock_code: str
    stock_name: str
    amount: int

class CreateUserAssetBody(BaseModel):
    access_token: str
    refresh_token: str
    stock_code: str
    stock_name: str
    amount: int

class UpdateUserAssetBody(BaseModel):
    access_token: str
    refresh_token: str
    user_asset: UserAsset

class DeleteUserAssetBody(BaseModel):
    access_token: str
    refresh_token: str
    asset_id: str