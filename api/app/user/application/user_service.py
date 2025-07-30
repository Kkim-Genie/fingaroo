from app.user.domain.repository.user_repo import IUserRepository
from app.user.domain.user import User
from app.config import get_settings
import requests
from datetime import datetime
from app.utils.id_utils import generate_access_token, generate_refresh_token

settings = get_settings()


class UserService:
    def __init__(
        self,
        user_repo: IUserRepository,
    ):
        self.user_repo = user_repo    

    def login(self, code:str):
        try:
            api_url = (
                f"https://nid.naver.com/oauth2.0/token"
                f"?grant_type=authorization_code"
                f"&client_id={settings.NAVER_CLIENT_ID}"
                f"&client_secret={settings.NAVER_CLIENT_SECRET}"
                f"&code={code}"
                f"&state={settings.NAVER_STATE}"
            )
            res = requests.get(api_url);
            response = res.json()
            access_token = response["access_token"]
            token_type = response["token_type"]

            user_info_response = requests.get('https://openapi.naver.com/v1/nid/me', 
                                        headers={
                                            'Authorization': f'{token_type} {access_token}'
                                        })
            user_info = user_info_response.json()
            data_response = user_info["response"]
            id = data_response["id"]
            user = self.user_repo.find_by_id(id)
            user = User(
                id=id,
                name=data_response["name"],
                email=data_response["email"],
                gender=data_response["gender"],
                birthyear=(int)(data_response["birthyear"]),
                reg_date=datetime.now()
            )
            if(user is None):
                self.user_repo.create(user)

            access_token = generate_access_token(user)
            refresh_token = generate_refresh_token(user)

            token = {
                "access_token": access_token,
                "refresh_token": refresh_token
            }

            return True, token, user;
        except Exception as e:
            print(f"Login error: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            if 'res' in locals():
                print(f"Response status: {res.status_code}")
                print(f"Response content: {res.text}")
            return False, None, None

        