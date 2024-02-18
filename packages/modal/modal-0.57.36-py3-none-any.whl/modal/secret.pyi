import modal.client
import modal.object
import typing
import typing_extensions

class _Secret(modal.object._StatefulObject):
    @staticmethod
    def from_dict(env_dict: typing.Dict[str, typing.Union[str, None]] = {}):
        ...

    @staticmethod
    def from_dotenv(path=None):
        ...

    @staticmethod
    async def create_deployed(deployment_name: str, env_dict: typing.Dict[str, str], namespace=1, client: typing.Union[modal.client._Client, None] = None, environment_name: typing.Union[str, None] = None) -> str:
        ...


class Secret(modal.object.StatefulObject):
    def __init__(self, *args, **kwargs):
        ...

    @staticmethod
    def from_dict(env_dict: typing.Dict[str, typing.Union[str, None]] = {}):
        ...

    @staticmethod
    def from_dotenv(path=None):
        ...

    class __create_deployed_spec(typing_extensions.Protocol):
        def __call__(self, deployment_name: str, env_dict: typing.Dict[str, str], namespace=1, client: typing.Union[modal.client.Client, None] = None, environment_name: typing.Union[str, None] = None) -> str:
            ...

        async def aio(self, *args, **kwargs) -> str:
            ...

    create_deployed: __create_deployed_spec
