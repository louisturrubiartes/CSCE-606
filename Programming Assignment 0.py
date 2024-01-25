import sys
import re

class Args:
    def __init__(self, schema: str, arguments: list[str]):
        self.schema = self._parse_schema(schema)
        self.arguments = self._parse_arguments(arguments)
        self._validate_arguments()

    def _parse_schema(self, schema):
        pattern = re.compile(r"([a-zA-Z])([#*]?)")
        return {match.group(1): match.group(2) for match in pattern.finditer(schema)}

    def _parse_arguments(self, args):
        parsed_args = {}
        it = iter(args)
        for arg in it:
            if arg.startswith("-"):
                flag = arg[1]
                if flag in self.schema:
                    if self.schema[flag] == "":
                        parsed_args[flag] = True
                    elif self.schema[flag] == "*":
                        parsed_args[flag] = next(it, "")
                    elif self.schema[flag] == "#":
                        value = next(it, "0")
                        if not value.isdigit():
                            raise ValueError(f"Invalid integer value for -{flag}")
                        parsed_args[flag] = int(value)
                else:
                    raise ValueError(f"Unexpected flag: -{flag}")
            else:
                continue
        return parsed_args

    def _validate_arguments(self):
        for flag in self.schema:
            if self.schema[flag] == "" and flag not in self.arguments:
                self.arguments[flag] = False
            elif self.schema[flag] in ["*", "#"] and flag not in self.arguments:
                self.arguments[flag] = "" if self.schema[flag] == "*" else 0

    def has(self, flag: str) -> bool:
        return flag in self.arguments

    def get_boolean(self, flag: str) -> bool:
        if flag not in self.schema or self.schema[flag] != "":
            raise ValueError(f"Flag -{flag} is not a boolean")
        return self.arguments.get(flag, False)

    def get_string(self, flag: str) -> str:
        if flag not in self.schema or self.schema[flag] != "*":
            raise ValueError(f"Flag -{flag} is not a string")
        return self.arguments.get(flag, "")

    def get_integer(self, flag: str) -> int:
        if flag not in self.schema or self.schema[flag] != "#":
            raise ValueError(f"Flag -{flag} is not an integer")
        return self.arguments.get(flag, 0)