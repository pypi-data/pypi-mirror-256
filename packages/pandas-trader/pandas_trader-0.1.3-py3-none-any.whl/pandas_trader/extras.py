import re


def to_snake_case(name: str) -> str:
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def to_camel_case(name: str) -> str:
    camel_string = "".join(x.capitalize() for x in name.lower().split("_"))
    return name[0].lower() + camel_string[1:]
