from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from .settings import settings


engine = create_async_engine(settings.database_url)

async_session = async_sessionmaker(engine, expire_on_commit=False)


class ListCommands:

    def __init__(self):
        self._commands: dict[str, "BaseCommand"] = {}
        self._executed: list[str] = []

    def add(self, command: "BaseCommand"):
        self._commands[command.__class__.__name__] = command

    async def execute_commands(self):
        for command_name in self._commands:
            await self._execute_command(command_name)

    async def _execute_command(self, command_name: str):
        if command_name in self._executed:
            return
        
        command = self._commands[command_name]
        if command.depends_on:
            for subcommand_name in command.depends_on:
                await self._execute_command(subcommand_name)

        await command.run_command()
        self._executed.append(command_name)


init_commands = ListCommands()


class MetaCommand(type):

    def __init__(cls, clsname, superclasses, attributes):
        if clsname == 'BaseCommand':
            return

        init_commands.add(cls(async_session))


class BaseCommand(metaclass=MetaCommand):

    depends_on: tuple["BaseCommand"] = tuple()

    def __init__(self, session: AsyncSession):
        self._session = session

    async def run(self):
        await self.run_command()

    async def run_command(self):
        raise NotImplemented


class Base(DeclarativeBase):
    ...
