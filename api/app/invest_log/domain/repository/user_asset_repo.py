from abc import ABCMeta, abstractmethod
from app.invest_log.domain.user_asset import UserAsset


class IUserAssetRepository(metaclass=ABCMeta):
    @abstractmethod
    def search_by_user_id(self, user_id: str) -> list[UserAsset]:
        raise NotImplementedError

    @abstractmethod
    def search_by_user_stock_code(self, user_id: str, stock_code: int) -> UserAsset|None:
        raise NotImplementedError

    @abstractmethod
    def create_user_asset(self, user_asset: UserAsset):
        raise NotImplementedError

    @abstractmethod
    def update_user_asset(self, asset_id: str, user_asset: UserAsset):
        raise NotImplementedError

    @abstractmethod
    def delete_user_asset(self, asset_id: str):
        raise NotImplementedError
