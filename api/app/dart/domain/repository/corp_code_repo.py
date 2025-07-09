from abc import ABCMeta, abstractmethod

from app.dart.domain.corp_code import DartCorpCode


class IDartCorpCodeRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_first(self) -> DartCorpCode:
        raise NotImplementedError
    
    # @abstractmethod
    # def find_by_corp_code(self, corp_code: str) -> DartCorpCode:
    #     raise NotImplementedError

    @abstractmethod
    def find_by_corp_name(self, corp_name: str) -> DartCorpCode:
        raise NotImplementedError