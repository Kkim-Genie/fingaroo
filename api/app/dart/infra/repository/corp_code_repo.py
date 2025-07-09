from fastapi import HTTPException

from app.database import SessionLocal
from app.dart.domain.repository.corp_code_repo import IDartCorpCodeRepository
from app.dart.domain.corp_code import DartCorpCode as DartCorpCodeVO
from app.dart.infra.db_models.corp_code import DartCorpCode
from app.utils.db_utils import row_to_dict


class DartCorpCodeRepository(IDartCorpCodeRepository):
    def get_first(self) -> DartCorpCodeVO:
        with SessionLocal() as db:
            corp = db.query(DartCorpCode).first()

        if not corp:
            raise HTTPException(status_code=422)

        return DartCorpCodeVO(**row_to_dict(corp))

    def find_by_corp_name(self, corp_name: str) -> DartCorpCodeVO:
        with SessionLocal() as db:
            corp = db.query(DartCorpCode).filter(DartCorpCode.corp_name == corp_name).first()
            if(not corp):
                corp = db.query(DartCorpCode).filter(DartCorpCode.corp_name.like(f"%{corp_name}%")).first()

        if not corp:
            raise HTTPException(status_code=422)

        return DartCorpCodeVO(**row_to_dict(corp))