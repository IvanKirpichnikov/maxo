from typing import cast

from maxo.routing.ctx import Ctx
from maxo.routing.filters.base import BaseFilter
from maxo.routing.updates.message_created import MessageCreated
from maxo.types.command_object import CommandObject


class CommandParseError(Exception):
    pass


class Command(BaseFilter[MessageCreated]):
    __slots__ = (
        "commands",
        "ignore_case",
        "ignore_mention",
        "prefixes",
    )

    def __init__(
        self,
        *values: str,
        prefixes: str = "/",
        ignore_case: bool = False,
        ignore_mention: bool = False,
    ) -> None:
        if not values:
            raise ValueError("At least one command should be specified")

        if "@" in prefixes:
            raise ValueError("Prefix '@' not supported")

        self.commands = values
        self.prefixes = prefixes
        self.ignore_case = ignore_case
        self.ignore_mention = ignore_mention

    async def execute(
        self,
        update: MessageCreated,
        ctx: Ctx[MessageCreated],
    ) -> bool:
        if not isinstance(update, MessageCreated):
            return False

        if update.message.body is None:
            return False

        if not update.message.body.text:
            return False

        try:
            command = self.parse_command(
                text=update.message.body.text,
                me_username=cast("str", ctx.bot.state.info.username),
            )
        except CommandParseError:
            return False

        ctx.state.command = command

        return True

    def parse_command(self, text: str, me_username: str) -> CommandObject:
        command = self.extract_command(text)
        self.validate_prefix(command=command)
        self.validate_mention(command, me_username)
        command = self.validate_command(command)

        return command

    def extract_command(self, text: str) -> CommandObject:
        try:
            if text.startswith("@"):
                mention, raw_command, *args = text.split(maxsplit=2)
            else:
                mention, (raw_command, *args) = "", (text.split(maxsplit=1))
        except ValueError as e:
            raise CommandParseError("Parse text error") from e

        if len(raw_command) < 2:
            raise CommandParseError("Invalid length command")

        return CommandObject(
            prefix=raw_command[0],
            command=raw_command[1:],
            args=args[0] if args else None,
            mention=mention or None,
        )

    def validate_prefix(self, command: CommandObject) -> None:
        if command.prefix not in self.prefixes:
            raise CommandParseError("Invalid prefix")

    def validate_mention(self, command: CommandObject, me_username: str) -> None:
        if (
            command.mention
            and not self.ignore_mention
            and command.mention.lower() != me_username.lower()
        ):
            raise CommandParseError("Mention did not match")

    def validate_command(self, command: CommandObject) -> CommandObject:
        for allowed_command in self.commands:
            command_name = command.command
            if self.ignore_case:
                command_name = command_name.casefold()

            if command_name == allowed_command:
                return command

        raise CommandParseError("Did not match command pattern")


class CommandStart(Command):
    def __init__(
        self,
        ignore_case: bool = False,
        ignore_mention: bool = False,
    ) -> None:
        super().__init__(
            "start",
            ignore_case=ignore_case,
            ignore_mention=ignore_mention,
        )
