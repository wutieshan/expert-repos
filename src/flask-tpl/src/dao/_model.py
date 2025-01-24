import dataclasses


@dataclasses.dataclass(frozen=True, eq=True)
class SysUserModel:
    username: str
    password: str
    email: str
    phone: str
    role_id: str
    status: int
    avatar: str
