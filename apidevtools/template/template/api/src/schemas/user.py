from apidevtools.simpleorm import Schema


class UserBase(Schema):
    __tablename__ = 'user'

    email: str
    avatar_url: str = None

    def pretty(self) -> Schema:
        self.email = self.email.lower()
        return self


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    ...


class User(UserBase):
    id: int
