from maxo.types.base import MaxoType


class CommandObject(MaxoType):
    prefix: str = "/"
    command: str = ""
    args: str | None = None
    mention: str | None = None

    @property
    def mentioned(self) -> bool:
        return self.mention is not None

    @property
    def text(self) -> str:
        line = f"@{self.mention} " if self.mention else ""

        line = f"{line} {self.prefix}{self.command}"
        if self.args:
            line += " " + self.args

        return line
