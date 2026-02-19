
class UserRepository:

    def find_by_username_and_password(self, db, username: str, password: str):
        return db.users.find_one({"username": username, "password": password})
