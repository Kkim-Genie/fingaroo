
from app.database import SessionLocal
from app.user.domain.repository.user_repo import IUserRepository
from app.user.domain.user import User as UserVO
from app.user.infra.db_models.user import User
from app.utils.db_utils import row_to_dict


class UserRepository(IUserRepository):
    def find_by_id(self, id: str) -> UserVO|None:
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == id).first()

        if not user:
            return None

        return UserVO(**row_to_dict(user))

    def create(self, user: UserVO) -> UserVO:
        with SessionLocal() as db:
            user = User(
                id=user.id,
                name=user.name,
                email=user.email,
                gender=user.gender,
                birthyear=user.birthyear,
                reg_date=user.reg_date
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        return UserVO(**row_to_dict(user))