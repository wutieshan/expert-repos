from ._base import AbstractDao
from ._model import SysUserModel


class SysUserDao(AbstractDao):
    def __init__(self):
        super().__init__()

    def get_all_users(self) -> list[SysUserModel]:
        self.proxy.execute()
