from app.repositories.login_repo import UserRepository


class LoginService:

    def __init__(self):
        self.repo = UserRepository()

    def login(self, db, username: str, password: str):
        user = self.repo.find_by_username_and_password(db, username, password)

        if not user:
            return {
                "status": 403,
                "message": "Invalid username or password",
            }

        return {
            "status": 200,
            "message": "Login successful",
        }
