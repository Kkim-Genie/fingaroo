from fastapi import HTTPException
from app.invest_log.domain.repository.user_asset_repo import IUserAssetRepository
from app.invest_log.domain.user_asset import UserAsset
from app.utils.id_utils import generate_nanoid


class UserAssetService:
    def __init__(
        self,
        user_asset_repo: IUserAssetRepository,
    ):
        self.user_asset_repo = user_asset_repo    

    def search_by_user_id(self, user_id: str) -> list[UserAsset]:
        return self.user_asset_repo.search_by_user_id(user_id)

    def create(self, user_id: str, stock_code: int, stock_name: str, amount: int):
        check_exist = self.user_asset_repo.search_by_user_stock_code(user_id, stock_code)
        if check_exist:
            raise HTTPException(status_code=400, detail="User asset already exists")

        user_asset = UserAsset(
            id=generate_nanoid(),
            user_id=user_id,
            stock_code=stock_code,
            stock_name=stock_name,
            amount=amount
        )
        return self.user_asset_repo.create_user_asset(user_asset)

    def update(self, user_asset: UserAsset):
        return self.user_asset_repo.update_user_asset(user_asset.id, user_asset)

    def delete(self, asset_id: str):
        return self.user_asset_repo.delete_user_asset(asset_id)
