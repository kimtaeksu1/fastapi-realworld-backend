import abc
from typing import Any

from conduit.dtos.user import CreateUserDTO, LoginUserDTO, UserDTO


class IUserAuthService(abc.ABC):
    @abc.abstractmethod
    async def sign_up_user(
        self, session: Any, user_to_create: CreateUserDTO
    ) -> tuple[UserDTO, str]: ...

    @abc.abstractmethod
    async def sign_in_user(
        self, session: Any, user_to_login: LoginUserDTO
    ) -> tuple[UserDTO, str]: ...
