from fastapi import HTTPException
from datetime import datetime, timedelta

from app.database import SessionLocal
from app.invest_log.domain.repository.user_asset_repo import IUserAssetRepository
from app.invest_log.infra.db_models.user_asset import UserAsset
from app.invest_log.domain.user_asset import UserAsset as UserAssetV0
from app.utils.db_utils import row_to_dict


class UserAssetRepository(IUserAssetRepository):
    def search_by_user_id(self, user_id: str) -> list[UserAssetV0]:
        with SessionLocal() as db:
            user_assets = db.query(UserAsset).filter(UserAsset.user_id == user_id).all()

        # 데이터가 없으면 빈 리스트 반환 (오류가 아님)
        if not user_assets:
            return []

        return [UserAssetV0(**row_to_dict(asset)) for asset in user_assets]

    def search_by_user_stock_code(self, user_id: str, stock_code: int) -> UserAssetV0|None:
        with SessionLocal() as db:
            user_asset = db.query(UserAsset).filter(UserAsset.user_id == user_id, UserAsset.stock_code == stock_code).first()
            if not user_asset:
                return None
            return UserAssetV0(**row_to_dict(user_asset))

    def create_user_asset(self, user_asset: UserAssetV0):
        with SessionLocal() as db:
            # domain 모델을 DB 모델로 변환
            db_user_asset = UserAsset(
                id=user_asset.id,
                user_id=user_asset.user_id,
                stock_code=user_asset.stock_code,
                stock_name=user_asset.stock_name,
                amount=user_asset.amount
            )
            db.add(db_user_asset)
            db.commit()

        return user_asset

    def update_user_asset(self, asset_id: str, user_asset: UserAssetV0):
        with SessionLocal() as db:
            db.query(UserAsset).filter(UserAsset.id == asset_id).update({
                "stock_code": user_asset.stock_code,
                "stock_name": user_asset.stock_name,
                "amount": user_asset.amount
            })
            db.commit()

        return user_asset

    def delete_user_asset(self, asset_id: str):
        with SessionLocal() as db:
            db.query(UserAsset).filter(UserAsset.id == asset_id).delete()
            db.commit()
