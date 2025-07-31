
from app.dart.domain.repository.corp_code_repo import IDartCorpCodeRepository
from app.dart.domain.corp_code import DartCorpCode

class DartCorpCodeService:
    def __init__(
        self,
        corp_code_repo: IDartCorpCodeRepository,
    ):
        self.corp_code_repo = corp_code_repo    

    def get_first(self) -> DartCorpCode:
        return self.corp_code_repo.get_first()

    def find_by_corp_name(self, corp_name: str) -> DartCorpCode:
        return self.corp_code_repo.find_by_corp_name(corp_name)

    def find_by_corp_code(self, corp_code: str) -> DartCorpCode:
        return self.corp_code_repo.find_by_corp_code(corp_code)