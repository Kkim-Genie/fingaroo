from abc import ABCMeta, abstractmethod

from app.user.domain.user import User


class IUserRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_by_id(self, id: str) -> User|None:
        raise NotImplementedError
    
    @abstractmethod
    def create(self, user: User) -> User:
        raise NotImplementedError